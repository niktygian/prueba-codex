from flask import Blueprint, render_template, request, redirect, url_for
from models import componentes as componentes_model

bp = Blueprint("inventario", __name__, url_prefix="/inventario")


@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        componentes_model.crear_componente_y_stock(request.form)
        return redirect(url_for("inventario.index"))

    q = request.args.get("q")
    componentes = componentes_model.listar_componentes(q)
    alertas = componentes_model.alertas_stock_bajo()
    return render_template("inventario.html", componentes=componentes, alertas=alertas, q=q or "")
