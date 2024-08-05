from dash_apps.cost_tracking_dash import create_cost_tracking_dashboard
# from dash_apps.recommendations_dash import create_recommendations_dashboard
# from dash_apps.budget_alerts_dash import create_budget_alerts_dashboard
# from dash_apps.historical_analysis_dash import create_historical_analysis_dashboard

def register_dash_apps(app):
    create_cost_tracking_dashboard(app)
    # create_recommendations_dashboard(app)
    # create_budget_alerts_dashboard(app)
    # create_historical_analysis_dashboard(app)
