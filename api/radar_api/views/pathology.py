from radar_api.serializers.pathology import PathologySerializer
from radar.models import PATHOLOGY_KIDNEY_TYPES, PATHOLOGY_KIDNEY_SIDES, Pathology
from radar.validation.pathology_validation import PathologyValidation
from radar.views.codes import CodedStringListView
from radar.views.data_sources import DataSourceObjectViewMixin
from radar.views.patients import PatientObjectDetailView, PatientObjectListView


class PathologyListView(DataSourceObjectViewMixin, PatientObjectListView):
    serializer_class = PathologySerializer
    model_class = Pathology
    validation_class = PathologyValidation


class PathologyDetailView(DataSourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = PathologySerializer
    model_class = Pathology
    validation_class = PathologyValidation


class PathologyKidneyTypeListView(CodedStringListView):
    items = PATHOLOGY_KIDNEY_TYPES


class PathologyKidneySideListView(CodedStringListView):
    items = PATHOLOGY_KIDNEY_SIDES


def register_views(app):
    app.add_url_rule('/pathology', view_func=PathologyListView.as_view('pathology_list'))
    app.add_url_rule('/pathology/<int:id>', view_func=PathologyDetailView.as_view('pathology_detail'))
    app.add_url_rule('/pathology-kidney-types', view_func=PathologyKidneyTypeListView.as_view('pathology_kidney_type_list'))
    app.add_url_rule('/pathology-kidney-sides', view_func=PathologyKidneySideListView.as_view('pathology_kidney_side_list'))