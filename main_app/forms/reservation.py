from django import forms
from ..models.reservation import ReservationParent

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
        self.fields['num_people'].widget.attrs['placeholder'] = '数字のみで入力して下さい'
        self.fields['representative_name'].widget.attrs['placeholder'] = '代表者名を入力して下さい'
        self.fields['memo'].widget.attrs['placeholder'] = '店舗への要望がございましたら、入力して下さい'
