import plotly.express as px
import plotly.graph_objects as go
from services.real_time_service import fetch_do_cost_data

def create_cost_chart(df):
    if df.empty:
        print("No data available to plot.")
        return go.Figure()
    fig = px.line(df, x='date', y='amount', color='region', title='DigitalOcean Droplet Costs by Region')
    return fig

def create_cost_table(df):
    if df.empty:
        print("No data available to display.")
        return go.Figure()
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df.description, df.amount, df.date, df.region, df.status],
                   fill_color='lavender',
                   align='left'))
    ])
    fig.update_layout(title='Droplet Cost Details')
    return fig
