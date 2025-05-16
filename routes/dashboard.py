from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint('dashboard', __name__)

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')
