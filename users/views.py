from quizapp import settings
from site_admin import views
from . tokens import generate_token
from .forms import UsersForm, ActivateForm, UserPassUpdateForm, AddFeedbackForm, UpdateFeedback, CaptchaForm
from .models import Users, Quizzes, Questions, Results, Feedbacks, Notifications, QuizLogs

from django.core.mail import send_mail, EmailMessage
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.forms import modelformset_factory, inlineformset_factory
from django.template.loader import render_to_string
from datetime import datetime

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views.generic import View
from xhtml2pdf import pisa

# Create your views here.
global current_year
current_year = datetime.now().year

def home(request):
    feedbacks = Feedbacks.objects.all

    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_superuser == True:
                login(request, user)
                uname = user.first_name
                return redirect('admin_dashboard', uname)    
            else:
                login(request, user)
                request.session['uid'] = user.id
                fname = user.first_name
                users = Users.objects.get(email=user.email)
                uid = urlsafe_base64_encode(force_bytes(users.id))
                return redirect('user_dashboard', fname, uid)
        else:
            messages.error(request, "Bad Credentials or maybe account not activated.")
            return redirect('home')
    return render(request, 'home.html', {'current_year': current_year, 'feedbacks':feedbacks,})

def contact(request):
    return redirect('home')

def forgot_password(request):
    if request.method == 'POST':
        username = request.POST['uname']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
            
        if user != None:
            # Reset mail
            current_site = get_current_site(request)
            email_sub = "Reset Password"
            message = render_to_string("users/reset_pass_mail.html",{
                'user' : user.first_name,
                'domain' : current_site.domain,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : generate_token.make_token(user),
            })
            email = EmailMessage(
                email_sub,
                message,
                settings.EMAIL_HOST_USER,
                [user.email],
            )
            email.fail_silently=True
            email.send()
            messages.success(request, "Password reset link has been sent. Please check your mail")
            return redirect('forgot_password')
        else:
            messages.error(request, "Username doesn't match any accounts.")
            return redirect('forgot_password')
    else:
        return render(request, 'forgot_pass.html', {'current_year': current_year})

def reset_password(request, uid64, token):
    if request.method == 'POST':
        uid =force_str(urlsafe_base64_decode(uid64))
        passwd = request.POST['password']
        cpasswd = request.POST['cpassword']
        is_alpha = False
        is_num = False
        is_upper = False
        is_lower = False
        is_special = False

        for x in passwd:
            if x.isalpha():
                is_alpha = True
                if x.isupper() and is_upper == False:
                    is_upper = True
                elif x.islower() and is_lower == False:
                    is_lower = True
            elif x.isnumeric() and is_num == False:
                is_num = True

        if len(passwd)<8:
            messages.error(request, "Password should have atleast 8 characters.")
            return redirect('reset_password', uid64, token)
        elif is_alpha != True or is_num != True or is_upper != True or is_lower != True:
            messages.error(request, "Password must be a combination of upper case, lower case letters and numbers.")
            return redirect('reset_password', uid64, token)
        elif passwd != cpasswd:
            messages.error(request, "Passwords not matching !")
            return redirect('reset_password', uid64, token)
        else:
            instance = get_object_or_404(User, id=uid)
            captcha = CaptchaForm(request.POST)
            if captcha.is_valid():
                form = UserPassUpdateForm(request.POST or None, instance=instance)
                if form.is_valid():
                    user = form.save()
                    user.set_password(passwd)
                    user.save()
                    messages.success(request, "Password reseted successfully. Try login.")
                    return redirect('home')
                else:
                    messages.error(request, "Something went wrong. Try again.")
                    return redirect('reset_password', uid64, token)
            else:
                messages.error(request, "Wrong Captcha")
                return redirect('reset_password', uid64, token)
    else:
        try:
            uid =force_str(urlsafe_base64_decode(uid64))
            myuser = User.objects.get(pk=uid)
            cap_form = CaptchaForm()
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            myuser = None
        
        if myuser is not None and generate_token.check_token(myuser, token):
            return render(request, 'users/reset_pass.html', {'current_year':current_year, 'uid':uid64, 'token':token, 'form':cap_form,})
    

def signout(request):
    logout(request)
    if request.session.has_key('uid'):
        del request.session['uid']
    messages.success(request, "Logged out succcessfully")
    return redirect('home')

