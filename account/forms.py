from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account, SECTION_CHOICES

class UserCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
           super(UserCreateForm, self).__init__(*args, **kwargs)

           for fieldname in ['username', 'password1', 'password2']:
               self.fields[fieldname].help_text = None

class AccountCreateForm(forms.ModelForm):
    section = forms.MultipleChoiceField(choices=SECTION_CHOICES, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Account
        exclude = ('user','image')
        # widgets = {
        #     name: forms.HiddenInput,
        # }
    
    
    # def clean_section(self):
    #     section = self.cleaned_data['section']

        # if section is not None:
        #     return section
        # else:
        #     raise forms.ValidationError(
        #         'セクションを選択してください'
        #     )

        # return section

# ? AccountとUserの紐付けはviewで行う！