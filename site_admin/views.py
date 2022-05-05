from quizapp import settings
from users import views
from users.models import Users, Quizzes, Questions, Results, Feedbacks, Notifications
from users.tokens import generate_token
from .forms import AddQuizForm, AddFeedbackReply, UpdateFeedbackReply

from django.shortcuts import redirect, render, get_object_or_404
from django.core.mail import send_mail, EmailMessage
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.forms import modelformset_factory, inlineformset_factory
from datetime import datetime

# Create your views here.
global current_year
current_year = datetime.now().year

@login_required(login_url='home')
def admin_dashboard(request, name):
    current_user = User.objects.get(pk=request.user.id)
    if current_user.is_superuser == True:
        role = 'admin'
        notification = Notifications.objects.filter(to=role, status=1)
        feedcount = 0
        resultcount = 0
        usercount = 0
        for item in notification:
            if item.subject == 'feedback':
                feedcount += 1
            elif item.subject == 'result':
                resultcount += 1
            elif item.subject == 'new_user':
                usercount += 1
        all_quizzes = Quizzes.objects.all
        return render(request, 'admin/admin_dashboard.html', {'role':role, 'feedcount':feedcount, 'resultcount':resultcount, 'usercount':usercount, 'current_year': current_year, 'all': all_quizzes, 'uname':name,})
    else:
        return redirect('home')

@login_required(login_url='home')
def add_quiz(request, name):
    current_user = User.objects.get(pk=request.user.id)
    if current_user.is_superuser == True:
        role = 'admin'
        notification = Notifications.objects.filter(to=role, status=1)
        feedcount = 0
        resultcount = 0
        usercount = 0
        for item in notification:
            if item.subject == 'feedback':
                feedcount += 1
            elif item.subject == 'result':
                resultcount += 1
            elif item.subject == 'new_user':
                usercount += 1
        date = datetime.now().strftime('%Y-%m-%d')
        if request.method == 'POST':
            quizform = AddQuizForm(request.POST or None)
            if quizform.is_valid():
                quizform.save()
                messages.success(request, "Quiz added sucessfully.")
                return redirect('admin_dashboard', name)
        else:
            return render(request, 'admin/add_quiz.html', {'role':role, 'feedcount':feedcount, 'resultcount':resultcount, 'usercount':usercount, 'current_year': current_year, 'date': date, 'uname': name})
    else:
        return redirect('home')

@login_required(login_url='home')
def result_notify(request, name):
    Notifications.objects.filter(to='admin', subject='result', status=1).update(status=0)
    return redirect('view_results', name)

@login_required(login_url='home')
def view_results(request, name):
    current_user = User.objects.get(pk=request.user.id)
    if current_user.is_superuser == True:
        if request.method == 'POST':
            uid = request.POST['uid']
            qid = request.POST['qid']
            user = Users.objects.get(pk=uid)
            token = generate_token.make_token(user)
            user_id = urlsafe_base64_encode(force_bytes(uid))
            quiz_id = urlsafe_base64_encode(force_bytes(qid))
            return redirect('generate_result', user_id, quiz_id, token)
        else:
            role = 'admin'
            notification = Notifications.objects.filter(to=role, status=1)
            feedcount = 0
            resultcount = 0
            usercount = 0
            for item in notification:
                if item.subject == 'feedback':
                    feedcount += 1
                elif item.subject == 'result':
                    resultcount += 1
                elif item.subject == 'new_user':
                    usercount += 1
            results = Results.objects.all
            return render(request, 'admin/view_results.html', {'role':role, 'feedcount':feedcount, 'resultcount':resultcount, 'usercount':usercount, 'current_year': current_year, 'uname':name, 'results':results,})
    else:
        return redirect('home')

@login_required(login_url='home')
def delete_result(request, id, name):
    current_user = User.objects.get(pk=request.user.id)
    if current_user.is_superuser == True:
        result = Results.objects.get(pk=id)
        uid = result.user_id.id
        qid = result.quiz_id.id
        quiz = Quizzes.objects.get(pk=qid)
        candidate = get_object_or_404(Users, id=uid)
        quiz.attendees.remove(candidate)
        result.delete()
        messages.success(request, "Result deleted successfully.")
        return redirect('view_results', name)
    else:
        return redirect('home')

