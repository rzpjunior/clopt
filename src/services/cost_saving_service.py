import pandas as pd
from pydo import Client
from flask import current_app
from app import cache
from datetime import datetime

pricing_table = {
    (1, 512): (0.00595, 4.00),
    (1, 1024): (0.00893, 6.00),
    (1, 2048): (0.01786, 12.00),
    (2, 2048): (0.02679, 18.00),
    (2, 4096): (0.03571, 24.00),
    (4, 8192): (0.07143, 48.00),
    (8, 16384): (0.14286, 96.00)
}

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
            hourly_cost = droplet['size']['price_hourly']
            monthly_cost = hourly_cost * 24 * 30

            usage_data.append({
                'name': droplet['name'],
                'region': droplet['region']['name'],
                'status': droplet['status'],
                'memory': droplet['size']['memory'],
                'vcpus': droplet['size']['vcpus'],
                'hours_running': hours_running,
                'amount': round(amount, 2),
                'price_hourly': f"${hourly_cost:.5f}",
                'current_hourly_cost': round(hourly_cost, 5),
                'current_monthly_cost': round(monthly_cost, 2)
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

    for index, row in df.iterrows():
        recommendations.append({
            'name': row['name'],
            'region': row['region'],
            'current_vcpus': row['vcpus'],
            'memory': row['memory'],
            'hours_running': row['hours_running'],
            'amount': row['amount'],
            'current_hourly_cost': round(row['current_hourly_cost'], 5),
            'current_monthly_cost': row['current_monthly_cost']
        })

    recommendations_df = pd.DataFrame(recommendations)
    return recommendations_df

def slice_nodes(df, sim_nodes):
    df['base_name'] = df['name'].apply(lambda x: '-'.join(x.split('-')[:-1]))
    base_names = df['base_name'].unique()

    sliced_df = pd.DataFrame()
    for base_name in base_names:
        nodes = df[df['base_name'] == base_name].head(sim_nodes)
        sliced_df = pd.concat([sliced_df, nodes])

    return sliced_df.drop(columns=['base_name'])

def simulate_cost_savings(df, sim_vcpus, sim_memory, sim_nodes):
    if df.empty:
        return df

    df = slice_nodes(df, sim_nodes)
    df['simulated_hourly_cost'], df['simulated_monthly_cost'], df['potential_savings'] = zip(*df.apply(lambda row: calculate_simulated_cost(row, sim_vcpus, sim_memory), axis=1))
    return df

def calculate_simulated_cost(row, sim_vcpus, sim_memory):
    try:
        if (sim_vcpus, sim_memory) in pricing_table:
            sim_price_hourly, sim_price_monthly = pricing_table[(sim_vcpus, sim_memory)]
        else:
            sim_price_hourly, sim_price_monthly = 0.00000, 0.00
        
        current_cost = row['current_hourly_cost']
        simulated_hourly_cost = sim_price_hourly
        simulated_monthly_cost = sim_price_monthly
        potential_savings = (current_cost - sim_price_hourly) * row['hours_running']
        
        return simulated_hourly_cost, simulated_monthly_cost, potential_savings
    except KeyError as e:
        print(f"KeyError: {e} not found in row")
        print(row)
        return 0.00000, 0.00, 0.00
    except Exception as e:
        print(f"An error occurred during simulation: {e}")
        return 0.00000, 0.00, 0.00
