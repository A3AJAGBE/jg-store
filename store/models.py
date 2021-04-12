from store import db
from flask_login import UserMixin


class Roles(db.Model):
    """Roles table"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    users = db.relationship('Users', backref='role', lazy=True)

    def __repr__(self):
        return self.name


class Users(UserMixin, db.Model):
    """Users table"""
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    email_confirmed = db.Column(db.Boolean(), nullable=False, default=0)
    email_confirmed_at = db.Column(db.DateTime())
    is_active = db.Column(db.Boolean(), nullable=False, default=1)
    password = db.Column(db.String(300), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False, default=1)

    def __repr__(self):
        return f'{self.first_name} {self.last_name}'


class Contact(db.Model):
    """contact table"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)


class Categories(db.Model):
    """Categories table"""
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), unique=True, nullable=False)
    products = db.relationship('Products', backref='category', lazy=True)

    def __repr__(self):
        return self.category


class Subcategories(db.Model):
    """Sub Categories table"""
    id = db.Column(db.Integer, primary_key=True)
    sub_category = db.Column(db.String(50), unique=True, nullable=False)
    products = db.relationship('Products', backref='subcategory', lazy=True)

    def __repr__(self):
        return self.sub_category


class Products(db.Model):
    """Products table"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    discount = db.Column(db.Integer)
    stock = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(128), unique=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    sub_category_id = db.Column(db.Integer, db.ForeignKey('subcategories.id'), nullable=False)

    def __repr__(self):
        return self.name
