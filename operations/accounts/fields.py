

from django.forms.fields import MultipleChoiceField

class TrustedMultipleChoiceField(MultipleChoiceField):

    def valid_value(*args, **kwargs):
        return True


    