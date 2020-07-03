from flask import Blueprint, render_template

bp = Blueprint('main', __name__, template_folder='templates', static_folder='static')

#Index Page
@bp.route('/')
def index():
    return render_template("index.html")