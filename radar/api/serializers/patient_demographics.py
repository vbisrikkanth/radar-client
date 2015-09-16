from radar.api.serializers.data_sources import DataSourceSerializerMixin
from radar.api.serializers.meta import MetaSerializerMixin
from radar.lib.serializers import ModelSerializer, ReferenceField, CodedStringSerializer, CodedIntegerSerializer
from radar.lib.models import PatientDemographics, EthnicityCode, GENDERS


class EthnicityCodeSerializer(ModelSerializer):
    class Meta(object):
        model_class = EthnicityCode


class EthnicityCodeReferenceField(ReferenceField):
    model_class = EthnicityCode
    serializer_class = EthnicityCodeSerializer


class PatientDemographicsSerializer(MetaSerializerMixin, DataSourceSerializerMixin, ModelSerializer):
    ethnicity_code = EthnicityCodeReferenceField()
    gender = CodedIntegerSerializer(GENDERS)

    class Meta(object):
        model_class = PatientDemographics
        exclude = ['ethnicity_code_id']