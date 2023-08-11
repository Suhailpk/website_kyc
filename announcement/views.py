from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Ann_table
from .forms import AnnTableForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy



# Create your views here.

'''class Announcement(View):

    def get(self,request):
        form = AnnTableForm()
        return render(request,'announcement/announcement.html',{'form':form})
    
    def post(self, request):
        form = AnnTableForm(request.POST)
        if form.is_valid():
            form.save()
        return render(request,'announcement/announcement.html',{'form':form})'''


class AnnList(ListView):
    model = Ann_table
    context_object_name = 'annlists'
    template_name = 'announcement/ann_list.html'


class AnnDetail(DetailView):
    model = Ann_table
    context_object_name = 'anndetails'
    template_name = 'announcement/ann_detail.html'


class AnnCreate(CreateView):
    model = Ann_table
    template_name  = 'announcement/ann_create.html'
    form_class = AnnTableForm
    success_url = reverse_lazy('annlist')



'''class AnnCreate(View):

    def get(self,request):
        form = AnnTableForm()
        return render(request,'announcement/ann_create.html', {'form':form})
    
    def post(self,requset):
        form = AnnTableForm(data=requset.POST, files=requset.FILES)
        if form.is_valid():
            form.save()
            return redirect('annlist')
        return render(requset,'announcement/ann_create.html', {'form':form})'''


class AnnUpdate(UpdateView):
    model = Ann_table
    template_name  = 'announcement/ann_create.html'
    form_class = AnnTableForm
    success_url = reverse_lazy('annlist')


class AnnDelete(DeleteView):
    model = Ann_table
    template_name = 'announcement/ann_delete.html'
    context_object_name = 'anndetails'
    success_url = reverse_lazy('annlist')



        

