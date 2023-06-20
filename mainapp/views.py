import os
from typing import Counter
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
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
    user = request.user
    myfiles = None

    if user.is_authenticated:
        myfiles = user.files.all()

    if request.method == 'POST':
        form = MyfileUploadForm(request.POST, request.FILES)

        print(form.as_p)

        if form.is_valid():
            file_size = request.FILES['file'].size

            if user.storage_space - user.used_storage_space >= file_size:
                file = form.save(commit=False)
                file.save()
                user.used_storage_space += file_size
                user.save()
                the_files = form.cleaned_data['files_data']
                the_files = form.files.getlist('files_data')

                for f in the_files:
                    FileModel(owner=user, file=f).save()

                messages.success(request, 'Plik został pomyślnie załadowany na dysk')

            else:
                messages.error(request, 'Brak miejsca na dysku')

            return redirect("home")

        else:
            length=[]
            the_files = form.files.getlist('files_data')

            file_size = 0
            for f in the_files:
                file_size += f.size

            user = request.user

            if user.storage_space - user.used_storage_space >= file_size:
                user.used_storage_space += file_size
                user.save()

                for f in the_files:
                     FileModel(owner=user, file=f).save()
                     b = f
                     length.append(b)

                context = {
                    'filedata':the_files,
                    'data':myfiles,
                    'len':length
                }

                messages.success(request, 'Plik został załadowany na dysk')

            else:
                messages.error(request, 'Brak miejsca na dysku')

            return redirect("home")

    else:
        if 'q' in request.GET:
            q = request.GET['q']
            numof = len(myfiles)

            context = {
                'form':MyfileUploadForm(),
                'datas':myfiles ,
                'data':myfiles,
                'no_files':numof
            }

            return render(request, 'index.html', context)

        numof = 0
        if user.is_authenticated:
            numof = len(myfiles)

        context = {
            'form':MyfileUploadForm(),
            'datas':myfiles,
            'data':myfiles,
            'no_files':numof
        }

        return render(request, 'index.html', context)


def delete_file(request, file_id):
    file_model = get_object_or_404(FileModel, ids=file_id)
    file_path = os.path.join(settings.MEDIA_ROOT, file_model.file.name)
    user = request.user
    user.used_storage_space -= file_model.file.size
    user.save()
    file_model.delete()
    os.remove(file_path)
    messages.success(request, "Plik został usunięty z dysku")
    return redirect('home')


def rename_file(request, file_id):
    file_model = get_object_or_404(FileModel, ids=file_id)

    if request.method == 'POST':
        new_name = request.POST.get('new_name')
        if new_name:
            os.rename(os.path.join(settings.MEDIA_ROOT, file_model.file.name), os.path.join(settings.MEDIA_ROOT, new_name))
            file_model.file.name = new_name
            file_model.save()
            messages.success(request, "Pomyślnie zmieniono nazwę pliku")
            return redirect('home')

    context = {
        'file': file_model,
    }

    return render(request, 'rename_file.html', context)


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.save()
            login(request, user)
            messages.success(request, "Rejestracja zakończyła się pomyślnie" )
            return redirect("home")

        messages.error(request, "Rejestracja nie zakończyła się pomyślnie")

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
				messages.info(request, f"Jesteś zalogowany jako {username}.")
				return redirect("home")
			else:
				messages.error(request,"Zła nazwa użytkownika lub hasło.")
		else:
			messages.error(request,"Zła nazwa użytkownika lub hasło.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})


def logout_request(request):
	logout(request)
	messages.info(request, "Wylogowano się pomyślnie.")
	return redirect("home")
