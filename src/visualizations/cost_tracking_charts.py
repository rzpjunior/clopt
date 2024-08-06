import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_cost_chart(df):
    if df.empty:
        return {}
    fig = px.line(df, x='date', y='amount', color='region', title='DigitalOcean Droplet Costs by Region')
    fig.update_traces(mode='lines+markers')
    fig.update_layout(clickmode='event+select')
    return fig

def create_cost_table(df):
    formatted_df = df.copy()
    formatted_df['date'] = pd.to_datetime(formatted_df['date']).dt.strftime('%Y-%m-%d')
    formatted_df['amount'] = formatted_df['amount'].apply(lambda x: f"${x:,.2f}")
    formatted_df['hourly_price'] = formatted_df['hourly_price'].apply(lambda x: f"${x:,.2f}")

    if df.empty:
        return {}

    total_amount = df['amount'].sum()
    total_hourly_price = df['hourly_price'].sum()
    total_row = ['Total', f"${total_amount:,.2f}", f"${total_hourly_price:,.2f}", '', '', '', '', '']

    if len(total_row) < len(formatted_df.columns):
        total_row.extend([''] * (len(formatted_df.columns) - len(total_row)))

    formatted_df.loc[len(formatted_df)] = total_row

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(formatted_df.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[formatted_df[col] for col in formatted_df.columns],
                   fill_color=[['lavender'] * (len(formatted_df) - 1) + ['lightyellow']],
                   align='left',
                   height=30)
    )])

    fig.update_layout(
        autosize=True,
        margin=dict(l=0, r=0, t=0, b=0),
        height=400,
    )
    
    fig.update_traces(
        columnwidth=[150, 40, 40, 40, 40, 40, 40, 40, 40, 100, 40],
    )
    return fig


def create_cost_summary(df):
    if df.empty:
        return {}
    total_cost = df['amount'].sum()
    average_cost = df['amount'].mean()
    summary = f"Total Cost: ${total_cost:.2f}, Average Cost: ${average_cost:.2f}"
    return summary

def create_detailed_chart(df, description):
    if df.empty:
        return {}
    filtered_df = df[df['description'] == description]
    fig = px.bar(filtered_df, x='date', y='amount', color='region', title=f'Cost Details for {description}')
    return fig

def create_resource_type_chart(df):
    if df.empty:
        return {}
    fig = px.pie(df, values='amount', names='resource_type', title='Cost Distribution by Resource Type')
    return fig

def create_trend_chart(df):
    if df.empty:
        return {}
    fig = px.line(df, x='date', y='amount', title='Historical Cost Trend')
    fig.update_traces(mode='lines+markers')
    return fig