# question_count = 0
@login_required(login_url='home')
def add_update_questions(request, qid, name):
    current_user = User.objects.get(pk=request.user.id)
    if current_user.is_superuser == True:
        role = 'admin'
        notification = Notifications.objects.filter(to=role, status=1)
        feedcount = 0
        resultcount = 0
        usercount = 0
        for item in notification:
            if item.subject == 'feedback':
                feedcount += 1
            elif item.subject == 'result':
                resultcount += 1
            elif item.subject == 'new_user':
                usercount += 1
        # global question_count
        quiz = Quizzes.objects.get(pk=qid)
        tot = quiz.tot_questions
        QuestionFormset = inlineformset_factory(Quizzes, Questions, fields=('question_no', 'question', 'option1', 'option2', 'option3', 'option4', 'answer'), can_delete=False, extra=1, max_num=tot)
        if request.method == 'POST':
            formset = QuestionFormset(request.POST, instance=quiz)
            if formset.is_valid():
                formset.save()
                if request.session.has_key('q_count'):
                    question_count = request.session['q_count']
                else:
                    question_count = 0
                question_count += 1
                if question_count >= tot:
                    messages.success(request, 'Questions and details added sucessfully.')
                    del request.session['q_count']
                    return redirect('admin_dashboard', name)
                else:
                    del request.session['q_count']
                    request.session['q_count'] = question_count
                    # messages.success(request, 'Question '+str(question_count)+' added sucessfully.')
                    return redirect('add_update_questions', qid=quiz.id, name=name)
        else:
            formset = QuestionFormset(instance=quiz)
            if not request.session.has_key('q_count'):
                request.session['q_count'] = 0
            return render(request, 'admin/questions.html', {'role':role, 'feedcount':feedcount, 'resultcount':resultcount, 'usercount':usercount, 'current_year': current_year, 'id':int(qid), 'uname':name, 'formset':formset, })
    else:
        return redirect('home')

@login_required(login_url='home')
def delete_quiz(request, id, name):
    current_user = User.objects.get(pk=request.user.id)
    if current_user.is_superuser == True:
        quiz = Quizzes.objects.get(pk=id)
        quiz.delete()
        messages.success(request, "Quiz deleted successfully.")
        return redirect('admin_dashboard', name)
    else:
        return redirect('home')

@login_required(login_url='home')
def update_quiz(request, id, name):
    current_user = User.objects.get(pk=request.user.id)
    if current_user.is_superuser == True:
        role = 'admin'
        notification = Notifications.objects.filter(to=role, status=1)
        feedcount = 0
        resultcount = 0
        usercount = 0
        for item in notification:
            if item.subject == 'feedback':
                feedcount += 1
            elif item.subject == 'result':
                resultcount += 1
            elif item.subject == 'new_user':
                usercount += 1
        date = datetime.now().strftime('%Y-%m-%d')
        if request.method == 'POST':
            instance = get_object_or_404(Quizzes, id=id)
            quizform = AddQuizForm(request.POST or None, instance=instance)
            if quizform.is_valid():
                quizform.save()
                messages.success(request, "Quiz Updated sucessfully.")
                return redirect('admin_dashboard', name)
        else:
            quiz = Quizzes.objects.get(pk=id)
            return render(request, 'admin/update_quiz.html', {'role':role, 'feedcount':feedcount, 'resultcount':resultcount, 'usercount':usercount, 'current_year': current_year, 'date': date, 'uname': name, 'quiz':quiz, 'id':id})
    else:
        return redirect('home')

@login_required(login_url='home')
def user_notify(request, name):
    Notifications.objects.filter(to='admin', subject='new_user', status=1).update(status=0)
    return redirect('view_users', name)

@login_required(login_url='home')
def view_users(request, name):
    current_user = User.objects.get(pk=request.user.id)
    if current_user.is_superuser == True:
        role = 'admin'
        notification = Notifications.objects.filter(to=role, status=1)
        feedcount = 0
        resultcount = 0
        usercount = 0
        for item in notification:
            if item.subject == 'feedback':
                feedcount += 1
            elif item.subject == 'result':
                resultcount += 1
            elif item.subject == 'new_user':
                usercount += 1
        all_users = Users.objects.all
        return render(request, 'admin/view_users.html', {'role':role, 'feedcount':feedcount, 'resultcount':resultcount, 'usercount':usercount, 'current_year': current_year, 'all': all_users, 'uname':name})
    else:
        return redirect('home')

