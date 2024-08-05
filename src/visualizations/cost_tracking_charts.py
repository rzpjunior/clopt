import plotly.express as px
import plotly.graph_objects as go

def create_cost_chart(df):
    if df.empty:
        return {}
    fig = px.line(df, x='date', y='amount', color='region', title='DigitalOcean Droplet Costs by Region')
    fig.update_traces(mode='lines+markers')
    fig.update_layout(clickmode='event+select')
    return fig

def create_cost_table(df):
    if df.empty:
        return {}
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df[col] for col in df.columns],
                   fill_color='lavender',
                   align='left'))
    ])
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
