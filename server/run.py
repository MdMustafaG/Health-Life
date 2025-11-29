from flask import Flask
from blueprints import init_blueprints

def create_app():
    app = Flask(
        __name__,
        template_folder="../client/templates",
        static_folder="../client/static"
    )

    init_blueprints(app)
    return app


if __name__ == "__main__":
    print("🔥 Starting HealthyLife backend...")
    app = create_app()
    print("🚀 Server running at http://127.0.0.1:5000")
    app.run(debug=True)
