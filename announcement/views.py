from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Ann_table, AnnMarkRead
from .forms import AnnTableForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils import timezone



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

def __str__(self):
        return self.announc.subject
class AnnDelete(DeleteView):
    model = Ann_table
    template_name = 'announcement/ann_delete.html'
    context_object_name = 'anndetails'
    success_url = reverse_lazy('annlist')



    

class AnnMarkReadList(ListView):
    model = AnnMarkRead
    template_name = 'announcement/ann_mark_list.html'
    context_object_name = 'annmarklists'

class AnnMarReadDetail(DetailView):
    model = AnnMarkRead
    template_name = 'announcement/ann_mark_detail.html'
    context_object_name = 'annmarkdetails'




class AnnMarkReadCreate(CreateView):
    model = AnnMarkRead
    fields = '__all__'
    template_name = 'announcement/ann_mark_create.html'
    success_url = reverse_lazy('annlist')


class AnnMarkReadUpdate(UpdateView):
    model = AnnMarkRead
    fields = '__all__'
    template_name = 'announcement/ann_mark_create.html'
    success_url = reverse_lazy('annlist')

'''class AnnUserView(View):
    
    def get(self, request):
        user = request.user
        print('====================',user.id)
        announcements = Ann_table.objects.filter(visible_to=user.id,is_read=False)
        return render(request, 'announcement/ann_view_user.html',{'announcements':announcements})
    
    def post(self, request):
        user = request.user
        if 'mark' in request.POST:
            ann = Ann_table.objects.get(visible_to=user.id)
            ann.is_read = True
            ann.save()
            ann.visible_to.exclude(id=user.id).update(is_read=False)
            return redirect('annviews')'''
    


    

class AnnUserView(View):

    def get(self, request):
        user = request.user
        #announcements = AnnMarkRead.objects.get(user=user.id)
        announcements = AnnMarkRead.objects.filter(user=user.id,is_read=False)
        print('-----------------------',announcements)
        return render(request, 'announcement/ann_view_user.html',{'announcements':announcements})
    
    def post(self, request):
        user = request.user
        if 'mark' in request.POST:
            announcement_id = request.POST.get('announcement_id')
            #announcement = get_object_or_404(Ann_table, id=announcement_id)
            
            # Check if the user has already marked this announcement as read
            print("user----",user)
            ann_mark = get_object_or_404(AnnMarkRead, announc_id=announcement_id, user=user.id)
            print('-----------',ann_mark)
            #if not ann_mark.is_read:
            ann_mark.is_read = True
            ann_mark.save()
                
        return redirect('annviews')
    

    '''def post(self, request):
        user = request.user
        if 'mark' in request.POST:
            announcement_ids = request.POST.getlist('announcement_ids')
            print('3333333333333333333333333',announcement_ids)
            for announcement_id in announcement_ids:
                announcement = get_object_or_404(Ann_table, pk=announcement_id)
                if not announcement.is_read_by_user(user):
                    AnnMarkRead.objects.create(announcement=announcement, user=user, is_read=True, read_at=timezone.now())
            return redirect('annviews')'''
'''ann = Ann_table.objects.get(visible_to=user.id)
            ann.is_read = True
            ann.save()
            print('===================================================',ann)
            
            #ann.save()
            #ann.visible_to.exclude(id=user.id).update(is_read=False)
            return redirect('annviews')'''




'''class AnnUserReadView(View):

    def get(self, request):
        user = request.user
        announcements = AnnUserRead.objects.filter(user_read=user.id,is_read=False)
        print(']]]]]]]]]]]]]]]]]]]]]]]]]]]',announcements)
        return render(request, 'announcement/ann_view_user.html',{'announcements':announcements})
    

    def post(self,request):
        user = request.user
        if 'mark' in request.POST:
            ann = AnnUserRead.objects.get(user_read=user.id)
            ann.is_read = True
            ann.save()
            return redirect('annviews')'''



class AnnHistory(View):

    def get(self, request):
        user = request.user
        announcements = AnnMarkRead.objects.filter(user=user.id, is_read=True)
        return render(request, 'announcement/ann_history_user.html',{'announcements':announcements})
    





        

