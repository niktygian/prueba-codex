from flask import Blueprint, render_template, request, redirect, url_for
from models import equipos as equipos_model
from models import clientes as clientes_model

bp = Blueprint("equipos", __name__, url_prefix="/equipos")


@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        equipos_model.crear(request.form)
        return redirect(url_for("equipos.index"))

    q = request.args.get("q")
    equipos = equipos_model.listar(q)
    clientes = clientes_model.listar()
    return render_template("equipos.html", equipos=equipos, clientes=clientes, q=q or "")
