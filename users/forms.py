from django import forms
from django.contrib.auth.models import User
from .models import Users
from .models import Feedbacks
from captcha.fields import CaptchaField

class UsersForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['fname', 'lname', 'email']

class ActivateForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['status']

class UserPassUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['password']

class AddFeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedbacks
        fields = ['user_id', 'user_name', 'feedback', 'date']

class UpdateFeedback(forms.ModelForm):
    class Meta:
        model = Feedbacks
        fields = ['feedback', 'status', 'date']

class CaptchaForm(forms.Form):
    captcha = CaptchaField()