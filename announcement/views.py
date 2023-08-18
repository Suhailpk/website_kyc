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
import zipfile
from io import BytesIO
from django.contrib.auth.mixins import LoginRequiredMixin
import csv
from io import StringIO



# Create your views here.




class AnnList(LoginRequiredMixin, ListView):
    model = Ann_table
    context_object_name = 'annlists'
    template_name = 'announcement/ann_list.html'


class AnnDetail(LoginRequiredMixin,DetailView):
    model = Ann_table
    context_object_name = 'anndetails'
    template_name = 'announcement/ann_detail.html'


class AnnCreate(LoginRequiredMixin,CreateView):
    model = Ann_table
    template_name  = 'announcement/ann_create.html'
    form_class = AnnTableForm
    success_url = reverse_lazy('annlist')





class AnnUpdate(LoginRequiredMixin,UpdateView):
    model = Ann_table
    template_name  = 'announcement/ann_create.html'
    form_class = AnnTableForm
    success_url = reverse_lazy('annlist')

def __str__(self):
        return self.announc.subject




class AnnDelete(LoginRequiredMixin,DeleteView):
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

    

class AnnUserView(LoginRequiredMixin,View):

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
    

class AnnHistory(LoginRequiredMixin,View):

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
            chunk_size = 5  # Number of announcements per CSV file

            for chunk_start in range(0, len(selected_announcements), chunk_size):
                chunk_end = chunk_start + chunk_size
                chunk = selected_announcements[chunk_start:chunk_end]
                
                csv_data = StringIO()
                csv_writer = csv.writer(csv_data)
                csv_writer.writerow(["Subject", "Message", "Start Date", "End Date"])

                for announcement in chunk:
                    csv_writer.writerow([
                        announcement.subject,
                        announcement.message,
                        announcement.start_date.strftime("%Y-%m-%d %H:%M:%S"),
                        announcement.end_date.strftime("%Y-%m-%d %H:%M:%S")
                    ])

                csv_data.seek(0)  # Reset the StringIO position

                file_name = f'selected_announcements_{chunk_start}-{chunk_end}.csv'
                zip_file.writestr(file_name, csv_data.read())

        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="selected_announcements.zip"'
        return response



    

'''class CsvList(ListView):
    model = Ann_table
    context_object_name = 'csvlists'
    template_name = 'announcement/ann_csv.html'''
    
