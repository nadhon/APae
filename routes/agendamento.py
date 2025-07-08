from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from entities.agendamento import Agendamento
from extensions import db
from datetime import datetime

bp = Blueprint('agendamento', __name__)

@bp.route('/agendar', methods=['GET', 'POST'])
def agendar():
    if request.method == 'POST':
        try:
            nome_paciente = request.form.get('nome_paciente')
            cpf_paciente = request.form.get('cpf_paciente')
            telefone_paciente = request.form.get('telefone_paciente')
            data = request.form.get('data')
            motivo = request.form.get('motivo')

            data_formatada = datetime.strptime(data, '%Y-%m-%dT%H:%M')

            novo_agendamento = Agendamento(
                nome_paciente=nome_paciente,
                cpf_paciente=cpf_paciente,
                telefone_paciente=telefone_paciente,
                data=data_formatada,
                motivo=motivo
            )

            db.session.add(novo_agendamento)
            db.session.commit()

            flash('Agendamento criado com sucesso!', 'success')
            return redirect(url_for('agendamento.agendar'))

        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar agendamento: {str(e)}', 'danger')

    return render_template('agendamento.html')
