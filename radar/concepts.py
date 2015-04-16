from collections import defaultdict

from radar.models import SDAMedication
from radar.validators import ValidationError, StopValidation, required, not_empty


class Concept(object):
    validators = {}

    def __init__(self):
        self._reset()

    def _reset(self):
        self.errors = defaultdict(list)

    def _valid(self):
        return not any(len(x) for x in self.errors)

    def _validate(self):
        self._reset()

        for model_key, validators in self.validators.items():
            model_value = getattr(self, model_key)

            for validator in validators:
                try:
                    validator(model_value)
                except ValidationError as e:
                    self.errors[model_key].append(e.message)
                    break
                except StopValidation:
                    break

        if not self._valid():
            return

        self.validate()

    def validate(self):
        pass

    def valid(self):
        self._validate()
        return self._valid()

    def to_sda(self):
        pass

class MedicationConcept(Concept):
    validators = {
        'from_date': [required],
        'name': [not_empty],
    }

    def __init__(self, from_date, to_date, name):
        super(MedicationConcept, self).__init__()

        self.from_date = from_date
        self.to_date = to_date
        self.name = name

    def validate(self):
        super(MedicationConcept, self).validate()

        if self.to_date is not None:
            if self.to_date < self.from_date:
                self.errors['to_date'].append('Must be on or after from date.')

    def to_sda(self):
        medication = SDAMedication()
        medication.from_time = self.from_date
        medication.to_time = self.to_date

        return {
            'medications': [medication]
        }