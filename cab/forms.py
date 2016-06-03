#coding: utf8
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'style':'margin:10px; padding:10px;height:40px',
            'class':'form-control ',
                'placeholder': 'Enter Password*'
        })
    )
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'style':'margin:10px; padding:10px;height:40px',
            'class':'form-control ',
                'placeholder': 'Confirm your password*'
        })
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwd and double passwd error')
        return password2


    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    

    class Meta:
        model = get_user_model()
        fields = ('email','firstname','lastname')
        widgets = {
            'email': forms.TextInput(attrs={
                'style':'margin:10px; padding:10px;height:40px',
                'class':'form-control ',
                'placeholder': 'E-mail address*'
            }),
              'firstname': forms.TextInput(attrs={
                'style':'margin:10px; padding:10px;height:40px',
                'class':'form-control ',
                'placeholder': 'First Name*'
            }),
            'lastname': forms.TextInput(attrs={
                'style':'margin:10px; padding:10px;height:40px',
                'class':'form-control ',
                'placeholder': 'Last Name'
            }),
          
        }
        
        

class UserChangeForm(forms.ModelForm):

    '''
    Форма для обновления данных пользователей. Нужна только для того, чтобы не
    видеть постоянных ошибок "Не заполнено поле password" при обновлении данных
    пользователя.
    '''
    password = ReadOnlyPasswordHashField(
        widget=forms.PasswordInput,
        required=False
    )

    def save(self, commit=True):
        user = super(UserChangeForm, self).save(commit=False)
        password = self.cleaned_data["password"]
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ['email', ]


class LoginForm(forms.Form):

    """Форма для входа в систему
    """
    username = forms.CharField()
    password = forms.CharField()
    