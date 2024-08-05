import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from services.cost_tracking_service import fetch_do_cost_data
from visualizations.cost_tracking_charts import create_cost_chart, create_cost_table, create_cost_summary, create_detailed_chart

def create_cost_tracking_dashboard(server):
    dash_app = dash.Dash(
        __name__,
        server=server,
        url_base_pathname='/cost-tracking/',
        external_stylesheets=['https://fonts.googleapis.com/css?family=Roboto:400,500,700&display=swap', '/static/css/style.css']
    )

    df = fetch_do_cost_data()
    regions = df['region'].unique()
    statuses = df['status'].unique()
    memories = df['memory'].unique()

    dash_app.layout = html.Div([
        html.Div([
            html.H1('Cost Tracking Dashboard', className='header-title'),
            html.Div(id='cost-summary', className='summary-box')
        ], className='header'),

        html.Div([
            html.Div([
                html.Label('Select Date Range:', className='filter-label'),
                dcc.DatePickerRange(
                    id='date-picker-range',
                    start_date=df['date'].min(),
                    end_date=df['date'].max(),
                    display_format='YYYY-MM-DD',
                    className='date-picker'
                ),
            ], className='filter-item'),

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

            html.Div([
                html.Label('Select Status:', className='filter-label'),
                dcc.Dropdown(
                    id='status-dropdown',
                    options=[{'label': status, 'value': status} for status in statuses],
                    value='all',
                    multi=False,
                    className='dropdown'
                ),
            ], className='filter-item'),

            html.Div([
                html.Label('Select Memory:', className='filter-label'),
                dcc.Dropdown(
                    id='memory-dropdown',
                    options=[{'label': f'{memory} MB', 'value': memory} for memory in memories],
                    value='all',
                    multi=False,
                    className='dropdown'
                ),
            ], className='filter-item'),
        ], className='filter-container'),

        html.Div([
            dcc.Graph(id='cost-chart', className='chart'),
            dcc.Graph(id='cost-table', className='chart'),
            dcc.Graph(id='detailed-chart', className='chart', style={'display': 'none'}),
        ], className='chart-container'),

        html.Div([
            html.Button('Export Data', id='export-button', className='export-button'),
            dcc.Download(id='download-dataframe-csv'),
        ], className='export-container'),

        dcc.Interval(id='interval-component', interval=60000, n_intervals=0)
    ], className='dashboard')

    @dash_app.callback(
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

    @dash_app.callback(
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

    @dash_app.callback(
        Output('download-dataframe-csv', 'data'),
        [Input('export-button', 'n_clicks')],
        prevent_initial_call=True
    )
    def export_data(n_clicks):
        df = fetch_do_cost_data()
        return dcc.send_data_frame(df.to_csv, 'cost_data.csv')

    return dash_app
