from django import contrib, forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import PasswordChangeForm
from . import models


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "이메일"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호"})
    )

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error(None, forms.ValidationError("비밀번호가 올바르지 않습니다."))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("유저가 존재하지 않습니다."))


class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")

        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "성"}),
            "last_name": forms.TextInput(attrs={"placeholder": "이름"}),
            "email": forms.EmailInput(attrs={"placeholder": "이메일 주소"}),
        }

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호 "})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호 확인"})
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError(
                "That email is already taken", code="existing_user"
            )
        except models.User.DoesNotExist:
            return email

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)
        user.save()

    def _post_clean(self):
        super()._post_clean()

        password = self.cleaned_data.get("password1")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error("password1", error)


class UpdatePasswordForm(PasswordChangeForm):

    """Update Passord Form Definition"""

    old_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Current Password", "class": "form-btn rounded-t-lg"}
        ),
    )

    new_password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={"placeholder": "New Password", "class": "form-btn"}
        ),
    )
    new_password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confrim New Password",
                "class": "form-btn rounded-b-lg",
            }
        ),
    )
