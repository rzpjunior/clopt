import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from services.do_service import fetch_do_cost_data
from visualizations.plotly_charts import create_cost_chart, create_cost_table

def create_dashboard(server):
    app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard/')

    app.layout = html.Div([
        html.H1('Cloud Cost Optimization Dashboard'),
        dcc.Dropdown(
            id='region-dropdown',
            options=[
                {'label': 'All Regions', 'value': 'all'},
                {'label': 'Singapore', 'value': 'sgp'},
            ],
            value='all',
            multi=False
        ),
        dcc.Graph(id='cost-chart'),
        dcc.Graph(id='cost-table'),
        dcc.Interval(id='interval-component', interval=60000, n_intervals=0)
    ])

    @app.callback(
        [Output('cost-chart', 'figure'),
         Output('cost-table', 'figure')],
        [Input('interval-component', 'n_intervals'),
         Input('region-dropdown', 'value')]
    )
    def update_dashboard(n, selected_region):
        df = fetch_do_cost_data()
        if selected_region and selected_region != 'all':
            df = df[df['region'] == selected_region]
        
        cost_chart = create_cost_chart(df)
        cost_table = create_cost_table(df)
        return cost_chart, cost_table

    return app
