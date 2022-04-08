from flask import Flask, Blueprint
from app.routes.vaccinations_routes import bp as vaccinations_bp

bp_api = Blueprint("api", __name__, url_prefix="")

def init_app(app: Flask):
    bp_api.register_blueprint(vaccinations_bp)

    app.register_blueprint(bp_api)