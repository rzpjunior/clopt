import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html
from services.cost_tracking_service import fetch_do_cost_data
from visualizations.cost_tracking_charts import create_cost_chart, create_cost_table, create_cost_summary, create_detailed_chart, create_resource_type_chart, create_trend_chart
import pandas as pd

def create_cost_tracking_dashboard(server):
    dash_app = dash.Dash(
        __name__,
        server=server,
        url_base_pathname='/cost-tracking/',
        external_stylesheets=['https://fonts.googleapis.com/css?family=Roboto:400,500,700&display=swap', '/static/css/style.css']
    )

    dash_app.layout = html.Div([
        dcc.Store(id='data-store', data=fetch_do_cost_data().to_dict('records')),
        html.Div([
            html.Div(id='cost-summary', className='summary-box')
        ], className='header'),
        html.Div([
            html.Div([
                html.Label('Select Date Range:', className='filter-label'),
                dcc.DatePickerRange(
                    id='date-picker-range',
                    start_date=fetch_do_cost_data()['date'].min(),
                    end_date=fetch_do_cost_data()['date'].max(),
                    display_format='YYYY-MM-DD',
                    className='date-picker'
                ),
            ], className='filter-item'),
            html.Div([
                html.Label('Select Region:', className='filter-label'),
                dcc.Dropdown(
                    id='region-dropdown',
                    options=[{'label': region, 'value': region} for region in fetch_do_cost_data()['region'].unique()],
                    value='all',
                    multi=False,
                    className='dropdown'
                ),
            ], className='filter-item'),
            html.Div([
                html.Label('Select Status:', className='filter-label'),
                dcc.Dropdown(
                    id='status-dropdown',
                    options=[{'label': status, 'value': status} for status in fetch_do_cost_data()['status'].unique()],
                    value='all',
                    multi=False,
                    className='dropdown'
                ),
            ], className='filter-item'),
            html.Div([
                html.Label('Select Memory:', className='filter-label'),
                dcc.Dropdown(
                    id='memory-dropdown',
                    options=[{'label': f'{memory} MB', 'value': memory} for memory in fetch_do_cost_data()['memory'].unique()],
                    value='all',
                    multi=False,
                    className='dropdown'
                ),
            ], className='filter-item'),
            html.Div([
                html.Label('Select Resource Type:', className='filter-label'),
                dcc.Dropdown(
                    id='resource-type-dropdown',
                    options=[{'label': resource, 'value': resource} for resource in fetch_do_cost_data()['resource_type'].unique()],
                    value='all',
                    multi=False,
                    className='dropdown'
                ),
            ], className='filter-item'),
        ], className='filter-container'),
        html.Div([
            dcc.Graph(id='cost-chart', className='chart'),
            dcc.Graph(id='cost-table', className='chart'),
            dcc.Graph(id='resource-type-chart', className='chart'),
            dcc.Graph(id='trend-chart', className='chart'),
            dcc.Graph(id='detailed-chart', className='chart', style={'display': 'none'}),
        ], className='chart-container'),
        html.Div([
            html.Button('Export Data', id='export-button', className='export-button'),
            dcc.Download(id='download-dataframe-csv'),
        ], className='export-container'),
        dcc.Interval(id='interval-component', interval=60000, n_intervals=0)
    ], className='dashboard')

    @dash_app.callback(
        [Output('data-store', 'data')],
        [Input('interval-component', 'n_intervals')]
    )
    def update_data(n):
        return [fetch_do_cost_data().to_dict('records')]

    @dash_app.callback(
        [Output('cost-chart', 'figure'),
         Output('cost-table', 'figure'),
         Output('cost-summary', 'children'),
         Output('resource-type-chart', 'figure'),
         Output('trend-chart', 'figure')],
        [Input('data-store', 'data'),
         Input('date-picker-range', 'start_date'),
         Input('date-picker-range', 'end_date'),
         Input('region-dropdown', 'value'),
         Input('status-dropdown', 'value'),
         Input('memory-dropdown', 'value'),
         Input('resource-type-dropdown', 'value')]
    )
    def update_dashboard(data, start_date, end_date, selected_region, selected_status, selected_memory, selected_resource_type):
        df = pd.DataFrame(data)
        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        if selected_region and selected_region != 'all':
            df = df[df['region'] == selected_region]
        if selected_status and selected_status != 'all':
            df = df[df['status'] == selected_status]
        if selected_memory and selected_memory != 'all':
            df = df[df['memory'] == int(selected_memory)]
        if selected_resource_type and selected_resource_type != 'all':
            df = df[df['resource_type'] == selected_resource_type]

        cost_chart = create_cost_chart(df)
        cost_table = create_cost_table(df)
        cost_summary = create_cost_summary(df)
        resource_type_chart = create_resource_type_chart(df)
        trend_chart = create_trend_chart(df)
        return cost_chart, cost_table, cost_summary, resource_type_chart, trend_chart

    @dash_app.callback(
        Output('detailed-chart', 'figure'),
        [Input('cost-chart', 'clickData')],
        [State('data-store', 'data')]
    )
    def display_detailed_chart(clickData, data):
        if clickData is None:
            return {}
        description = clickData['points'][0]['x']
        df = pd.DataFrame(data)
        detailed_chart = create_detailed_chart(df, description)
        return detailed_chart

    @dash_app.callback(
        Output('download-dataframe-csv', 'data'),
        [Input('export-button', 'n_clicks')],
        [State('data-store', 'data')],
        prevent_initial_call=True
    )
    def export_data(n_clicks, data):
        df = pd.DataFrame(data)
        return dcc.send_data_frame(df.to_csv, 'cost_data.csv')

    return dash_app
