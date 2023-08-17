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
import datetime
import csv
import zipfile
from io import BytesIO



# Create your views here.




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

    

class AnnUserView(View):

    def get(self, request):
        user = request.user
        #current_date = datetime.datetime.now().date()
        now  = timezone.now()
        #start_date = now - timezone.timedelta(days=7)
        #end_date = now

        announcements = AnnMarkRead.objects.filter(user=user.id,is_read=False,announc__start_date__lte=now,announc__end_date__gte=now)
        
        print('===================',now)
        return render(request, 'announcement/ann_view_user.html',{'announcements':announcements})
    
    def post(self, request):
        user = request.user
        if 'mark' in request.POST:
            announcement_id = request.POST.get('announcement_id')
            ann_mark = get_object_or_404(AnnMarkRead, announc_id=announcement_id, user=user.id)
            ann_mark.is_read = True
            ann_mark.save()
                
        return redirect('annviews')
    

class AnnHistory(View):

    def get(self, request):
        user = request.user
        announcements = AnnMarkRead.objects.filter(user=user.id, is_read=True)
        return render(request, 'announcement/ann_history_user.html',{'announcements':announcements})
    



class ExportSelectedAnnouncements(View):
    def post(self, request):
        selected_ids = request.POST.getlist('selected_ids[]')
        selected_announcements = Ann_table.objects.filter(id__in=selected_ids)

        # Create a BytesIO object to store the zip data
        zip_buffer = BytesIO()

        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            csv_data = "Subject,Message,Start Date,End Date\n"
            
            for announcement in selected_announcements:
                csv_data += f"{announcement.subject},{announcement.message},{announcement.start_date},{announcement.end_date}\n"

            zip_file.writestr('selected_announcements.csv', csv_data)

        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="selected_announcements.zip"'
        return response
    

class CsvList(ListView):
    model = Ann_table
    context_object_name = 'csvlists'
    template_name = 'announcement/ann_csv.html'
    
