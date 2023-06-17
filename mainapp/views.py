from typing import Counter
from django.shortcuts import render, HttpResponse, redirect
from os import listdir
from os.path import isfile, join
from django.shortcuts import render
from django.views.generic.base import TemplateView
from .forms import MyfileUploadForm
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import file_upload
from .models import FileModel
from myproj import settings


def index(request):
    file_upload.objects.all().delete()
    all_data = file_upload.objects.all()
    media_path = settings.MEDIA_ROOT
    myfiles = [f for f in listdir(media_path) if isfile(join(media_path, f))]

    for a in range(len(myfiles)):
        file_upload( my_file=myfiles[a]).save()

    if request.method == 'POST':
        form = MyfileUploadForm(request.POST, request.FILES)

        print(form.as_p)

        if form.is_valid():
            user = request.user
            file_size = request.FILES['file'].size

            if user.storage_space >= file_size:
                file = form.save(commit=False)
                file.user = user
                file.save()
                user.storage_space -= file_size
                user.save()
                the_files = form.cleaned_data['files_data']
                the_files = form.files.getlist('files_data')
                for i in the_files:
                    file_upload( my_file=i).save()

                return HttpResponse("file upload")

            else:
                 messages.error(request, 'Brak miejsca na dysku')

        else:
            length=[]
            all_data = file_upload.objects.all()
            the_files = form.files.getlist('files_data')

            file_size = 0
            for f in the_files:
                file_size += f.size

            user = request.user

            if user.storage_space >= file_size:
#                file.user = user
                user.storage_space -= file_size
                user.save()

                for i in the_files:
                     file_upload( my_file=i).save()
                     b = i
                     length.append(b)
                context = {
                    'filedata':the_files,
                    'data':all_data,
                    'len':length
                }
                return render(request,'uploaded.html',context)


            else:
                 messages.error(request, 'Brak miejsca na dysku')

    else:
        if 'q' in request.GET:
            q= request.GET['q']
            all_data = file_upload.objects.filter(my_file__icontains=q)
            numof = len(all_data)
            context = {
            'form':MyfileUploadForm(),
            'datas':myfiles ,
            'data': all_data,
            'no_files':numof
           }

            return render(request, 'index.html', context)
        else:
             all_data = file_upload.objects.all()
        numof = len(myfiles)
        context = {
            'form':MyfileUploadForm(),
            'datas':myfiles ,
            'data': all_data,
            'no_files':numof
        }

        return render(request, 'index.html', context)


def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("home")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"register_form":form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("home")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})


def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.")
	return redirect("home")
