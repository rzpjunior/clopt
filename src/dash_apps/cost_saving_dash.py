import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from services.cost_saving_service import generate_cost_saving_recommendations, simulate_cost_savings
from visualizations.cost_saving_charts import create_recommendations_table, create_savings_potential_chart, create_cost_breakdown_chart
import pandas as pd

# Define the specifications for vCPUs and memory based on the provided image
vcpu_memory_mapping = {
    1: [512, 1024, 2048],
    2: [2048, 4096],
    4: [8192],
    8: [16384]
}

def get_base_names(df):
    df['base_name'] = df['name'].apply(lambda x: '-'.join(x.split('-')[:-2]))
    return df['base_name'].unique()

def filter_by_base_name(df, base_name):
    if base_name == 'all':
        return df
    return df[df['name'].str.startswith(base_name)]

def create_cost_saving_dashboard(server):
    dash_app = dash.Dash(
        __name__,
        server=server,
        url_base_pathname='/cost-saving/',
        external_stylesheets=['https://fonts.googleapis.com/css?family=Roboto:400,500,700&display=swap', '/static/css/style.css']
    )

    df = generate_cost_saving_recommendations()
    base_names = get_base_names(df)

    dash_app.layout = html.Div([
        dcc.Store(id='data-store', data=df.to_dict('records')),
        html.Div([
            html.Div([
                html.Label('Select Droplet Base Name:', className='filter-label'),
                dcc.Dropdown(
                    id='base-name-dropdown',
                    options=[{'label': base_name, 'value': base_name} for base_name in base_names] + [{'label': 'All', 'value': 'all'}],
                    value='all',
                    multi=False,
                    className='dropdown'
                ),
            ], className='filter-item'),
            html.Div([
                html.Label('Simulate vCPUs:', className='filter-label'),
                dcc.Dropdown(
                    id='sim-vcpus',
                    options=[{'label': f'{vcpu} vCPUs', 'value': vcpu} for vcpu in vcpu_memory_mapping.keys()],
                    value=None,
                    multi=False,
                    className='dropdown'
                ),
            ], className='filter-item'),
            html.Div([
                html.Label('Simulate Memory (MiB):', className='filter-label'),
                dcc.Dropdown(
                    id='sim-memory',
                    options=[{'label': f'{memory} MiB', 'value': memory} for memory in vcpu_memory_mapping[1]],
                    value=None,
                    multi=False,
                    className='dropdown'
                ),
            ], className='filter-item'),
            html.Div([
                html.Label('Simulate Nodes:', className='filter-label'),
                dcc.Dropdown(
                    id='sim-nodes',
                    options=[{'label': f'{nodes} Nodes', 'value': nodes} for nodes in range(1, 21)],
                    value=None,
                    multi=False,
                    className='dropdown'
                ),
            ], className='filter-item'),
        ], className='filter-container'),
        html.Div([
            dcc.Graph(id='recommendations-table', className='chart'),
            dcc.Graph(id='savings-potential-chart', className='chart'),
            dcc.Graph(id='cost-breakdown-chart', className='chart'),
        ], className='chart-container'),
        dcc.Interval(id='interval-component', interval=60000, n_intervals=0)
    ], className='dashboard')

    @dash_app.callback(
        [Output('data-store', 'data')],
        [Input('interval-component', 'n_intervals')]
    )
    def update_data(n):
        return [generate_cost_saving_recommendations().to_dict('records')]

    @dash_app.callback(
        Output('sim-memory', 'options'),
        [Input('sim-vcpus', 'value')]
    )
    def set_memory_options(selected_vcpus):
        return [{'label': f'{memory} MiB', 'value': memory} for memory in vcpu_memory_mapping[selected_vcpus]]

    @dash_app.callback(
        [Output('recommendations-table', 'figure'),
         Output('savings-potential-chart', 'figure'),
         Output('cost-breakdown-chart', 'figure')],
        [Input('data-store', 'data'),
         Input('base-name-dropdown', 'value'),
         Input('sim-vcpus', 'value'),
         Input('sim-memory', 'value'),
         Input('sim-nodes', 'value')]
    )
    def update_dashboard(data, base_name, sim_vcpus, sim_memory, sim_nodes):
        df = pd.DataFrame(data)
        df = filter_by_base_name(df, base_name)
        df = simulate_cost_savings(df, sim_vcpus, sim_memory, sim_nodes)

        recommendations_table = create_recommendations_table(df)
        savings_potential_chart = create_savings_potential_chart(df)
        cost_breakdown_chart = create_cost_breakdown_chart(df)
        return recommendations_table, savings_potential_chart, cost_breakdown_chart

    return dash_app
