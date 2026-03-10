from flask import Flask, render_template

from models.db import close_db, init_schema
from models import ordenes as ordenes_model
from models import componentes as componentes_model
from routes.clientes import bp as clientes_bp
from routes.equipos import bp as equipos_bp
from routes.ordenes import bp as ordenes_bp
from routes.inventario import bp as inventario_bp


def create_app():
    app = Flask(__name__)

    init_schema()
    app.teardown_appcontext(close_db)

    app.register_blueprint(clientes_bp)
    app.register_blueprint(equipos_bp)
    app.register_blueprint(ordenes_bp)
    app.register_blueprint(inventario_bp)

    @app.route("/")
    def dashboard():
        stats = ordenes_model.estadisticas_dashboard()
        alertas = componentes_model.alertas_stock_bajo()
        return render_template("dashboard.html", stats=stats, alertas=alertas)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
