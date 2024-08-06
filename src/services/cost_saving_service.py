import pandas as pd
from pydo import Client
from flask import current_app
from app import cache
from datetime import datetime

def fetch_do_usage_data():
    token = current_app.config['DIGITALOCEAN_API_TOKEN']
    client = Client(token=token)

    cached_data = cache.get('usage_data')
    if cached_data is not None:
        return cached_data

    try:
        response = client.droplets.list()
        droplets = response['droplets']
        usage_data = []

        for droplet in droplets:
            created_at = datetime.strptime(droplet['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            current_time = datetime.utcnow()
            hours_running = (current_time - created_at).total_seconds() / 3600
            amount = droplet['size']['price_hourly'] * hours_running
            
            usage_data.append({
                'name': droplet['name'],
                'region': droplet['region']['name'],
                'status': droplet['status'],
                'memory': droplet['size']['memory'],
                'vcpus': droplet['size']['vcpus'],
                'hours_running': hours_running,
                'amount': round(amount, 2)
            })

        df = pd.DataFrame(usage_data)
        cache.set('usage_data', df, timeout=60 * 5)
        return df

    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()

def generate_cost_saving_recommendations():
    df = fetch_do_usage_data()
    recommendations = []

    # Example logic for underutilized resources
    underutilized_droplets = df[(df['hours_running'] > 720) & (df['vcpus'] > 1)]
    for index, row in underutilized_droplets.iterrows():
        current_cost = row['amount']
        current_price_hourly = current_cost / row['hours_running']
        suggested_price_hourly = current_price_hourly / row['vcpus']
        suggested_cost = suggested_price_hourly * row['hours_running']
        potential_savings = current_cost - suggested_cost

        recommendations.append({
            'name': row['name'],
            'region': row['region'],
            'current_vcpus': row['vcpus'],
            'suggested_vcpus': 1,
            'potential_savings': round(potential_savings, 2),
            'amount': row['amount'],
            'hours_running': row['hours_running'],
            'memory': row['memory']
        })

    recommendations_df = pd.DataFrame(recommendations)
    return recommendations_df

def simulate_cost_savings(df, sim_vcpus, sim_memory, sim_nodes):
    if df.empty:
        return df

    print("DataFrame before simulation:")
    print(df.head())

    df['hourly_cost'], df['monthly_cost'] = zip(*df.apply(lambda row: calculate_simulated_cost(row, sim_vcpus, sim_memory, sim_nodes), axis=1))
    return df

def calculate_simulated_cost(row, sim_vcpus, sim_memory, sim_nodes):
    try:
        sim_price_hourly = (row['amount'] / row['hours_running']) * (sim_vcpus / row['current_vcpus']) * (sim_memory / row['memory'])
        hourly_cost = round(sim_price_hourly, 2)
        monthly_cost = round(hourly_cost * 24 * 30 * sim_nodes, 2)
        return hourly_cost, monthly_cost
    except KeyError as e:
        print(f"KeyError: {e} not found in row")
        print(row)
        return 0, 0
    except Exception as e:
        print(f"An error occurred during simulation: {e}")
        return 0, 0