def signup(request):
    if request.method == 'POST':
        username = request.POST['uname']
        firstname = request.POST['fname']
        lastname = request.POST['lname']
        email = request.POST['email']
        passwd = request.POST['password']
        cpasswd = request.POST['cpassword']
        is_alpha = False
        is_num = False
        is_upper = False
        is_lower = False
        is_special = False

        for x in passwd:
            if x.isalpha():
                is_alpha = True
                if x.isupper() and is_upper == False:
                    is_upper = True
                elif x.islower() and is_lower == False:
                    is_lower = True
            elif x.isnumeric() and is_num == False:
                is_num = True

        if User.objects.filter(username=username):
            messages.error(request, "Username already exists. Please use another one.")
            return redirect('signup')
        elif len(username)>10:
            messages.error(request, "Username cannot be more than 10 characters.")
            return redirect('signup')
        elif Users.objects.filter(email=email):
            messages.error(request, "Email already registered. Please use another one.")
            return redirect('signup')
        elif len(passwd)<8:
            messages.error(request, "Password should have atleast 8 characters.")
            return redirect('signup')
        elif is_alpha != True or is_num != True or is_upper != True or is_lower != True:
            messages.error(request, "Password must be a combination of upper case, lower case letters and numbers.")
            return redirect('signup')
        elif passwd != cpasswd:
            messages.error(request, "Passwords not matching !")
            return redirect('signup')
        else:
            captcha = CaptchaForm(request.POST)
            if captcha.is_valid():
                form = UsersForm(request.POST or None)
                if form.is_valid():
                    form.save()
                    notify = Notifications(to='admin', subject='new_user', status=1)
                    notify.save()
                    myuser = User.objects.create_user(username, email, passwd)
                    myuser.first_name = firstname
                    myuser.last_name = lastname
                    myuser.is_active = False
                    myuser.save()
                    messages.success(request, "Your Account has been successfully created. We've send you a\
                    confirmation email. Please confirm your email inorder to activate your account.")
            
                    # Welcome Email
                    subject = "Welcome to Quiz App"
                    message = "Hello " + myuser.first_name + " !! \n" + "Welcome to Quiz App ! \nThank you for visting our website.\nWe've send you a confirmation email. Please confirm your email id inorder to activate your account.\n\nRegards,\nQUIZ APP Administrator"
                    from_email = settings.EMAIL_HOST_USER
                    to_list = [myuser.email]
                    send_mail(subject, message, from_email, to_list, fail_silently=True)

                    # Confirmation Email
                    current_site = get_current_site(request)
                    email_sub = "Confirm your Email"
                    message1 = render_to_string("users/email_confirmation.html",{
                        'user' : myuser.first_name,
                        'domain' : current_site.domain,
                        'uid' : urlsafe_base64_encode(force_bytes(myuser.pk)),
                        'token' : generate_token.make_token(myuser),
                    })
                    email = EmailMessage(
                        email_sub,
                        message1,
                        settings.EMAIL_HOST_USER,
                        [myuser.email],
                    )
                    email.fail_silently=True
                    email.send()

                    return redirect('home')
            else:
                messages.error(request, "Wrong Captcha")
                return redirect('signup')
    else:
        cap_form = CaptchaForm()
        return render(request, 'signup.html', {'current_year': current_year, 'form':cap_form,})

def activate(request, uid64, token):
    try:
        uid =force_str(urlsafe_base64_decode(uid64))
        myuser = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None
    
    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        activate = Users.objects.get(email=myuser.email)
        activate.status = 'activated'
        activate.save()
        messages.success(request, "Account activated successfully. You can now login.")        
        return redirect('home')
    else:
        return render(request, 'users/activation_failed.html')

def feedbacks(request):
    feedbacks = Feedbacks.objects.all
    return render(request, 'user_feedbacks.html', {'current_year': current_year, 'feedbacks': feedbacks,})

@login_required(login_url='home')
def user_dashboard(request, name, id64):
    if request.session.has_key('uid'):
        role = 'user'
        id = force_str(urlsafe_base64_decode(id64))
        notification = Notifications.objects.filter(to=id, status=1)
        replycount = 0
        for item in notification:
            if item.subject == 'reply':
                replycount += 1
        if request.session.has_key('user'):
            del request.session['user']
        user = Users.objects.get(pk=id)
        user_inst = get_object_or_404(Users, id=id)
        uid = urlsafe_base64_encode(force_bytes(id))
        fullname = user.fname+' '+user.lname
        quizzes = Quizzes.objects.all
        return render(request, 'users/user_dashboard.html', {'role':role, 'replycount':replycount, 'name':name, 'current_year': current_year, 'user_id':uid, 'user':user_inst, 'fname':name, 'fullname':fullname, 'quizzes':quizzes,})
    else:
        return redirect('home')

