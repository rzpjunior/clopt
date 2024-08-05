import pandas as pd
from pydo import Client
from flask import current_app

def fetch_do_cost_data():
    token = current_app.config['DIGITALOCEAN_API_TOKEN']
    client = Client(token=token)
    
    try:
        response = client.droplets.list()
        droplets = response['droplets']
        invoice_data = []

        for droplet in droplets:
            invoice_data.append({
                'description': droplet['name'],
                'amount': droplet['size']['price_hourly'] * droplet['size']['memory'],
                'date': droplet['created_at']
            })

        df = pd.DataFrame(invoice_data)
        return df
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()
