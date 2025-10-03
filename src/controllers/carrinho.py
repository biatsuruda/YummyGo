from flask import Blueprint, render_template, session, redirect, url_for, flash

# Cria um Blueprint para as rotas do carrinho
carrinho_bp = Blueprint('carrinho', __name__, url_prefix='/carrinho')

@carrinho_bp.route('/')
def view():
    """Exibe o conteúdo do carrinho de compras."""
    # Aqui você implementaria a lógica para obter os itens do carrinho
    # Ex: carrinho_items = session.get('carrinho_items', [])
    # Por enquanto, vamos retornar uma página simples
    return render_template('carrinho/view.html')

# Exemplo de rota para adicionar item (opcional, pode ser adicionado depois)
@carrinho_bp.route('/add/<int:item_id>')
def add_to_cart(item_id):
    """Adiciona um item ao carrinho."""
    # Lógica para adicionar item à sessão ou DB
    flash(f'Item {item_id} adicionado ao carrinho!', 'success')
    return redirect(url_for('carrinho.view'))

# Exemplo de rota para remover item (opcional)
@carrinho_bp.route('/remove/<int:item_id>')
def remove_from_cart(item_id):
    """Remove um item do carrinho."""
    # Lógica para remover item
    flash(f'Item {item_id} removido do carrinho!', 'info')
    return redirect(url_for('carrinho.view'))