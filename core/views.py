from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse

from django.http import HttpResponse
from django.forms import forms
from django.shortcuts import render
from tablib import Dataset

from core.models import Category, Store
from account.models import Univ, Profile
from core.resources import StoreResource


def home(request, pk):
    current_user = request.user
    profile = Profile.objects.get(user=current_user.id)
    univ = profile.univ
    categories = Category.objects.filter(univ_id=univ)
    data = {
        'current_user': current_user.id,
        'univ': univ,
        'profile': profile,
        'categories': categories,
    }
    return render(request, 'core/home.html', data)



def match_new(request, pk):
    univ = request.user.profile.univ
    univ_input = Profile.objects.filter(name=univ)
    categories = Category.objects.get()
    stores = Store.objects.all()
    if request.method == "POST":
        pass
    else:
        pass
    return render(request, 'core/match_new.html')


def choice_cat(request, pk):
    cats = Category.objects.all()
    if request.method == 'POST':
        pass
    else:
        data = {
            'cats':cats,
        }
    return render(request, 'core/choice_cat.html', data)


def choice_store(request):
    return render(request, 'core/choice_store.html')


def match_fin(request):
    return render(request, 'core/match_fin.html')


def mypage(request):
    return render(request, 'core/mypage.html')

def main(request):
    univs = Univ.objects.all()
    data = {
        'univs': univs
    }
    return render(request, 'core/main.html', data)


# class UploadFileForm(forms.Form):
#     file = forms.FileField()
#
#
# # Create your views here.
# def upload(request):
#     if request.method == "POST":
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             filehandle = request.FILES['file']
#             return excel.make_response(filehandle.get_sheet(), "xlsx",
#                                        file_name="download")
#     else:
#         form = UploadFileForm()
#     return render(
#         request,
#         'upload_form.html',
#         {
#             'form': form,
#             'title': 'Excel file upload and download example',
#             'header': ('Please choose any excel file ' +
#                        'from your cloned repository:')
#         })

def export(request):
    person_resource = CrawlingResource()
    dataset = person_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="persons.xlsx"'
    return response


def simple_upload(request):
    if request.method == 'POST':
        person_resource = StoreResource()
        dataset = Dataset()
        new_persons = request.FILES['myfile']

        imported_data = dataset.load(new_persons.read())
        result = person_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            person_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'core/simple_upload.html')

#
# def export(request):
#     person_resource = CrawlingResource()
#     dataset = person_resource.export()
#     response = HttpResponse(dataset.csv, content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="persons.csv"'
#     return response