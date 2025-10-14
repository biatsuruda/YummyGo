from flask import Blueprint, render_template

restaurantes_bp = Blueprint('restaurantes', __name__, url_prefix='/restaurantes')

@restaurantes_bp.route('/restaurante')  # sem ".html"
def restaurante():
    return render_template('usuarios/restaurante.html')