@login_required(login_url='home')
def instructions(request, user_id, quiz_id):
    if request.session.has_key('uid'):
        role = 'user'
        uid = force_str(urlsafe_base64_decode(user_id))
        notification = Notifications.objects.filter(to=uid, status=1)
        replycount = 0
        for item in notification:
            if item.subject == 'reply':
                replycount += 1
        qid = urlsafe_base64_encode(force_bytes(quiz_id))
        quiz = Quizzes.objects.get(pk=quiz_id)
        user = Users.objects.get(pk=uid)
        current_site = get_current_site(request)
        domain = current_site.domain
        request.session['user'] = user_id
        user_inst = get_object_or_404(Users, id=uid)
        if user_inst in quiz.attendees.all():
            return redirect('user_dashboard', user.fname, user_id)
        else:
            return render(request, 'users/instructions.html', {'role':role, 'replycount':replycount, 'name':user.fname, 'current_year': current_year, 'user_id':user_id, 'quiz_id':qid, 'domain':domain, 'quiz':quiz,})
    else:
        return redirect('home')

@login_required(login_url='home')
def attempt(request, user_id, quiz_id):
    if request.session.has_key('user'):
        
        if not request.session.has_key('qst_no'):
            request.session['qst_no'] = 1
        question_number = request.session['qst_no']
        
        if not request.session.has_key('score'):
            request.session['score'] = 0
        score = request.session['score']
        
        if not request.session.has_key('cor_ans'):
            request.session['cor_ans'] = 0
        correct_answers = request.session['cor_ans']
        
        if not request.session.has_key('wr_ans'):
            request.session['wr_ans'] = 0
        wrong_answers = request.session['wr_ans']

        uid = force_str(urlsafe_base64_decode(user_id))
        qid = force_str(urlsafe_base64_decode(quiz_id))
        user = Users.objects.get(pk=uid)
        quiz = Quizzes.objects.get(pk=qid)
        tot_questions = quiz.tot_questions
        max_mark = quiz.max_mark
        time = quiz.max_time/tot_questions
        date = datetime.now().strftime('%Y-%m-%d')
        candidate_id = datetime.now().strftime('%Y%m%d')+qid+uid

        if request.method == 'POST':
            if request.POST.get('answer', False):
                answer = request.POST.get('answer', False)
                logs = QuizLogs.objects.create(candidate_id=candidate_id, question_no=question_number, selected_option=answer)
                logs.save()
                check = Questions.objects.get(quiz_id=qid, question_no=question_number)
                if check.answer == answer:
                    correct_answers += 1
                    del request.session['cor_ans']
                    request.session['cor_ans'] = correct_answers
                    
                    score += quiz.mark_for_correct
                    del request.session['score']
                    request.session['score'] = score
                else:
                    wrong_answers += 1
                    del request.session['wr_ans']
                    request.session['wr_ans'] = wrong_answers
                    
                    score += quiz.mark_for_wrong
                    del request.session['score']
                    request.session['score'] = score
            else:
                logs = QuizLogs.objects.create(candidate_id=candidate_id, question_no=question_number, selected_option='NA')
                logs.save()
            if question_number < tot_questions:
                question_number += 1
                del request.session['qst_no']
                request.session['qst_no'] = question_number
                questions = Questions.objects.get(quiz_id=qid, question_no=question_number)
                return render(request, 'users/attempt_quiz.html', {'current_year': current_year, 'user_id':user_id, 'quiz_id':quiz_id, 'candidate_id':candidate_id, 'question':questions, 'q_time':time,})
            else:
                result = Results.objects.create(quiz_id =quiz, user_id=user, candidate_id=candidate_id, score=score, max_mark=max_mark, tot_questions=tot_questions, correct_answers=correct_answers, wrong_answers=wrong_answers, date=date)
                result.save()
                notify = Notifications(to='admin', subject='result', status=1)
                notify.save()
                del request.session['score']
                del request.session['cor_ans']
                del request.session['wr_ans']
                del request.session['qst_no']
                # Result mail
                current_site = get_current_site(request)
                email_sub = "Quiz Result"
                message = render_to_string("users/result_mail.html",{
                    'user' : user.fname,
                    'domain' : current_site.domain,
                    'uid' : user_id,
                    'qid' : quiz_id,
                    'token' : generate_token.make_token(user),
                })
                email = EmailMessage(
                    email_sub,
                    message,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                )
                email.fail_silently=True
                email.send()
                candidate = get_object_or_404(Users, id=uid)
                quiz.attendees.add(candidate)
                cand_id = urlsafe_base64_encode(force_bytes(candidate_id))
                return redirect('view_logs', user_id, quiz_id, cand_id, 'user')
                # return redirect('add_feedback', user_id)
        else:
            questions = Questions.objects.get(quiz_id=qid, question_no=question_number)
            return render(request, 'users/attempt_quiz.html', {'current_year': current_year, 'user_id':user_id, 'quiz_id':quiz_id, 'candidate_id':candidate_id, 'question':questions, 'q_time':time,})
    else:
        uid = force_str(urlsafe_base64_decode(user_id))
        user = Users.objects.get(pk=uid)
        return redirect('user_dashboard', user.fname, user_id)

