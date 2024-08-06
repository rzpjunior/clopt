import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_recommendations_table(df):
    if df.empty:
        return {}
    
    formatted_df = df.copy()
    formatted_df['potential_savings'] = formatted_df['potential_savings'].apply(lambda x: f"${x:,.2f}")
    
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(formatted_df.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[formatted_df[col] for col in formatted_df.columns],
                   fill_color='lavender',
                   align='left'))
    ])
    return fig

def create_savings_potential_chart(df):
    if df.empty:
        return {}
    
    fig = px.bar(df, x='name', y='potential_savings', color='region', title='Potential Savings by Resource')
    fig.update_yaxes(tickprefix="$", title_text='Potential Savings ($)')
    return fig

def create_cost_breakdown_chart(df):
    if df.empty:
        return {}
    
    breakdown_df = df[['name', 'amount']].groupby('name').sum().reset_index()
    fig = px.pie(breakdown_df, names='name', values='amount', title='Cost Breakdown by Resource')
    return fig
