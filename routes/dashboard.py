from flask import Blueprint, render_template
from flask_login import login_required
from entities.admin import Admin
from entities.paciente import Paciente

bp = Blueprint('dashboard', __name__)

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    pacientes = Paciente.query.all()
    admins = Admin.query.all()
    return render_template('dashboard.html', pacientes=pacientes, admins=admins, show_footer_and_nav=False)
