import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from .plotly_charts import create_cost_chart

def create_dashboard(server):
    app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard/')

    app.layout = html.Div([
        html.H1('Cloud Cost Optimization Dashboard'),
        dcc.Graph(id='cost-chart'),
        dcc.Interval(id='interval-component', interval=60000, n_intervals=0)
    ])

    @app.callback(Output('cost-chart', 'figure'),
                  [Input('interval-component', 'n_intervals')])
    def update_chart(n):
        return create_cost_chart()

    return app
