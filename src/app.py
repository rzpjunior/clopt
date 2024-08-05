from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():
        from controllers import main_controller, do_controller
        app.register_blueprint(main_controller.bp)
        app.register_blueprint(do_controller.bp, name='do_blueprint')

        from visualizations.dash_app import create_dashboard
        create_dashboard(app)

    return app

def main():
    app = create_app()
    app.run(debug=True)

if __name__ == '__main__':
    main()
