from django import forms
from ..models.reservation import ReservationParent
from django.utils.translation import gettext_lazy as _

class DateTimeInput(forms.DateInput):
    input_type = 'datetime-local'

class ReservationForm(forms.ModelForm):
    class Meta:
        model  = ReservationParent
        fields = ('reservation_datetime', 'num_people', 'representative_name', 'memo')
        widgets = {
            'reservation_datetime': DateTimeInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['num_people'].widget.attrs['placeholder']          = _("Please enter numbers only")
        self.fields['representative_name'].widget.attrs['placeholder'] = _("Please enter the name of the representative")
        self.fields['memo'].widget.attrs['placeholder']                = _("Please enter any requests you have for the store")
