from flask import Flask
from blueprints import init_blueprints

def create_app():
    # Initialize Flask app
    app = Flask(
        __name__,
        template_folder="../client/templates",
        static_folder="../client/static"
    )

    # Register all blueprints
    init_blueprints(app)

    return app


# Run Flask app
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
