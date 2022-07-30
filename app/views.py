from typing import List
from flask import redirect, render_template, request, url_for, Response
from flask.views import MethodView
from flask_login import login_required, login_user, current_user, logout_user
from sqlalchemy.exc import IntegrityError

from . import db
from . import login_manager, bcrypt
from .models import AppUser, Catalogue, CatalogueType, BulkPackType, Producer, MeasurementUnit
from .forms import LoginForm, UpdateUserInformationForm, ChangePasswordForm, CatalogueAddForm
from .serializers import CatalogueSchema
from .error_message import MessageLevel, Message

catalogue_schema = CatalogueSchema()


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
            Message.flash_message(f"Użytkownik z  podanym adresem: {user_email} e-mail nie istnieje.",
                                  MessageLevel.WARNING)
            return redirect(url_for("login_view"))

        if bcrypt.check_password_hash(app_user.password, user_password):
            login_user(app_user)
            next_url = request.args.to_dict().get('next')

            if next_url:
                return redirect(next_url)
            return redirect(url_for("dashboard_view"))

        Message.flash_message("Wprowadzono nieprawidłowe hasło",
                              MessageLevel.WARNING)
        return redirect(url_for("login_view"))


class LogoutView(MethodView):
    """
    Allows the user to log out.
    """

    def get(self) -> Response:
        """
        Redirects logged out user to login site.
        """
        logout_user()
        Message.flash_message("Zostałeś poprawnie wylogowany",
                              MessageLevel.SUCCESS)

        return redirect(url_for("login_view"))


class DashboardView(MethodView):
    methods = ["GET", "POST"]

    def __init__(self) -> None:
        self.template_name = "dashboard.html"

    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect('/?next)=' + request.path)

    @login_required
    def get(self):
        return render_template(self.template_name, current_user=current_user)


class CatalogueView(MethodView):
    methods = ["GET", "POST"]

    def __init__(self) -> None:
        self.template_name = "catalogue.html"

    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect('/?next=' + request.path)

    def __set_select_field_choices(self, form: CatalogueAddForm) -> None:
        measurement_units = MeasurementUnit.query.all()
        catalogue_types = CatalogueType.query.all()
        bulk_packs = BulkPackType.query.all()
        producers = Producer.query.all()

        form.measurement_unit_id.choices = [
            (measurement_unit.id, measurement_unit.name) for measurement_unit in measurement_units
        ]
        form.catalogue_type_id.choices = [
            (catalogue_type.id, catalogue_type.name) for catalogue_type in catalogue_types
        ]
        form.bulk_pack_id.choices = [
            (bulk_pack.id, bulk_pack.name) for bulk_pack in bulk_packs
        ]
        form.producer_id.choices = [
            (producer.id, producer.name) for producer in producers
        ]

    def __get_catalogue_data(self) -> List[tuple]:
        return db.session.query(Catalogue, CatalogueType, BulkPackType, Producer, MeasurementUnit) \
            .join(CatalogueType, CatalogueType.id == Catalogue.catalogue_type_id) \
            .join(BulkPackType, BulkPackType.id == Catalogue.bulk_pack_id) \
            .join(Producer, Producer.id == Catalogue.producer_id) \
            .join(MeasurementUnit, MeasurementUnit.id == Catalogue.measurement_unit_id) \
            .all()

    def __remove_unnecessary_entries(self, form_data: CatalogueAddForm, entries: List[str]) -> Catalogue:
        for entry in entries:
            form_data.pop(entry, None)

        return catalogue_schema.make_catalogue(form_data)

    @login_required
    def get(self):
        catalogue_add_form = CatalogueAddForm()
        self.__set_select_field_choices(catalogue_add_form)
        catalogue = self.__get_catalogue_data()

        return render_template(self.template_name, current_user=current_user, catalogue=catalogue, catalogue_add_form=catalogue_add_form)

    def post(self):
        catalogue_add_form = CatalogueAddForm(request.form)
        self.__set_select_field_choices(catalogue_add_form)

        if catalogue_add_form.validate_on_submit():
            catalogue_to_add = self.__remove_unnecessary_entries(
                catalogue_add_form.data, ['add_product', 'csrf_token'])

            db.session.add(catalogue_to_add)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                Message.flash_message(f'Istnieje już produkt o symbolu "{catalogue_add_form.stock_code.data}"',
                                      MessageLevel.WARNING)
                catalogue = self.__get_catalogue_data()
                return render_template(self.template_name, current_user=current_user, catalogue=catalogue, catalogue_add_form=catalogue_add_form)

            Message.flash_message("Produkt został pomyślnie dodany",
                                  MessageLevel.SUCCESS)
        else:
            error_message = Message.get_err_message(
                catalogue_add_form.errors.values())
            Message.flash_message(f'{error_message}', MessageLevel.WARNING)

        catalogue = self.__get_catalogue_data()
        return render_template(self.template_name, current_user=current_user, catalogue=catalogue, catalogue_add_form=catalogue_add_form)


class ProfileView(MethodView):
    methods = ["GET", "POST"]

    def __init__(self) -> None:
        self.template_name = "profile.html"

    @ login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect('/?next=' + request.path)

    def __update_user(self, user, data_form):
        user.name = data_form.name.data
        user.surname = data_form.surname.data
        user.phone_number = data_form.phone_number.data

        db.session.commit()
        Message.flash_message(
            "Dane zaktualizowane-data", MessageLevel.SUCCESS)

    def __update_password(self, password_form):
        if bcrypt.check_password_hash(current_user.password, password_form.current_password.data):
            user = AppUser.query \
                .filter_by(email_address=current_user.email_address) \
                .first()
            user.password = bcrypt.generate_password_hash(
                password_form.new_password.data)
            db.session.commit()
            Message.flash_message(
                "Hasło zostało zmienione-password", MessageLevel.SUCCESS)
        else:
            Message.flash_message(
                "Podaj poprawne aktualne hasło-password", MessageLevel.WARNING)

    @ login_required
    def get(self):
        data_form = UpdateUserInformationForm()
        password_form = ChangePasswordForm()
        return render_template(self.template_name, current_user=current_user, data_form=data_form, password_form=password_form)

    def post(self):
        data_form = UpdateUserInformationForm(request.form)
        password_form = ChangePasswordForm(request.form)

        if data_form.validate_on_submit():
            user_to_update = AppUser.query \
                .filter_by(email_address=current_user.email_address) \
                .first()
            self.__update_user(user_to_update, data_form)
        elif data_form.save.data:
            error_message = Message.get_err_message(data_form.errors.values())
            Message.flash_message(f'{error_message}-data',
                                  MessageLevel.WARNING)

        if password_form.validate_on_submit():
            self.__update_password(password_form)
        elif password_form.change_password.data:
            error_message = Message \
                .get_err_message(password_form.errors.values())
            Message.flash_message(f'{error_message}-password',
                                  MessageLevel.WARNING)

        return render_template(self.template_name, current_user=current_user, data_form=data_form, password_form=password_form)
