import email
from flask import redirect, render_template, request, flash, url_for
from flask.views import MethodView
from flask_login import login_required, login_user, current_user
import flask_login

from . import db
from . import login_manager, bcrypt
from .models import AppUser
from .forms import LoginForm, UpdateUserInformationForm


@login_manager.user_loader
def load_user(user_id) -> AppUser:
    return AppUser.query.get(int(user_id))


class LoginView(MethodView):
    methods = ["GET", "POST"]

    def __init__(self) -> None:
        self.template_name = "login-bulma.html"

    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for("dashboard_view"))
        form = LoginForm()
        return render_template(self.template_name, form=form)

    def post(self):
        form = LoginForm(request.form)
        user_email = form.email.data
        user_password = form.password.data
        app_user = AppUser.query.filter_by(email_address=user_email).first()

        if not app_user:
            flash(f"User with e-mail address: {user_email} doesn't exists.",
                  "warning")
            return redirect(url_for("login_view"))

        if bcrypt.check_password_hash(app_user.password, user_password):
            login_user(app_user)
            return redirect(url_for("dashboard_view"))

        flash("Invalid password provided", "warning")
        return redirect(url_for("login_view"))


class DashboardView(MethodView):
    methods = ["GET", "POST"]

    def __init__(self) -> None:
        self.template_name = "dashboard.html"

    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect('/?next=' + request.path)

    @login_required
    def get(self):
        return render_template(self.template_name, current_user=current_user)


class CatalogueView(MethodView):
    methods = ["GET", "POST"]

    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect('/?next=' + request.path)

    @login_required
    def get(self):
        return render_template(self.template_name)


class ProfileView(MethodView):
    methods = ["GET", "POST"]

    def __init__(self) -> None:
        self.template_name = "profile.html"

    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect('/?next=' + request.path)

    @login_required
    def get(self):
        form = UpdateUserInformationForm()
        return render_template(self.template_name, current_user=current_user, form=form)

    def post(self):
        form = UpdateUserInformationForm(request.form)
        user_to_update = AppUser.query \
            .filter_by(email_address=form.email_address.data) \
            .first()

        user_to_update.name = form.name.data
        user_to_update.surname = form.surname.data
        user_to_update.phone_number = form.phone_number.data
        user_to_update.email_address = form.email_address.data

        db.session.commit()

        return redirect(url_for("profile_view"))
