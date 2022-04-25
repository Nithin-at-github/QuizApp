from django.contrib import admin
from .models import Users
from .models import Quizzes
from .models import Questions
from .models import Feedbacks
from .models import Results

# Register your models here.

admin.site.register(Users)
admin.site.register(Quizzes)
admin.site.register(Questions)
admin.site.register(Feedbacks)
admin.site.register(Results)