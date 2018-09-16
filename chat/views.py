from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
import json
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from chat.forms import UserForm, StudentForm, IssueForm
from chat.models.student import Student
from chat.models.issue import Issue
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone


def index(request):
    return render(request, 'chat/index.html', {})


def room(request, room_name="helpdesk"):
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_id_list = []
    for session in active_sessions:
        data = session.get_decoded()
        user_id_list.append(data.get('_auth_user_id', None))
        # Query all logged in users based on id list
    online_users = User.objects.filter(id__in=user_id_list)
    issues = Issue.objects.filter(is_complete=False)
    print(issues)
    if request.method == "POST":
        user_id = request.user
        new_issue = json.loads(request.body)['issue']
        issue = Issue(issue_desc=new_issue, user=user_id)
        issue.save()
    return render(request, 'chat/room.html', {
       'room_name_json': mark_safe(json.dumps(room_name)), 'online_users': online_users, 'issues': issues,})

def register(request):
    '''Handles the creation of a new user for authentication

    Method arguments:
    request -- The full HTTP request object
    '''

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        student_form = StudentForm(data=request.POST)

        if user_form.is_valid() and student_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()
            student = student_form.save(commit=False)
            student.user = user
            student.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        return login_user(request)

    elif request.method == 'GET':
        user_form = UserForm()
        student_form = StudentForm()
        template_name = 'register.html'
        return render(request, template_name, {'user_form': user_form, 'student_form': student_form})


def login_user(request):
    '''Handles the creation of a new user for authentication

    Method arguments:
    request -- The full HTTP request object
    '''

    # Obtain the context for the user's request.
    context = RequestContext(request)

    # Stores the path the users were trying to get to originally if its different or takes them to the home screen
    next = request.GET.get('next') or '/chat'
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':

        # Use the built-in authenticate method to verify
        username=request.POST['username']
        password=request.POST['password']
        authenticated_user = authenticate(username=username, password=password)

        # If authentication was successful, log the user in
        if authenticated_user is not None:
            login(request=request, user=authenticated_user)
            return HttpResponseRedirect("/chat/helpdesk")

        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {}, {}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
            #Renders the page via the login.html template and stores the next variable
            return render(request, 'login.html', {'next': next})




# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage. Is there a way to not hard code
    # in the URL in redirects?????
    return HttpResponseRedirect('/chat')

