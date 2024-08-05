from flask import Flask
from config import Config
from flask_caching import Cache

cache = Cache()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    cache.init_app(app)

    with app.app_context():
        # Register blueprints
        from controllers.main_controller import bp as main_bp
        from controllers.cost_tracking_controller import bp as cost_tracking_bp

        app.register_blueprint(main_bp)
        app.register_blueprint(cost_tracking_bp)

        # Initialize Dash apps
        from dash_apps.cost_tracking_dash import create_cost_tracking_dashboard
        create_cost_tracking_dashboard(app)

    return app

def main():
    app = create_app()
    app.run(debug=True)

if __name__ == '__main__':
    main()
