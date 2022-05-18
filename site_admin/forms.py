from django import forms
from django.contrib.auth.models import User
from users.models import Quizzes
from users.models import Feedbacks
from captcha.fields import CaptchaField

class AddQuizForm(forms.ModelForm):
    class Meta:
        model = Quizzes
        fields = ['title', 'tot_questions', 'mark_for_correct', 'mark_for_wrong', 'max_time', 'max_mark', 'date_added']

class AddFeedbackReply(forms.ModelForm):
    class Meta:
        model = Feedbacks
        fields = ['reply']

class UpdateFeedbackReply(forms.ModelForm):
    class Meta:
        model = Feedbacks
        fields = ['reply', 'reply_status']

class CaptchaForm(forms.Form):
    captcha = CaptchaField()
