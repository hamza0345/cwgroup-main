from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import CustomUser, Hobby

class SignupForm(UserCreationForm):
    """
    For server-side signup with extra fields:
      - name (first_name)
      - email
      - date_of_birth
    """

    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'password1', 'password2', 'date_of_birth']

class SigninForm(AuthenticationForm):
    """
    For server-side login form.
    """

    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class ProfileUpdateForm(UserChangeForm):
    """
    Allows editing:
      - name
      - email
      - date_of_birth
      - hobbies (via ModelMultipleChoiceField)
    """

    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    hobbies = forms.ModelMultipleChoiceField(
        queryset=Hobby.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'date_of_birth', 'hobbies']
