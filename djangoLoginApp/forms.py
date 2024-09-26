from django import forms
from djangoLoginApp.models import User


class SignUpForm(forms.Form):
    name = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"placeholder": "Fullname"})
    )
    username = forms.CharField(
        min_length=5,
        max_length=10,
        widget=forms.TextInput(attrs={"placeholder": "Username"}),
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password1 = forms.CharField(
        min_length=8,
        max_length=20,
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
    )
    password2 = forms.CharField(
        min_length=8,
        max_length=20,
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Passwords do not match")
            
        return cleaned_data
