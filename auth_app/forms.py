from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), min_length=5)
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Повторіть пароль")

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Користувач з таким email вже існує")
        return email

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("password2"):
            self.add_error("password2", "Паролі не співпадають")


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, label="Username")
    password = forms.CharField(
        widget=forms.PasswordInput, required=True, label="Пароль"
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Невірний Username")
        return username

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not password:
            raise forms.ValidationError("Пароль не може бути порожнім")
        return password

    def authenticate_user(self):
        user = authenticate(
            username=self.cleaned_data.get("username"),
            password=self.cleaned_data.get("password"),
        )
        if user is None:
            raise forms.ValidationError("Невірний пароль")
        return user
