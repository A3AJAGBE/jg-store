import os
from store import db, app
from flask_login import UserMixin, current_user
from flask_admin import Admin, AdminIndexView, form
from flask_admin.contrib.sqla import ModelView
from flask import url_for, redirect, request
from flask_uploads import UploadSet, IMAGES, configure_uploads
from sqlalchemy import event
# Do not remove the PIL import
import PIL


# Uploads Config
app.config['UPLOADED_IMAGES_DEST'] = image_directory = 'store/static/products_images'
app.config['UPLOADED_IMAGES_URL'] = 'store/static/products_images/'
app.config['UPLOADED_FILES_ALLOW'] = ['.jpg', '.png', '.jpeg']

images = UploadSet('images', IMAGES)
configure_uploads(app, images)


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
    reply = db.Column(db.String(20))
    reply_status = db.Column(db.String(20), default='Not Sent')

    def __repr__(self):
        return self.name

    # @property
    # def reply_email(self):
    #     return f'<a href="mailto:{self.email}?subject=[The Jewelry Gallery] Message Reply">Reply Email</a>'


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

    @property
    def image_filepath(self):
        """To access the product image filepath"""
        return images.path(self.image)


@event.listens_for(Products, 'after_delete')
def delete_image(target):
    """This function deletes the image from the folder."""
    if target.image_filepath is not None:
        try:
            os.remove(target.image_filepath)
        except OSError:
            pass


class MainAdminHomeView(AdminIndexView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role_id == 3

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


class MainAdminView(ModelView):
    column_exclude_list = ['password', 'email_confirmed_at']

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role_id == 3

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


class ImageView(MainAdminView):

    form_extra_fields = {
        'image': form.ImageUploadField(
            base_path=image_directory,
            url_relative_path='products/'
        )
    }


class ContactView(MainAdminView):
    form_choices = {
        'reply_status': [
            ('Sent', 'Sent'),
            ('Not Sent', 'Not Sent')
        ]
    }


"""Flask Admin setup"""
# set bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'flatly'
admin = Admin(app, 'E-store App', url='/',
                   index_view=MainAdminHomeView(name='The Jewelry Gallery'),
                   template_mode='bootstrap3')

# Add administrative views here
admin.add_view(MainAdminView(Roles, db.session, endpoint='admin/roles'))
admin.add_view(MainAdminView(Users, db.session, endpoint='admin/users'))
admin.add_view(ContactView(Contact, db.session, endpoint='admin/contact'))
admin.add_view(MainAdminView(Categories, db.session, endpoint='admin/categories'))
admin.add_view(MainAdminView(Subcategories, db.session, endpoint='admin/subcategories'))
admin.add_view(ImageView(Products, db.session, endpoint='admin/products'))
