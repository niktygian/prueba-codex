from functools import wraps

from flask import Flask, render_template, session, redirect, url_for, request, Response

from models.db import close_db, init_schema
from models import ordenes as ordenes_model
from models import componentes as componentes_model
from models import auth as auth_model
from routes.auth import bp as auth_bp
from routes.clientes import bp as clientes_bp
from routes.equipos import bp as equipos_bp
from routes.ordenes import bp as ordenes_bp
from routes.inventario import bp as inventario_bp
from utils.barcode import code39_svg


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("auth.login", next=request.path))
        return view(*args, **kwargs)

    return wrapped_view


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "taller-electronico-secret-key"

    init_schema()

    with app.app_context():
        auth_model.ensure_default_admin()
        ordenes_model.asegurar_barcodes()

    app.teardown_appcontext(close_db)

    app.register_blueprint(auth_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(equipos_bp)
    app.register_blueprint(ordenes_bp)
    app.register_blueprint(inventario_bp)

    @app.context_processor
    def inject_user():
        return {"session": session}

    @app.before_request
    def protect_routes():
        open_endpoints = {"auth.login", "static"}
        if request.endpoint in open_endpoints or request.endpoint is None:
            return None
        if request.endpoint == "barcode_svg" and session.get("user_id"):
            return None
        if not session.get("user_id"):
            return redirect(url_for("auth.login"))
        return None

    @app.route("/")
    @login_required
    def dashboard():
        stats = ordenes_model.estadisticas_dashboard()
        alertas = componentes_model.alertas_stock_bajo()
        return render_template("dashboard.html", stats=stats, alertas=alertas)

    @app.route("/barcode/<string:value>.svg")
    @login_required
    def barcode_svg(value):
        svg = code39_svg(value)
        return Response(svg, mimetype="image/svg+xml")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