@login_required(login_url='home')
def view_logs(request, user_id, quiz_id, cand_id, mode='user'):
    if mode == 'admin':
        logs = QuizLogs.objects.filter(candidate_id=cand_id)
        if logs:
            uid = urlsafe_base64_encode(force_bytes(user_id))
            questions = Questions.objects.filter(quiz_id=quiz_id)    
            return render(request, 'users/view_logs.html', {'current_year': current_year, 'user_id':uid, 'candidate_id': cand_id, 'questions': questions, 'logs': logs, 'mode': mode})
        else:
            HttpResponse("Not Found")
    else:
        cid = force_str(urlsafe_base64_decode(cand_id))
        logs = QuizLogs.objects.filter(candidate_id=cid)
        if logs:
            qid = force_str(urlsafe_base64_decode(quiz_id))
            questions = Questions.objects.filter(quiz_id=qid)    
            return render(request, 'users/view_logs.html', {'current_year': current_year, 'user_id':user_id, 'candidate_id': cid, 'questions': questions, 'logs': logs, 'mode': mode})
        else:
            HttpResponse("Not Found")

@login_required(login_url='home')
def add_feedback(request, user_id, rtype='manual'):
    if request.session.has_key('uid'):
        role = 'user'
        uid = force_str(urlsafe_base64_decode(user_id))
        notification = Notifications.objects.filter(to=uid, status=1)
        replycount = 0
        for item in notification:
            if item.subject == 'reply':
                replycount += 1
        if request.session.has_key('user'):
            rtype = 'auto'
            del request.session['user']
        user = Users.objects.get(pk=uid)
        fullname = user.fname+ ' ' +user.lname
        date = datetime.now().strftime('%Y-%m-%d')

        if request.method == 'POST': 
            form = AddFeedbackForm(request.POST or None)
            if form.is_valid():
                form.save()
                notify = Notifications(to='admin', subject='feedback', status=1)
                notify.save()
                return redirect('user_dashboard', user.fname, user_id)
        return render(request, 'users/add_feedback.html',{'role':role, 'replycount':replycount, 'name':user.fname, 'rtype':rtype, 'current_year': current_year, 'user_id':user_id, 'uid':uid, 'fullname':fullname, 'date':date,})
    else:
        return redirect('home')

@login_required(login_url='home')
def reply_notify(request, user_id):
    if request.session.has_key('uid'):
        uid = force_str(urlsafe_base64_decode(user_id))
        Notifications.objects.filter(to=uid, subject='reply', status=1).update(status=0)
        return redirect('user_view_feedbacks', user_id)
    else:
        return redirect('home')

@login_required(login_url='home')
def user_view_feedbacks(request, user_id):
    if request.session.has_key('uid'):
        role = 'user'
        uid = force_str(urlsafe_base64_decode(user_id))
        notification = Notifications.objects.filter(to=uid, status=1)
        replycount = 0
        for item in notification:
            if item.subject == 'reply':
                replycount += 1
        user = Users.objects.get(pk=uid)
        feedbacks = Feedbacks.objects.all().filter(user_id=uid)
        if request.method == 'POST':
            feed_id = int(request.POST['id'])
            mode = 'edit'
            date = datetime.now().strftime('%Y-%m-%d')
            return render(request, 'users/user_view_feedbacks.html', {'role':role, 'replycount':replycount, 'name':user.fname, 'current_year': current_year, 'user_id':user_id, 'feedbacks':feedbacks, 'feed_id':feed_id, 'mode':mode, 'date':date,})
        else:
            return render(request, 'users/user_view_feedbacks.html', {'role':role, 'replycount':replycount, 'name':user.fname, 'current_year': current_year, 'user_id':user_id, 'feedbacks':feedbacks})
    else:
        return redirect('home')

