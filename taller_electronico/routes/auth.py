from flask import Blueprint, render_template, request, redirect, url_for, session

from models import auth as auth_model

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        user = auth_model.login(request.form.get("username", ""), request.form.get("password", ""))
        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["nombre"] = user["nombre"]
            return redirect(url_for("dashboard"))
        error = "Credenciales inválidas"
    return render_template("login.html", error=error)


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
