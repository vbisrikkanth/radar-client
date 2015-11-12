from radar.serializers.core import Serializer
from radar.serializers.fields import StringField, IntegerField


class BasicUserSerializer(Serializer):
    id = IntegerField()
    username = StringField()
    email = StringField()
    first_name = StringField()
    last_name = StringField()


class CreatedUserMixin(object):
    created_user = BasicUserSerializer(read_only=True)

    def get_model_exclude(self):
        model_exclude = super(CreatedUserMixin, self).get_model_exclude()
        model_exclude.add('created_user_id')
        return model_exclude


class ModifiedUserMixin(object):
    modified_user = BasicUserSerializer(read_only=True)

    def get_model_exclude(self):
        model_exclude = super(ModifiedUserMixin, self).get_model_exclude()
        model_exclude.add('modified_user_id')
        return model_exclude


class MetaSerializerMixin(CreatedUserMixin, ModifiedUserMixin):
    pass