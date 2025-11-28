from .home import home_bp
from .diagnostic import diagnostic_bp
from .dashboard import dashboard_bp
from .chatbot import chatbot_bp
from .appointment import appointment_bp
from .doctorRegistration import doctor_bp
from .feedback import feedback_bp

def init_blueprints(app):
    """Register all blueprints here"""
    app.register_blueprint(home_bp)
    app.register_blueprint(diagnostic_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(appointment_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(feedback_bp)  