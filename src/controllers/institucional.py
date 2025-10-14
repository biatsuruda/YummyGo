from flask import Blueprint, render_template, url_for
institucional_bp = Blueprint('institucional', __name__, template_folder='../templates/institucional')

@institucional_bp.route('/sobre-nos')
def sobre_nos():
    return render_template('sobre_nos.html')

@institucional_bp.route('/carreiras')
def carreiras():
    return render_template('carreiras.html')

@institucional_bp.route('/imprensa')
def imprensa():
    return render_template('imprensa.html')

@institucional_bp.route('/central-de-ajuda')
def central_de_ajuda():
    return render_template('central_de_ajuda.html')

@institucional_bp.route('/contato')
def contato():
    return render_template('contato.html')

@institucional_bp.route('/termos-de-uso')
def termos_de_uso():
    return render_template('termos_de_uso.html')

@institucional_bp.route('/faq')
def faq():
    return render_template('faq.html')