from flask import Blueprint, render_template
import os

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    google_maps_key = os.environ.get("GOOGLE_MAPS_KEY", "")
    return render_template("main/index.html", google_maps_key=google_maps_key)