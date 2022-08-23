from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from .models import Route
from .models import ExpenseReport


class LoginForm(AuthenticationForm):
    '''ログインフォーム'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label


class RouteForm(forms.ModelForm):
    '''経路フォーム'''
    class Meta:
        model = Route
        fields = ("departure_point","arrival_point","transportation","fare","account")
        widgets = {
            "account":forms.HiddenInput(),  # 非表示
        }

    def clean_fare(self):
        fare = self.cleaned_data.get('fare')
        if fare < 0:
            raise ValidationError("金額は0以上で入力して下さい!")
        return fare


class ExpenseReportForm(forms.ModelForm):
    '''清算書フォーム
    ExpenseReportモデルに金額フィールドを追加したフォーム
    '''

    # 追加フィールド
    fare = forms.IntegerField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'disabled': 'disabled',
                }
            ),
        )

    class Meta:
        model = ExpenseReport
        fields = ("payment_date","subjects","partner","purpose","route","lap","fare","account")
        widgets = {
            "payment_date":forms.DateInput(attrs={"type":"date"}),
            "account":forms.TextInput(attrs={"hidden":"hidden"}),
        }

    @staticmethod
    def create_formset():
        '''モデルフォームセット'''
        model = ExpenseReport
        return forms.modelformset_factory(model,form=ExpenseReportForm,extra=1,can_delete=True)