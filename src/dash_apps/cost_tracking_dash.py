import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from services.cost_tracking_service import fetch_do_cost_data
from visualizations.cost_tracking_charts import create_cost_chart, create_cost_table, create_cost_summary, create_detailed_chart

def create_cost_tracking_dashboard(server):
    app = dash.Dash(__name__, server=server, url_base_pathname='/cost-tracking/')

    df = fetch_do_cost_data()
    regions = df['region'].unique()
    statuses = df['status'].unique()
    memories = df['memory'].unique()

    app.layout = html.Div([
        html.H1('Cost Tracking Dashboard'),
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
        dcc.Graph(id='detailed-chart', style={'display': 'none'}),
        html.Button('Export Data', id='export-button'),
        dcc.Download(id='download-dataframe-csv'),
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

    @app.callback(
        Output('detailed-chart', 'figure'),
        [Input('cost-chart', 'clickData')]
    )
    def display_detailed_chart(clickData):
        if clickData is None:
            return {}
        description = clickData['points'][0]['x']
        df = fetch_do_cost_data()
        detailed_chart = create_detailed_chart(df, description)
        return detailed_chart

    @app.callback(
        Output('download-dataframe-csv', 'data'),
        [Input('export-button', 'n_clicks')],
        prevent_initial_call=True
    )
    def export_data(n_clicks):
        df = fetch_do_cost_data()
        return dcc.send_data_frame(df.to_csv, 'cost_data.csv')

    return app
