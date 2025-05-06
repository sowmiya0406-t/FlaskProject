from flask import Blueprint, flash, render_template, request, redirect, url_for
from models import db
from models.models import Product, Location, ProductMovement

routes = Blueprint('routes', __name__)

@routes.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@routes.route('/')
def home():
    products = Product.query.all()
    return render_template('product.html', products=products)

@routes.route('/products/create', methods=['POST'])
def create_product():
    name = request.form['name']
    quantity = int(request.form['quantity'])
    db.session.add(Product(name=name, quantity=quantity))
    db.session.commit()
    return redirect(url_for('routes.home'))

@routes.route('/products/<int:id>/delete', methods=['POST'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('routes.home'))

@routes.route('/products/<int:id>/update', methods=['POST'])
def update_product(id):
    product = Product.query.get_or_404(id)
    product.name = request.form['name']
    product.quantity = int(request.form['quantity'])
    db.session.commit()
    return redirect(url_for('routes.home'))

@routes.route('/locations')
def locations():
    all_locations = Location.query.all()
    return render_template('locations.html', locations=all_locations)

@routes.route('/locations/create', methods=['POST'])
def create_location():
    name = request.form['name']
    db.session.add(Location(name=name))
    db.session.commit()
    return redirect(url_for('routes.locations'))

@routes.route('/locations/<int:id>/delete', methods=['POST'])
def delete_location(id):
    location = Location.query.get_or_404(id)

    used_in_movements = ProductMovement.query.filter(
        (ProductMovement.from_location_id == id) | 
        (ProductMovement.to_location_id == id)
    ).first()

    if used_in_movements:
        flash("Cannot delete location. It is referenced in product movements.", "danger")
        return redirect(url_for('routes.locations'))

    db.session.delete(location)
    db.session.commit()
    flash("Location deleted successfully.", "success")
    return redirect(url_for('routes.locations'))


@routes.route('/locations/<int:id>/update', methods=['POST'])
def update_location(id):
    location = Location.query.get_or_404(id)
    location.name = request.form['name']
    db.session.commit()
    return redirect(url_for('routes.locations'))


@routes.route('/movements')
def movements():
    all_movements = ProductMovement.query.all()
    products = Product.query.all()
    locations = Location.query.all()
    return render_template('productMovements.html', movements=all_movements, products=products, locations=locations)

@routes.route('/movements/create', methods=['GET', 'POST'])
def create_movement():
    products = Product.query.all()
    locations = Location.query.all()

    if request.method == 'POST':
        try:
            product_id = int(request.form['product_id'])
            from_location_id = int(request.form['from_location_id'])
            to_location_id = int(request.form['to_location_id'])
            quantity = int(request.form['quantity'])

            if from_location_id == to_location_id:
                return "From and To locations must be different", 400

            if quantity <= 0:
                return "Quantity must be a positive integer", 400

            product = Product.query.get_or_404(product_id)

            if product.quantity < quantity:
                return "Not enough stock to move", 400

            product.quantity -= quantity

            movement = ProductMovement(
                product_id=product_id,
                from_location_id=from_location_id,
                to_location_id=to_location_id,
                quantity=quantity
            )

            db.session.add(movement)
            db.session.commit()
            return redirect(url_for('routes.movements'))

        except Exception as e:
            db.session.rollback()
            return f"Error processing movement: {e}", 500

    return render_template('create_movements.html', products=products, locations=locations)

@routes.route('/movements/<int:id>/delete', methods=['POST'])
def delete_movement(id):
    movement = ProductMovement.query.get_or_404(id)
    db.session.delete(movement)
    db.session.commit()
    flash("Movement deleted successfully.", "success")
    return redirect(url_for('routes.movements'))

