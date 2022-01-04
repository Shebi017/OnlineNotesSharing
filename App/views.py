from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate,login

# Create your views here.

def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    if request.method == "POST":
        data = request.POST

        contact = Contact(name=data['name'],phone=data['phone'],email=data['email'],subject=data['subject'],message=data['message'])

        contact.save()

        messages.success(request,'Message is Sent Successfully.')

        return redirect('/')
    return render(request, "contact.html")

def user_signup(request):
    if request.method == "POST":
        data = request.POST
        username = data['username']
        branch = Branch.objects.get(id=data['branch'])
        check_user = User.objects.filter(username=username).first()
        if check_user is not None:
            messages.success(request,'Username is already exisist.')

        user = User.objects.create(first_name=data['fname'],last_name=data['lname'],username=data['username'],email=data['email'])

        user.set_password(data['password'])

        user.save()

        profile = Profile.objects.create(user=user,phone=data['phone'],branch=branch,role=data['role'])
        profile.save()
        messages.success(request,'User is registred successfully.')

        return redirect("/user_login/")
    
    branches = Branch.objects.all()

    context={
        'branches':branches,
    }

    return render(request, "user_signup.html",context)

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,'User is Logged In  successfully.')
            return redirect("/profile_home/")
        else:
            messages.success(request,'Invalid Username or Password.')
            return redirect("/user_login/")
            
    return render(request, "user_login.html")

def admin_login(request):
    if request.method == "POST":
        data = request.POST
        user = authenticate(request,username=data['username'],password=data['password'])

        if user is not None:
            if user.is_staff:
                login(request, user)
                messages.success(request, 'Admin is logged in successfully.')
                return redirect("/admin/")
            else:
                messages.success(request, 'User is not Admin')
                return redirect("/admin_login/")
        
        else:
            messages.success(request, 'Invalid username or password')
            return redirect("/admin_login/")
    return render(request, "admin_login.html")


def profile_home(request):
    # if not request.user.is_authenticated:
    #     return redirect("/user_login/")
    user = request.user
    profile = Profile.objects.get(user=user)
    context={
        'profile':profile,
    }
    return render(request, "profile/home.html",context)

def upload_notes(request):
    if request.method == "POST":
        try:
            branch_id = request.POST.get('branch')
            branch = Branch.objects.get(id=branch_id)
            subject = request.POST.get('subject')
            file = request.FILES.get('file')
            file_type = request.POST.get('file_type')
            description = request.POST.get('description')

            profile = Profile.objects.get(user=request.user)

            Note.objects.create(branch=branch,subject=subject,file_type=file_type,description=description,file=file,profile=profile)

            messages.success(request, "Notes is uploaded successfully")
            return redirect("/view_my/")
        except Exception as e:
            print(e)
            messages.success(request, "Something went wrong.Please try again.")
            return redirect("/upload_notes/")

    branches = Branch.objects.all()

    context={
        'branches':branches,
    }
    return render(request, "profile/upload.html",context)

def view_all_notes(request):
    notes = Note.objects.filter(status="Accept")

    context={
        'notes':notes,
    }
    return render(request, "profile/all_notes.html",context)

def view_my_notes(request):
    profile = Profile.objects.get(user= request.user)
    notes = Note.objects.filter(profile=profile)
    context={
        'notes':notes,
    }
    return render(request, "profile/my_notes.html",context)

def user_logout(request):
    logout(request)
    return redirect('/')

def update_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    branches = Branch.objects.all()
    if request.method == "POST":
        data = request.POST
        ############################### EDIT LOGIC ########################
        user.first_name = data['fname']
        user.last_name = data['lname']
        user.email = data['email']
        user.username = data['username']
        profile.phone = data['phone']

        profile.branch = Branch.objects.get(id=data['branch'])
        profile.role = data['role']

        profile.save()
        user.save()

        messages.success(request,"Profile is edit successfully.")

        return redirect("/profile_home/")

    context={
        'profile':profile,
        'branches':branches,
    }
    return render(request, "profile/update.html",context)

def change_password(request):
    user = request.user
    if request.method == "POST":
        data = request.POST
        if data['confirm'] == data['new']:
            user.set_password(data['new'])
            user.save()
            messages.success(request, 'Password is changed successfully.')
            return redirect("/user_login/")
        else:
            messages.success(request,"Password is not matched")
            return redirect("/change_password/")


    return render(request, "profile/change_password.html")


