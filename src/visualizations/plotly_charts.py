import plotly.express as px
from services.do_service import fetch_do_cost_data

def create_cost_chart():
    df = fetch_do_cost_data()
    fig = px.line(df, x='date', y='amount', title='DigitalOcean Monthly Costs')
    return fig
