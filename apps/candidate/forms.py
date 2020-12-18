from django import forms
from django.core import validators
from django.core.exceptions import ValidationError


class ApplicationForm(forms.Form):
    name = forms.CharField(validators=[validators.MaxLengthValidator(256)])
    email = forms.EmailField(help_text='example@gmail.com', validators=[validators.MaxLengthValidator(256)])
    phone = forms.CharField(validators=[validators.MaxLengthValidator(14)])
    full_address = forms.CharField(validators=[validators.MaxLengthValidator(512)])
    name_of_university = forms.CharField(validators=[validators.MaxLengthValidator(256)])
    graduation_year = forms.IntegerField(widget=forms.NumberInput, validators=[validators.MinValueValidator(2015),
                                                                               validators.MaxValueValidator(2020)])
    cgpa = forms.FloatField(label='CGPA', required=False, validators=[validators.MinValueValidator(2.0),
                                                        validators.MaxValueValidator(4.0)])
    experience_in_months = forms.IntegerField(required=False, validators=[validators.MinValueValidator(0),
                                                                          validators.MaxValueValidator(100)])
    current_work_place_name = forms.CharField(required=False, validators=[validators.MaxLengthValidator(256)])
    applying_in = forms.ChoiceField(choices=(('Mobile', 'Mobile'), ('Backend', 'Backend')))
    expected_salary = forms.IntegerField(validators=[validators.MinValueValidator(15000),
                                                     validators.MaxValueValidator(60000)])
    field_buzz_reference = forms.CharField(required=False, validators=[validators.MaxLengthValidator(256)])
    github_project_url = forms.CharField(validators=[validators.MaxLengthValidator(512)])
    cv_file = forms.FileField(validators=[validators.FileExtensionValidator(allowed_extensions=['pdf'])])

    # Validation
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.isnumeric():
            raise ValidationError("The value must be Numeric")
        return phone
