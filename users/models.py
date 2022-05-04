from django.db import models

# Create your models here.

class Users(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.fname+ ' ' +self.lname

class Quizzes(models.Model):
    title = models.CharField('Quiz Title', max_length=100)
    tot_questions = models.IntegerField()
    mark_for_correct = models.FloatField()
    mark_for_wrong = models.FloatField()
    max_time = models.IntegerField()
    max_mark = models.IntegerField()
    date_added = models.DateField('Date Added')
    attendees = models.ManyToManyField(Users, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('-date_added',)

class Questions(models.Model):
    choices = (
        ('', 'Select'),
        ('option1', 'Option 1'),
        ('option2', 'Option 2'),
        ('option3', 'Option 3'),
        ('option4', 'Option 4'),
    )

    quiz_id = models.ForeignKey(Quizzes, blank=False, null=False, on_delete=models.CASCADE)
    question_no = models.IntegerField(default=0)
    question = models.TextField(blank=False)
    option1 = models.CharField('Option 1', max_length=200, blank=False)
    option2 = models.CharField('Option 2', max_length=200, blank=False)
    option3 = models.CharField('Option 3', max_length=200, blank=False)
    option4 = models.CharField('Option 4', max_length=200, blank=False)
    answer = models.CharField(max_length=200, choices=choices, blank=False, default='Select')

    def __str__(self):
        return str(self.quiz_id)+' -'+' question '+str(self.question_no)


class Results(models.Model):
    quiz_id = models.ForeignKey(Quizzes, blank=False, null=False, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Users, blank=False, null=False, on_delete=models.CASCADE)
    candidate_id = models.CharField('Candidate Id', max_length=100)
    score = models.FloatField()
    max_mark = models.IntegerField()
    tot_questions =models.IntegerField()
    correct_answers = models.IntegerField()
    wrong_answers = models.IntegerField()
    date = models.DateField('Date Attended')
    
    def __str__(self):
        return str(self.user_id)+ ' - ' +str(self.quiz_id)
    
    class Meta:
        ordering = ('-date',)


class Feedbacks(models.Model):
    user_id = models.ForeignKey(Users, blank=False, null=False, on_delete=models.CASCADE)
    user_name = models.CharField('Full Name', max_length=100, blank=False)
    feedback = models.TextField(blank=False)
    status = models.CharField('Status', max_length=10, blank=True)
    reply = models.TextField(blank=True)
    reply_status = models.CharField('Reply Status', max_length=10, blank=True)
    date = models.DateField('Date Posted')

    def __str__(self):
        return self.user_name
    
    class Meta:
        ordering = ('-date',)

class Notifications(models.Model):
    to = models.CharField('To', max_length=10)
    subject = models.CharField('Subject', max_length=50)
    status = models.IntegerField()

    def __str__(self):
        return self.subject
