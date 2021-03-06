"""quizapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from users import views as users_views
from site_admin import views as admin_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),

    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
    
    path('', users_views.home, name='home'),
    path('signup', users_views.signup, name='signup'),
    path('signout', users_views.signout, name='signout'),
    path('contact', users_views.contact, name='contact'),
    path('forgot_password', users_views.forgot_password, name='forgot_password'),
    path('reset_password/<uid64>/<token>/', users_views.reset_password, name='reset_password'),
    path('activate/<uid64>/<token>/', users_views.activate, name='activate'),
    path('feedbacks', users_views.feedbacks, name='feedbacks'),
    path('user_dashboard/<name>/<id64>/', users_views.user_dashboard, name='user_dashboard'),
    path('instructions/<user_id>/<quiz_id>/', users_views.instructions, name='instructions'),
    path('attempt/<user_id>/<quiz_id>/', users_views.attempt, name='attempt'),
    path('add_feedback/<user_id>/type/', users_views.add_feedback, name='add_feedback'),
    path('reply_notify/<user_id>/', users_views.reply_notify, name='reply_notify'),
    path('user_view_feedbacks/<user_id>/', users_views.user_view_feedbacks, name='user_view_feedbacks'),
    path('update_feedback/<user_id>/<feed_id>/', users_views.update_feedback, name='update_feedback'),
    path('delete_feedback/<user_id>/<feed_id>/', users_views.delete_feedback, name='delete_feedback'),
    path('user_view_results/<user_id>/', users_views.user_view_results, name='user_view_results'),
    path('view_logs/<user_id>/<quiz_id>/<cand_id>/<mode>/', users_views.view_logs, name='view_logs'),
    path('user_account/<user_id>/', users_views.user_account, name='user_account'),
    path('update_user_details/<user_id>/', users_views.update_user_details, name='update_user_details'),
    path('user_change_password/<user_id>/', users_views.user_change_password, name='user_change_password'),

    path('generate_result/<user_id>/<quiz_id>/<token>/', users_views.generate_result, name='generate_result'),
    
    path('admin_dashboard/<name>/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('add_quiz/<name>/', admin_views.add_quiz, name='add_quiz'),
    path('result_notify/<name>/', admin_views.result_notify, name='result_notify'),
    path('view_results/<name>/', admin_views.view_results, name='view_results'),
    path('delete_result/<id>/<name>/', admin_views.delete_result, name='delete_result'),
    path('add_update_questions/<int:qid>/<name>/', admin_views.add_update_questions, name='add_update_questions'),
    path('delete_quiz/<id>/<name>/', admin_views.delete_quiz, name='delete_quiz'),
    path('update_quiz/<id>/<name>/', admin_views.update_quiz, name='update_quiz'),
    path('user_notify/<name>/', admin_views.user_notify, name='user_notify'),
    path('view_users/<name>/', admin_views.view_users, name='view_users'),
    path('feed_notify/<name>/', admin_views.feed_notify, name='feed_notify'),
    path('view_feedbacks/<name>/', admin_views.view_feedbacks, name='view_feedbacks'),
    path('delete_user/<id>/<name>/', admin_views.delete_user, name='delete_user'),
]
