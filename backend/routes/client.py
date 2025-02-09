#!/usr/bin/python3
"""
API for client
"""
from flask import Blueprint
from __init__ import db, bcrypt
from models.user import User
from models.client import Client
from forms.client import ClientProfileForm
from flask import redirect, render_template, url_for, flash, request
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required


clients_Bp = Blueprint('clients', __name__)


@clients_Bp.route("/client", methods=['GET', 'POST'])
@login_required
def client_profile():
    form = ClientProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.phone_number = form.phone_number.data
        if not current_user.client:
            current_user.client = Client(user=current_user)
        current_user.client.name = form.username.data
        current_user.client.email = form.email.data
        current_user.client.phone_number = form.phone_number.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('clients.client_profile'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phone_number.data = current_user.phone_number
    #return render_template('account.html', title='Account')
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('client.html', title='Client Profile', image_file=image_file, form=form)