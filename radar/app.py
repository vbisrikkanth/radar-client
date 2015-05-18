from flask import Flask
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SignallingSession
from flaskext.markdown import Markdown

from radar.auth.services import load_user
from radar.auth.views import require_login
from radar.context_processors import inject_navigation, inject_delete_form
from radar.models import CreatedModifiedMixin
from radar.ordering import url_for_order_by
from radar.pagination import url_for_per_page, url_for_page
from radar.template_filters import datetime_format, nl2br, date_format, missing
from radar.views import bp as radar_bp
from radar.patients.diagnosis.views import bp as diagnosis_bp
from radar.disease_groups.views import bp as disease_groups_bp
from radar.patients.medications.views import bp as medications_bp
from radar.patients.views import bp as patients_bp
from radar.units.views import bp as units_bp
from radar.users.views import bp as users_bp
from radar.patients.lab_results.views import bp as lab_results_bp
from radar.patients.renal_imaging.views import bp as renal_imaging_bp
from radar.news.views import bp as news_bp
from radar.auth.views import bp as auth_bp
from radar.patients.genetics.views import bp as genetics_bp
from radar.patients.dialysis.views import bp as dialysis_bp
from radar.patients.hospitalisation.views import bp as hospitalisation_bp
from radar.patients.pathology.views import bp as pathology_bp
from radar.patients.transplants.views import bp as transplants_bp
from radar.patients.salt_wasting.views import bp as salt_wasting_bp
from radar.patients.plasmapheresis.views import bp as plasmapheresis_bp
from radar.database import db
from sqlalchemy import event


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    Markdown(app)

    app.register_blueprint(radar_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(disease_groups_bp, url_prefix='/disease-groups')
    app.register_blueprint(units_bp, url_prefix='/units')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(patients_bp, url_prefix='/patients')
    app.register_blueprint(news_bp, url_prefix='/news')

    patient_blueprints = [
        (diagnosis_bp, '/diagnosis'),
        (dialysis_bp, '/dialysis'),
        (genetics_bp, '/genetics'),
        (hospitalisation_bp, '/hospitalisation'),
        (lab_results_bp, '/lab-results'),
        (medications_bp, '/medications'),
        (pathology_bp, '/pathology'),
        (plasmapheresis_bp, '/plasmapheresis'),
        (renal_imaging_bp, '/renal-imaging'),
        (salt_wasting_bp, '/salt-wasting'),
        (transplants_bp, '/transplants'),
    ]

    patient_base = '/patients/<int:patient_id>'

    for bp, url_prefix in patient_blueprints:
        app.register_blueprint(bp, url_prefix=patient_base + url_prefix)

    login_manager.user_loader(load_user)
    login_manager.login_view = 'auth.login'

    app.before_request(require_login)

    app.add_template_filter(date_format)
    app.add_template_filter(datetime_format)
    app.add_template_filter(nl2br)
    app.add_template_filter(missing)

    app.add_template_global(url_for_order_by)
    app.add_template_global(url_for_page)
    app.add_template_global(url_for_per_page)

    app.context_processor(inject_navigation)
    app.context_processor(inject_delete_form)

    # Automatically set the created_user and modified_user
    @event.listens_for(SignallingSession, 'before_flush')
    def receive_before_flush(session, flush_context, instances):
        for obj in session.new:
            if isinstance(obj, CreatedModifiedMixin):
                if obj.created_user is None:
                    obj.created_user = current_user

                obj.modified_user = current_user

        for obj in session.dirty:
            if isinstance(obj, CreatedModifiedMixin):
                obj.modified_user = current_user

    return app