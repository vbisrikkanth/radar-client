from radar.validation.core import Field, Validation, ListField, ValidationError
from radar.validation.meta import MetaValidationMixin
from radar.validation.validators import not_empty, none_if_blank, optional, email_address, max_length, required, upper, lower
from radar.validation.number_validators import gmc_number


class GroupConsultantValidation(MetaValidationMixin, Validation):
    group = Field([required()])

    def validate_group(self, group):
        if group.type != 'HOSPITAL':
            raise ValidationError('Must be a hospital.')

        return group


class GroupConsultantListField(ListField):
    def __init__(self, chain=None):
        super(GroupConsultantListField, self).__init__(GroupConsultantValidation(), chain=chain)

    def validate(self, group_consultants):
        group_ids = set()

        for i, group_consultant in enumerate(group_consultants):
            group_id = group_consultant.group.id

            if group_id in group_ids:
                raise ValidationError({i: {'group': 'Consultant already in group.'}})
            else:
                group_ids.add(group_id)

        return group_consultants


class ConsultantValidation(MetaValidationMixin, Validation):
    first_name = Field([not_empty(), upper(), max_length(100)])
    last_name = Field([not_empty(), upper(), max_length(100)])
    email = Field([none_if_blank(), optional(), lower(), email_address()])
    telephone_number = Field([none_if_blank(), optional(), max_length(100)])
    gmc_number = Field([optional(), gmc_number()])
    group_consultants = GroupConsultantListField()
