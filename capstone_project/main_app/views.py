from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from .forms import LoginForm
from .models import Student, Classroom
from .lessons import a,b,c,d,e,f,g,h,i

# Create your views here.

# index view
def index(request):
    return render(request, 'index.html')

# login view
def login_view(request):
    # we can use the same view for multiple HTTP requests
    # this can be done with a simple if statement
    if request.method == 'POST':
        # handle post request
        # we want to authenticate the user with the username and pw
        form = LoginForm(request.POST)
        # validate the form data
        if form.is_valid():
            # get the username and pw and save them to variables
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            # here we use django's built in authenticate method
            user = authenticate(username = u, password = p)
            # if you found a user with matching credentials
            if user is not None:
                # if that user has not been disabled by admin
                if user.is_active:
                    # use django's built in login function
                    login(request, user)
                    return HttpResponseRedirect('/teacher/classroom')
                else:
                    print('the account has been disabled')
            else:
                print('the username or password is incorrect')
    else:
        # the request is a get, we render the login page
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

# logout view
def logout_view(request):
    # print('####### THIS IS THE REQUEST #######')
    # print(request.user)
    logout(request)
    return HttpResponseRedirect('/')

# signup view
def signup_view(request):
    # if the req is a post, then sign them up
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            g = Group.objects.get(name='teacher')
            g.user_set.add(user)
            user.is_staff= True
            user.save()
            login(request, user)
            return HttpResponseRedirect('/user/' + str(user.username))
    # if the req is a get, then show the form
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})


# game view 

def game(request):


    answer = 0

    if request.method == 'POST':
        answer = request.POST['answer']
        print("THIS IS THE REQUEST #############")
        print(request.POST['answer'])
        
    lesson = a 
    n = 0
    
   ## print(lesson)
    print(request)
    return render (request, 'student/game.html', {'lesson' : lesson, 'n': n, 'answer' : answer})






# Teacher View
@user_passes_test(lambda user: user.is_staff)
def teacher_view(request): 
    classrooms = Classroom.objects.all()
    students = Student
    return render (request, 'teacher/classroom.html', {'classrooms': classrooms})


# SELECT * FROM main_app_classroom JOIN main_app_student ON main_app_classroom.id = main_app_student.classroom_id;

# Teacher View classroom
@user_passes_test(lambda user: user.is_staff)
def classroom_show(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    # students = Student.objects.all().select_related(classroom_id)
    # students = Student.objects.all(classroom=classroom_id) # objects.get fails because it returns more than 1
    students = Student.objects.filter(classroom_id = classroom_id)

    print('what is students', students[0].user)

    return render (request, 'teacher/classroom_show.html', { 'classroom': classroom , 'students': students})
