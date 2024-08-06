import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from services.cost_saving_service import generate_cost_saving_recommendations
from visualizations.cost_saving_charts import create_recommendations_table, create_savings_potential_chart, create_cost_breakdown_chart
import pandas as pd

def create_cost_saving_dashboard(server):
    dash_app = dash.Dash(
        __name__,
        server=server,
        url_base_pathname='/cost-saving/',
        external_stylesheets=['https://fonts.googleapis.com/css?family=Roboto:400,500,700&display=swap', '/static/css/style.css']
    )

    df = generate_cost_saving_recommendations()
    regions = df['region'].unique()

    dash_app.layout = html.Div([
        dcc.Store(id='data-store', data=df.to_dict('records')),
        html.Div([
            html.Div([
                html.Label('Select Region:', className='filter-label'),
                dcc.Dropdown(
                    id='region-dropdown',
                    options=[{'label': region, 'value': region} for region in regions],
                    value='all',
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
        [Output('recommendations-table', 'figure'),
         Output('savings-potential-chart', 'figure'),
         Output('cost-breakdown-chart', 'figure')],
        [Input('data-store', 'data'),
         Input('region-dropdown', 'value')]
    )
    def update_dashboard(data, selected_region):
        df = pd.DataFrame(data)
        if selected_region and selected_region != 'all':
            df = df[df['region'] == selected_region]

        recommendations_table = create_recommendations_table(df)
        savings_potential_chart = create_savings_potential_chart(df)
        cost_breakdown_chart = create_cost_breakdown_chart(df)
        return recommendations_table, savings_potential_chart, cost_breakdown_chart

    return dash_app
