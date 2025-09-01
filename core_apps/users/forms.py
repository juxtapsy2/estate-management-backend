from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm

User = get_user_model()

class UserChangeForm(BaseUserChangeForm):
    class Meta(BaseUserChangeForm._meta):
        model = User
        fields = ["first_name", "last_name", "username", "email"]

class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm._meta):
        model = User
        fields = ["first_name", "last_name", "username", "email"]

        error_messages = {
            "duplicate_username": "Username already exists.",
            "duplicate_email": "Email already in used.",
        }

    def clean_email(self) -> str:
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(self.error_messages["duplicate_email"])
        return email
    
    def clean_username(self) -> str:
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(self.error_messages["duplicate_username"])
        return username