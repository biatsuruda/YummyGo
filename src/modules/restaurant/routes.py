"""
Módulo do Restaurante (Restaurant) - Rotas

Define as rotas para /portal/ (dashboard) e /portal/registar
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from src.modules.restaurant.forms import RestaurantRegistrationForm, CategoryForm, ProductForm, OrderStatusForm
from src.extensions import db
from src.models import Restaurante, Categoria, Produto, Pedido, ItemPedido

# --- Criação do Blueprint ---
restaurant_bp = Blueprint('restaurant', __name__, template_folder='templates')


# --- Dashboard ---
@restaurant_bp.route('/')
@login_required
def dashboard():
    """Página principal do Portal do Restaurante."""
    if current_user.role != 'restaurante':
        flash('Acesso negado. Registe o seu restaurante primeiro.', 'danger')
        return redirect(url_for('restaurant.register'))
    return render_template('dashboard.html')


# --- Registro de Restaurante ---
@restaurant_bp.route('/registar', methods=['GET', 'POST'])
@login_required
def register():
    """Permite que o usuário registre um restaurante."""
    if current_user.role == 'restaurante':
        return redirect(url_for('restaurant.dashboard'))

    form = RestaurantRegistrationForm()
    if form.validate_on_submit():
        novo_restaurante = Restaurante(
            nome_fantasia=form.nome_fantasia.data,
            cnpj=form.cnpj.data,
            taxa_entrega=form.taxa_entrega.data,
            tempo_medio_entrega=form.tempo_medio_entrega.data,
            ativo=False
        )
        try:
            novo_restaurante.dono = current_user
            current_user.role = 'restaurante'
            db.session.add(novo_restaurante)
            db.session.commit()
            flash('Restaurante registado com sucesso!', 'success')
            return redirect(url_for('restaurant.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao registar o restaurante.', 'danger')
            print(f"Erro: {e}")

    return render_template('register_restaurant.html', form=form)


# --- Gestão de Cardápio ---
@restaurant_bp.route('/cardapio', methods=['GET', 'POST'])
@login_required
def manage_menu():
    """Gerencia categorias e produtos do cardápio."""
    if current_user.role != 'restaurante':
        abort(403)

    restaurante = current_user.restaurante
    category_form = CategoryForm()
    product_form = ProductForm()

    # Preenche as opções de categorias no formulário de produto
    product_form.categoria_id.choices = [
        (cat.id, cat.nome)
        for cat in Categoria.query.filter_by(restaurante_id=restaurante.id).order_by(Categoria.nome).all()
    ]

    # Adicionar categoria
    if category_form.submit_category.data and category_form.validate_on_submit():
        nova_categoria = Categoria(nome=category_form.nome.data, restaurante_id=restaurante.id)
        db.session.add(nova_categoria)
        db.session.commit()
        flash('Categoria adicionada com sucesso!', 'success')
        return redirect(url_for('restaurant.manage_menu'))

    # Adicionar produto
    if product_form.submit_product.data and product_form.validate_on_submit():
        novo_produto = Produto(
            nome=product_form.nome.data,
            descricao=product_form.descricao.data,
            preco=product_form.preco.data,
            disponivel=product_form.disponivel.data,
            categoria_id=product_form.categoria_id.data,
            restaurante_id=restaurante.id
        )
        db.session.add(novo_produto)
        db.session.commit()
        flash('Produto adicionado com sucesso!', 'success')
        return redirect(url_for('restaurant.manage_menu'))

    categorias = Categoria.query.filter_by(restaurante_id=restaurante.id).order_by(Categoria.nome).all()
    return render_template('manage_menu.html', category_form=category_form, product_form=product_form, categorias=categorias)


# --- Editar Categoria ---
@restaurant_bp.route('/cardapio/categoria/editar/<int:categoria_id>', methods=['GET', 'POST'])
@login_required
def edit_category(categoria_id):
    if current_user.role != 'restaurante':
        abort(403)
    categoria = Categoria.query.get_or_404(categoria_id)
    if categoria.restaurante_id != current_user.restaurante.id:
        abort(403)

    form = CategoryForm(obj=categoria)
    if form.validate_on_submit():
        categoria.nome = form.nome.data
        db.session.commit()
        flash('Categoria atualizada com sucesso!', 'success')
        return redirect(url_for('restaurant.manage_menu'))

    return render_template('edit_category.html', form=form, categoria=categoria)


# --- Editar Produto ---
@restaurant_bp.route('/cardapio/produto/editar/<int:produto_id>', methods=['GET', 'POST'])
@login_required
def edit_product(produto_id):
    if current_user.role != 'restaurante':
        abort(403)
    produto = Produto.query.get_or_404(produto_id)
    if produto.restaurante_id != current_user.restaurante.id:
        abort(403)

    form = ProductForm(obj=produto)
    form.categoria_id.choices = [
        (cat.id, cat.nome)
        for cat in Categoria.query.filter_by(restaurante_id=current_user.restaurante.id).all()
    ]

    if form.validate_on_submit():
        produto.nome = form.nome.data
        produto.descricao = form.descricao.data
        produto.preco = form.preco.data
        produto.disponivel = form.disponivel.data
        produto.categoria_id = form.categoria_id.data
        db.session.commit()
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('restaurant.manage_menu'))

    return render_template('edit_product.html', form=form, produto=produto)


# --- Apagar Categoria ---
@restaurant_bp.route('/cardapio/categoria/apagar/<int:categoria_id>', methods=['POST'])
@login_required
def delete_category(categoria_id):
    if current_user.role != 'restaurante':
        abort(403)
    categoria = Categoria.query.get_or_404(categoria_id)
    if categoria.restaurante_id != current_user.restaurante.id:
        abort(403)

    db.session.delete(categoria)
    db.session.commit()
    flash('Categoria (e produtos) apagada com sucesso!', 'success')
    return redirect(url_for('restaurant.manage_menu'))


# --- Apagar Produto ---
@restaurant_bp.route('/cardapio/produto/apagar/<int:produto_id>', methods=['POST'])
@login_required
def delete_product(produto_id):
    if current_user.role != 'restaurante':
        abort(403)
    produto = Produto.query.get_or_404(produto_id)
    if produto.restaurante_id != current_user.restaurante.id:
        abort(403)

    # Se o produto já foi pedido, só marcar como indisponível
    if produto.itens_pedido:
        produto.disponivel = False
        flash('Produto não pode ser apagado pois já foi pedido. Marcado como indisponível.', 'warning')
    else:
        db.session.delete(produto)
        flash('Produto apagado com sucesso!', 'success')

    db.session.commit()
    return redirect(url_for('restaurant.manage_menu'))



# --- Gestão de Pedidos ---
STATUS_FLUXO = ['Recebido', 'Em Preparo', 'Em Rota de Entrega', 'Concluído']

@restaurant_bp.route('/pedidos', methods=['GET', 'POST'])
@login_required
def manage_orders():
    if current_user.role != 'restaurante':
        abort(403)

    restaurante = current_user.restaurante
    pedidos = (
        Pedido.query.filter_by(restaurante_id=restaurante.id)
        .order_by(Pedido.data_hora.desc())
        .all()
    )

    if request.method == 'POST':
        pedido_id = request.form.get('pedido_id')
        novo_status = request.form.get('novo_status')

        pedido = Pedido.query.get_or_404(pedido_id)
        if pedido.restaurante_id != restaurante.id:
            abort(403)

        if novo_status in STATUS_FLUXO:
            pedido.status = novo_status
            db.session.commit()
            flash('Status do pedido atualizado com sucesso!', 'success')

        return redirect(url_for('restaurant.manage_orders'))

    return render_template('restaurant_orders.html', pedidos=pedidos, STATUS_FLUXO=STATUS_FLUXO)

@restaurant_bp.route('/pedidos/apagar/<int:pedido_id>', methods=['POST'])
@login_required
def delete_order(pedido_id):
    if current_user.role != 'restaurante':
        abort(403)

    pedido = Pedido.query.get_or_404(pedido_id)
    if pedido.restaurante_id != current_user.restaurante.id:
        abort(403)

    # Apaga os itens do pedido antes de apagar o pedido
    for item in pedido.itens:
        db.session.delete(item)
    db.session.delete(pedido)
    db.session.commit()
    flash('Pedido apagado com sucesso!', 'success')
    return redirect(url_for('restaurant.manage_orders'))

# --- Editar Pedido ---
@restaurant_bp.route('/pedidos/editar/<int:pedido_id>', methods=['GET', 'POST'])
@login_required
def edit_order(pedido_id):
    if current_user.role != 'restaurante':
        abort(403)

    pedido = Pedido.query.get_or_404(pedido_id)
    if pedido.restaurante_id != current_user.restaurante.id:
        abort(403)

    if request.method == 'POST':
        # Exemplo: atualizar status e observações
        novo_status = request.form.get('status')
        if novo_status in STATUS_FLUXO:
            pedido.status = novo_status

        # Aqui você poderia atualizar quantidade de itens, produtos, etc.
        db.session.commit()
        flash('Pedido atualizado com sucesso!', 'success')
        return redirect(url_for('restaurant.manage_orders'))

    return render_template('edit_order.html', pedido=pedido, STATUS_FLUXO=STATUS_FLUXO)
