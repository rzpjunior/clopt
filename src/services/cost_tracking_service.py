import pandas as pd
from pydo import Client
from flask import current_app
from app import cache
from datetime import datetime

def fetch_do_cost_data():
    token = current_app.config['DIGITALOCEAN_API_TOKEN']
    client = Client(token=token)

    cached_data = cache.get('cost_data')
    if cached_data is not None:
        return cached_data

    try:
        response = client.droplets.list()
        droplets = response['droplets']
        invoice_data = []

        for droplet in droplets:
            created_at = datetime.strptime(droplet['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            current_time = datetime.utcnow()
            hours_running = (current_time - created_at).total_seconds() / 3600
            amount = droplet['size']['price_hourly'] * hours_running
            
            invoice_data.append({
                'description': droplet['name'],
                'amount': round(amount, 2),
                'date': pd.to_datetime(droplet['created_at']),
                'region': droplet['region']['name'],
                'status': droplet['status'],
                'memory': droplet['size']['memory'],
                'vcpus': droplet['size']['vcpus'],
                'disk': droplet['size']['disk'],
                'tags': ', '.join(droplet['tags']),
                'resource_type': 'Droplet'
            })

        df = pd.DataFrame(invoice_data)
        cache.set('cost_data', df, timeout=60 * 5)
        return df

    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()
