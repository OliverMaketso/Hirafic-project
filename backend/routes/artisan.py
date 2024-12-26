#!/usr/bin/python3
"""
API for artisan
"""
import os
import secrets
from PIL import Image
from flask import Blueprint
from __init__ import db, bcrypt
from models.user import User
from models.artisan import Artisan
from forms.artisan import ArtisanProfileForm
from flask import redirect, render_template, url_for, flash, request, current_app
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required


artisans_Bp = Blueprint('artisans', __name__)



def save_picture(form_picture):
    """ function to save the updated profile picture"""
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture.filename)
    pic_fname = random_hex + file_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', pic_fname)
    
    output_size = (125, 125)
    open_image = Image.open(form_picture)
    open_image.thumbnail(output_size)
    
    open_image.save(picture_path)
    return pic_fname


@artisans_Bp.route("/artisan", methods=['GET', 'POST'])
@login_required
def artisan_profile():
    form = ArtisanProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.phone_number = form.phone_number.data
        if not current_user.artisan:
            current_user.artisan = Artisan(user=current_user)
        current_user.artisan.name = form.username.data
        current_user.artisan.email = form.email.data
        current_user.artisan.phone_number = form.phone_number.data
        current_user.artisan.location = form.location.data
        current_user.artisan.specialization = form.specialization.data
        current_user.artisan.skills = form.skills.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('artisans.artisan_profile'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phone_number.data = current_user.phone_number
        form.location.data = current_user.artisan.location
        form.specialization.data = current_user.artisan.specialization
        form.skills.data = current_user.artisan.skills
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    #return render_template('account.html', title='Account')
    return render_template('artisan.html', title='Artisan Profile', image_file=image_file, form=form)