from django import forms
from django.utils.safestring import mark_safe

from apps.main.models.models import Status, Departure


class ChangeStatusForm(forms.Form):
    _selected_action = forms.CharField(
        widget=forms.MultipleHiddenInput,
        label='hidden'
    )
    message = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'class': 'vLargeTextField'}
        ),
        label=mark_safe('Комментарий')
    )


class CreateDepartureForm(forms.ModelForm):
    _selected_action = forms.CharField(
        widget=forms.MultipleHiddenInput,
        label='hidden'
    )

    class Meta:
        model = Departure
        fields = '__all__'


class ChangeGlobalStatusForm(ChangeStatusForm):
    status = forms.ChoiceField(
        choices=Status.choices,
        label=mark_safe('Статус заказа'),
    )

    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        super().__init__(*args, **kwargs)
        self.fields['status'].widget.attrs['class'] = 'selection'