@login_required(login_url='home')
def update_feedback(request, user_id, feed_id):
    if request.session.has_key('uid'):
        role = 'user'
        uid = force_str(urlsafe_base64_decode(user_id))
        notification = Notifications.objects.filter(to=uid, status=1)
        replycount = 0
        for item in notification:
            if item.subject == 'reply':
                replycount += 1
        user = Users.objects.get(pk=uid)
        feedbacks = Feedbacks.objects.all().filter(user_id=uid)
        if request.method == 'POST':
            instance = get_object_or_404(Feedbacks, id=request.POST['id'])
            updateform = UpdateFeedback(request.POST or None, instance=instance)
            if updateform.is_valid():
                updateform.save()
                notify = Notifications(to='admin', subject='feedback', status=1)
                notify.save()
                messages.success(request, "Feedback edited successfully")
                return redirect('user_view_feedbacks', user_id)
            else:
                messages.error(request, "Something went wrong")
                return redirect('add_feedbacks', user_id)
        else:
            return render(request, 'users/user_view_feedbacks.html', {'role':role, 'replycount':replycount, 'name':user.fname, 'current_year': current_year, 'user_id':user_id, 'feedbacks':feedbacks})
    else:
        return redirect('home')

def delete_feedback(request, user_id, feed_id):
    feedback = Feedbacks.objects.get(pk=feed_id)
    feedback.delete()
    messages.success(request, "Feedback deleted successfully.")
    return redirect('user_view_feedbacks', user_id)

@login_required(login_url='home')
def user_view_results(request, user_id):
    if request.session.has_key('uid'):
        role = 'user'
        uid = force_str(urlsafe_base64_decode(user_id))
        user = Users.objects.get(pk=uid)
        notification = Notifications.objects.filter(to=uid, status=1)
        replycount = 0
        for item in notification:
            if item.subject == 'reply':
                replycount += 1
        if request.method == 'POST':
            candidate_id = request.POST['candidate_id']
            quiz_str = request.POST['quiz'].split('-', 1) 
            title = quiz_str[0]
            # eg: "April 22, 2022"
            date_str = quiz_str[1].split(',', 1)
            # eg: "April 22" " 2022"
            date_str1 = date_str[0].split(' ', 1)
            # eg: "April" "22"
            month = date_str1[0]
            str_date = month[0:3]+" "+date_str1[1]+date_str[1]
            # eg: "April 22 2022"
            date = datetime.strptime(str_date, '%b %d %Y')
            quiz = Quizzes.objects.get(title=title, date_added=date)
            try:
                result = Results.objects.get(quiz_id=quiz.id, candidate_id=candidate_id)
            except Results.DoesNotExist:
                result = None
            if result != None:
                token = generate_token.make_token(user)
                user_id = urlsafe_base64_encode(force_bytes(result.user_id.id))
                quiz_id = urlsafe_base64_encode(force_bytes(result.quiz_id.id))
                return redirect('generate_result', user_id, quiz_id, token)            
            else:
                messages.error(request, "Candidate Id not matching with the selected quiz.")
                return redirect('user_view_results', user_id)
        else:
            quizzes = Quizzes.objects.all()
            return render(request, 'users/user_view_results.html', {'role':role, 'replycount':replycount, 'current_year': current_year, 'user_id':user_id, 'name':user.fname, 'quizzes':quizzes})
    else:
        return redirect('home')

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def generate_result(request, user_id, quiz_id, token, *args, **kwargs):
    try:
        uid = force_str(urlsafe_base64_decode(user_id))
        user = Users.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and generate_token.check_token(user, token):
        qid = force_str(urlsafe_base64_decode(quiz_id))
        quiz = Quizzes.objects.get(pk=qid)
        result = Results.objects.get(user_id=uid, quiz_id=qid)        
        if result:
            percent = (result.score / result.max_mark) * 100
            if 100 <= percent > 90:
                grade = 'A+'
            elif 90 <= percent > 80:
                grade = 'A'
            elif 80 <= percent > 70:
                grade = 'B+'
            elif 70 <= percent > 60:
                grade = 'B'
            elif 60 <= percent > 50:
                grade = 'C+'
            elif 50 <= percent > 40:
                grade = 'C'
            elif 40 <= percent > 30:
                grade = 'D+'
            elif percent == 30:
                grade = 'D'
            elif percent < 30:
                grade = 'E'
            
            data = {
                'title': quiz.title,
                'qdate': quiz.date_added,
                'name': user.fname+' '+user.lname,
                'candidate_id': result.candidate_id,
                'score': result.score,
                'max_mark': result.max_mark,
                'grade': grade,
                'tot_questions': result.tot_questions,
                'correct_answers': result.correct_answers,
                'wrong_answers': result.wrong_answers,
                'date': result.date,
                'current_year': current_year,
            }
            pdf = render_to_pdf('users/result.html', data)
            if pdf:
                return HttpResponse(pdf, content_type='application/pdf')
            else:
                return HttpResponse('Not found1')
        else:
            return HttpResponse('Not found2')
    else:
        return HttpResponse('Not found3')