@login_required(login_url='home')
def delete_user(request, id, name):
    current_user = User.objects.get(pk=request.user.id)
    if current_user.is_superuser == True:
        user = Users.objects.get(pk=id)
        auth_user = User.objects.get(email=user.email)
        user.delete()
        auth_user.delete()
        messages.success(request, "User removed successfully.")
        return redirect('view_users', name)
    else:
        return redirect('home')

@login_required(login_url='home')
def feed_notify(request, name):
    Notifications.objects.filter(to='admin', subject='feedback', status=1).update(status=0)
    return redirect('view_feedbacks', name)

@login_required(login_url='home')
def view_feedbacks(request, name):
    current_user = User.objects.get(pk=request.user.id)
    if current_user.is_superuser == True:
        role = 'admin'
        notification = Notifications.objects.filter(to=role, status=1)
        feedcount = 0
        resultcount = 0
        usercount = 0
        for item in notification:
            if item.subject == 'feedback':
                feedcount += 1
            elif item.subject == 'result':
                resultcount += 1
            elif item.subject == 'new_user':
                usercount += 1
        feedbacks = Feedbacks.objects.all
        if request.method == 'POST':
            if 'update_reply' in request.POST:
                instance = get_object_or_404(Feedbacks, id=request.POST['id'])
                user = Users.objects.get(pk=request.POST['user_id'])
                date = request.POST['date']
                reply = request.POST['reply']
                update_reply_form = UpdateFeedbackReply(request.POST or None, instance=instance)
                if update_reply_form.is_valid():
                    update_reply_form.save()
                    notify = Notifications(to=request.POST['user_id'], subject='reply', status=1)
                    notify.save()
                    # Revised reply Mail
                    subject = "Reply for Revised Feedback"
                    message = "Hello " + user.fname + " !! \n" + "This is the reply for your feedback dated "+ date +".\n\n"+ reply +".\n\nRegards,\nQUIZ APP Administrator"
                    from_email = settings.EMAIL_HOST_USER
                    to_list = [user.email]
                    send_mail(subject, message, from_email, to_list, fail_silently=False)
                    messages.success(request, "Reply edited successfully")
                    return redirect('view_feedbacks', name)
                else:
                    messages.success(request, "Error")
                    return redirect('view_feedbacks', name)
            elif 'edit_reply' in request.POST:
                feed_id = int(request.POST['id'])
                mode = 'edit'
                return render(request, 'admin/view_feedbacks.html', {'role':role, 'feedcount':feedcount, 'resultcount':resultcount, 'usercount':usercount, 'current_year': current_year, 'uname':name, 'feedbacks': feedbacks, 'feed_id':feed_id, 'mode':mode,})
            else:
                user = Users.objects.get(pk=request.POST['user_id'])
                date = request.POST['date']
                reply = request.POST['reply']
                
                instance = get_object_or_404(Feedbacks, id=request.POST['feed_id'])
                replyform = AddFeedbackReply(request.POST or None, instance=instance)
                if replyform.is_valid():
                    replyform.save()
                    notify = Notifications(to=request.POST['user_id'], subject='reply', status=1)
                    notify.save()
                    # Reply Mail
                    subject = "Reply for Feedback"
                    message = "Hello " + user.fname + " !! \n" + "This is the reply for your feedback dated "+ date +".\n\n"+ reply +".\n\nRegards,\nQUIZ APP Administrator"
                    from_email = settings.EMAIL_HOST_USER
                    to_list = [user.email]
                    send_mail(subject, message, from_email, to_list, fail_silently=True)
                    messages.success(request, "Reply send successfully")
                    return redirect('view_feedbacks', name)
                else:
                    messages.error(request, "Some error")
                    return redirect('view_feedbacks', name)
        return render(request, 'admin/view_feedbacks.html', {'role':role, 'feedcount':feedcount, 'resultcount':resultcount, 'usercount':usercount, 'current_year': current_year, 'uname':name, 'feedbacks': feedbacks,})
    else:
        return redirect('home')
