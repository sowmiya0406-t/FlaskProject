from datetime import datetime
from models import db 

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    movements = db.relationship('ProductMovement', backref='product', lazy=True)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    movements_from = db.relationship(
        'ProductMovement',
        foreign_keys='ProductMovement.from_location_id',
        backref='from_location',
        lazy=True
    )
    movements_to = db.relationship(
        'ProductMovement',
        foreign_keys='ProductMovement.to_location_id',
        backref='to_location',
        lazy=True
    )

class ProductMovement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    from_location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    to_location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
