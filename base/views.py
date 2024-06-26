from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from .models import Space, Topic, Message,User # we imported the model we want to query
from .forms import Spaceform, Userform, My_usercreationForm

#paces = [
#    {"id":"1", "name":"GENERATIVE AI ART."},
#    {"id":"2", "name":"BACKEND ENGINEER WORKFLOW."},
 #   {"id":"3", "name":"GROWING YOUR TECH NETWORK."},
 #   {"id":"4", "name":"GETTING YOUR DREAM TECH JOB."}
#]



# Create your views here. 

def login_page(request):
    page = "login"
    if request.user.is_authenticated: # made sure user can't go to the login page through the url if authenticated
        return redirect("home")
    
    if request.method == "POST": # functionality of this function starts here
        email = request.POST.get("email").lower()
        password = request.POST.get("password") #at this point we are getting the value from the frontend(we are getting the post that was made) 
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "user does not exist")
        user = authenticate(request, email=email, password=password)
        if user is not None:  # translation if the user is a user.
            login(request, user) #login takes in two arguments
            return redirect("home")
        else:
            messages.error(request, "username or password does not exist")
    context={"page":page}
    return render(request, "base/login_register.html", context)



def logoutUser(request):
    logout(request)
    return redirect("home")



def register_page(request):
    form = My_usercreationForm()
    if request.method == "POST":
        form = My_usercreationForm(request.POST)
        if form.is_valid():
            user=  form.save(commit=False) # held it here
            user.username = user.username.lower() # to change it to lower case for our user here
            user.save() #then actually saved itt
            login(request, user)
            return redirect("home") 
        else:
            messages.error(request, 'error occurred during registration')    
    return render(request, "base/login_register.html", {"form":form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    spaces = Space.objects.filter(
        Q(topic__name__icontains=q)|
        Q(name__icontains=q)|
        Q(description__icontains=q))
    
    topics = Topic.objects.all()[0:5] #translation: give us all topics but display 0 to 5 of them
    
    space_count = spaces.count()
    
    space_messages = Message.objects.filter(Q(space__name__icontains=q)) #if we wanted recent activity to be based on who we follow we would probably use filter
                                                                        #IMPORTANT on this line we were able to filter our activity column to show info based on the message space name.
    context = {'spaces':spaces, 'topics':topics, 'space_count':space_count, 'space_messages':space_messages}
    return render(request,'base/home.html', context) # third slot carries what we are working with


def space(request, pk):
    space = Space.objects.get(id=pk)  #this means we are getting value by the id
    space_messages = space.message_set.all() # translation: give us the set of messages related to this space
    participants = space.participants.all()#translate get all in participants
    
    
    if request.method == "POST": # at this point we write code to allow  user visibly comment
        space_messages = Message.objects.create(
            user = request.user,
            space = space,                    #we get the input from the frontend
            body = request.POST.get("body")
        )
        space.participants.add(request.user) # in order to add the user who commented to our participants column.
        return redirect("space", pk=space.id )

    
    context = {'space':space, 'space_messages':space_messages, "participants":participants}
    return render(request,'base/space.html', context)

def user_profile(request, pk): 
    user = User.objects.get(id=pk) # get user based on id
    spaces = user.space_set.all() # tranlation get all spaces related to this specific user/ the space we display on profile view is based on our user unlike home
    space_messages=user.message_set.all() # this is to get the messages specific to this user for our profile activity component which will show only messagesmade by the specific user
    topics = Topic.objects.all()
    context={"user":user, "spaces":spaces,"space_messages":space_messages,"topics":topics}
    return render(request, "base/profile.html", context)




@login_required(login_url="login")
def create_space(request):
    form = Spaceform()  # diff btw create_space and update_space in c we got spaceform with nothing in it whereas the latter we have sothing in it 
    topics = Topic.objects.all()
    if request.method == 'POST':
        form = Spaceform(request.POST)# in an instance where we type request.POST only it means we are passing in the data
        topic_name = request.POST.get('topic') # we get the topic from the front end
        topic, created = Topic.objects.get_or_create(name= topic_name) # check if the topic already exists in database else we create a new one designate to name
        
        Space.objects.create(
            host=request.user, # we excluded host(along with participants) because it is not something we want to fill on our form. it is made now that the user that made the request is the host
            topic= topic, # topic either is what already exists i database or what is newly created
            name= request.POST.get("name"),
            description= request.POST.get("description"),
        )      
        
        return redirect("home")       
    context = {'form':form, "topics":topics}
    return render(request, 'base/space_form.html', context)



@login_required(login_url="login")
def update_space(request, pk):
    space = Space.objects.get(id=pk) # we get the item we want to update (space) based on its id or pk
    form = Spaceform(instance=space) #Then we get the form # instance=space pre-fills our empty form with the space value 
    topics = Topic.objects.all()
    if request.user !=  space.host:
        return HttpResponse('you are not the host!') #this stops someone who isnt the host from accessing this function
         
    if request.method == 'POST':
        form = Spaceform(request.POST, instance=space) # before this line when we update space is not overwritten so now when POST is implemented it overwrites space or instance=space
        topic_name = request.POST.get('topic') # we get the topic from the front end
        topic, created = Topic.objects.get_or_create(name= topic_name) # check if the topic already exists in database else we create a new one designate to name
        space.name = request.POST.get("name") #the name of the space we are updating is equals to what we get from our frontend
        space.topic = topic
        space.description = request.POST.get("description") #the description of the space we are updating is equals to what we get from our frontend
        space.save()
        return redirect("home")
    context= {'form':form,"topics":topics,'space':space}
    return render(request, 'base/space_form.html', context)



@login_required(login_url="login")
def delete_space(request, pk):
    space = Space.objects.get(id=pk)
    
    if request.user != space.host: # Translation: if user who requests is not equal to host in our message model return http response 
        return HttpResponse('you are not the host!')
    
    if request.method == 'POST':
        space.delete()
        return redirect('home')
    return render(request, "base/delete.html", {"obj":space})



@login_required(login_url="login")
def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    
    if request.user !=  message.user: # Translation: if user who requests is not equal to user in our message model return http response 
        return HttpResponse('you are not the host!')
        
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, "base/delete.html", {"obj":message})
        
        
@login_required(login_url="login")
def UpdateUser(request):
    user = request.user
    form = Userform(instance=user)
    
    if request.method == "POST":
        form = Userform(request.POST, request.FILES ,instance=user)
        if form.is_valid:
            form.save()
            return redirect("user-profile", pk=user.id)
    return render(request, "base/update-user.html", {"form":form})


def topics_page(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)  #Translation filter based on the topic name that contains part of query or q
    return render(request, "base/topics.html", {"topics":topics})
    
    
def activity_page(request):
    space_messages= Message.objects.all()
    context={"space_messages":space_messages}
    return render(request, "base/activity.html", context)
     