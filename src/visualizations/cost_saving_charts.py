import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_recommendations_table(df):
    if df.empty:
        return {}

    # Calculate totals
    total_amount = df['amount'].sum()
    total_current_hourly_cost = df['current_hourly_cost'].sum()
    total_current_monthly_cost = df['current_monthly_cost'].sum()
    total_simulated_hourly_cost = df['simulated_hourly_cost'].sum()
    total_simulated_monthly_cost = df['simulated_monthly_cost'].sum()
    total_potential_savings = df['potential_savings'].sum()
    total_deduction = df['amount_to_pay'].sum()

    formatted_df = df.copy()
    formatted_df['potential_savings'] = formatted_df['potential_savings'].apply(lambda x: f"${x:,.2f}")
    formatted_df['amount_to_pay'] = formatted_df['amount_to_pay'].apply(lambda x: f"${x:,.2f}")
    formatted_df['current_hourly_cost'] = formatted_df['current_hourly_cost'].apply(lambda x: f"${x:,.5f}")
    formatted_df['current_monthly_cost'] = formatted_df['current_monthly_cost'].apply(lambda x: f"${x:,.2f}")
    formatted_df['simulated_hourly_cost'] = formatted_df['simulated_hourly_cost'].apply(lambda x: f"${x:,.5f}")
    formatted_df['simulated_monthly_cost'] = formatted_df['simulated_monthly_cost'].apply(lambda x: f"${x:,.2f}")
    formatted_df['amount'] = formatted_df['amount'].apply(lambda x: f"${x:,.2f}")
    formatted_df['hours_running'] = formatted_df['hours_running'].apply(lambda x: f"{x:.2f} hours")

    # Ensure total_row has the same length as columns in formatted_df
    total_row = pd.DataFrame([{
        'name': 'Total',
        'region': '',
        'current_vcpus': '',
        'memory': '',
        'hours_running': '',
        'current_hourly_cost': f"${total_current_hourly_cost:,.5f}",
        'current_monthly_cost': f"${total_current_monthly_cost:,.2f}",
        'simulated_hourly_cost': f"${total_simulated_hourly_cost:,.5f}",
        'simulated_monthly_cost': f"${total_simulated_monthly_cost:,.2f}",
        'potential_savings': f"${total_potential_savings:,.2f}",
        'amount_to_pay': f"${total_deduction:,.2f}",
        'amount': f"${total_amount:,.2f}"
    }])

    formatted_df = pd.concat([formatted_df, total_row], ignore_index=True)

    fill_color = [['lavender'] * len(formatted_df) for _ in range(len(formatted_df.columns))]
    for i, col in enumerate(formatted_df.columns):
        if col in ['simulated_hourly_cost', 'simulated_monthly_cost', 'potential_savings']:
            fill_color[i] = ['lightgreen'] * len(formatted_df)
            fill_color[i][-1] = 'lightyellow'
        elif col in ['amount_to_pay']:
            fill_color[i] = ['tomato'] * len(formatted_df)
            fill_color[i][-1] = 'lightyellow'

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(formatted_df.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[formatted_df[col] for col in formatted_df.columns],
                   fill_color=fill_color,
                   align='left',
                   height=30)
    )])

    fig.update_layout(
        autosize=True,
        margin=dict(l=0, r=0, t=0, b=0),
        height=400,
    )

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
