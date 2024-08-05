import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from services.real_time_service import fetch_do_cost_data
from visualizations.real_time_charts import create_cost_chart, create_cost_table, create_cost_summary

def create_real_time_dashboard(server):
    app = dash.Dash(__name__, server=server, url_base_pathname='/cost-tracking/')

    df = fetch_do_cost_data()
    regions = df['region'].unique()
    statuses = df['status'].unique()
    memories = df['memory'].unique()

    app.layout = html.Div([
        html.H1('Real-Time Cost Dashboard'),
        html.Div(id='cost-summary'),
        dcc.DatePickerRange(
            id='date-picker-range',
            start_date=df['date'].min(),
            end_date=df['date'].max()
        ),
        dcc.Dropdown(
            id='region-dropdown',
            options=[{'label': region, 'value': region} for region in regions],
            value='all',
            multi=False
        ),
        dcc.Dropdown(
            id='status-dropdown',
            options=[{'label': status, 'value': status} for status in statuses],
            value='all',
            multi=False
        ),
        dcc.Dropdown(
            id='memory-dropdown',
            options=[{'label': f'{memory} MB', 'value': memory} for memory in memories],
            value='all',
            multi=False
        ),
        dcc.Graph(id='cost-chart'),
        dcc.Graph(id='cost-table'),
        dcc.Interval(id='interval-component', interval=60000, n_intervals=0)
    ])

    @app.callback(
        [Output('cost-chart', 'figure'),
         Output('cost-table', 'figure'),
         Output('cost-summary', 'children')],
        [Input('interval-component', 'n_intervals'),
         Input('date-picker-range', 'start_date'),
         Input('date-picker-range', 'end_date'),
         Input('region-dropdown', 'value'),
         Input('status-dropdown', 'value'),
         Input('memory-dropdown', 'value')]
    )
    def update_dashboard(n, start_date, end_date, selected_region, selected_status, selected_memory):
        df = fetch_do_cost_data()
        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        if selected_region and selected_region != 'all':
            df = df[df['region'] == selected_region]
        if selected_status and selected_status != 'all':
            df = df[df['status'] == selected_status]
        if selected_memory and selected_memory != 'all':
            df = df[df['memory'] == int(selected_memory)]
        
        cost_chart = create_cost_chart(df)
        cost_table = create_cost_table(df)
        cost_summary = create_cost_summary(df)
        return cost_chart, cost_table, cost_summary

    return app
