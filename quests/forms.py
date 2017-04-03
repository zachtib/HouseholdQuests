from django import forms
from django.core.exceptions import ValidationError


class SpendForm(forms.Form):
    amount = forms.DecimalField(decimal_places=2, min_value=0)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(SpendForm, self).__init__(*args, **kwargs)

    def clean_amount(self):
        data = self.cleaned_data['amount']
        if data > self.user.profile.balance:
            raise ValidationError("Not enough money in account")
        return data
