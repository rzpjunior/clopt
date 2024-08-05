from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():
        from controllers.main_controller import bp as main_bp
        from controllers.real_time_controller import bp as real_time_bp
        # from controllers.recommendations_controller import bp as recommendations_bp
        # from controllers.budget_alerts_controller import bp as budget_alerts_bp
        # from controllers.historical_analysis_controller import bp as historical_analysis_bp

        app.register_blueprint(main_bp)
        app.register_blueprint(real_time_bp, name='real_time_blueprint')
        # app.register_blueprint(recommendations_bp, name='recommendations_blueprint')
        # app.register_blueprint(budget_alerts_bp, name='budget_alerts_blueprint')
        # app.register_blueprint(historical_analysis_bp, name='historical_analysis_blueprint')

        from visualizations.dash_app import create_dashboard
        create_dashboard(app)

    return app

def main():
    app = create_app()
    app.run(debug=True)

if __name__ == '__main__':
    main()
