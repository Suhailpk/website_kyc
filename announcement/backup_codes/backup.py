class AnnUserRead(models.Model):
    user_read = models.OneToOneField(AnnMarkRead, on_delete=models.CASCADE)
    announc_read = models.ForeignKey(Ann_table, on_delete=models.CASCADE) 
    is_read = models.BooleanField(default=False)                   


class AnnMarkRead(models.Model):
    announcement = models.ForeignKey('Ann_table', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

class Ann_table(models.Model):
    subject = models.CharField(max_length=200)
    message = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.ImageField(upload_to='ann_images/')
    visible_to = models.ManyToManyField(User, related_name='visible_announcements')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

    def is_read_by_user(self, user):
        return AnnMarkRead.objects.filter(announcement=self, user=user, is_read=True).exists()
        
        
 
 
class Announcement(View):

    def get(self,request):
        form = AnnTableForm()
        return render(request,'announcement/announcement.html',{'form':form})
    
    def post(self, request):
        form = AnnTableForm(request.POST)
        if form.is_valid():
            form.save()
        return render(request,'announcement/announcement.html',{'form':form})
        
        
        

class AnnCreate(View):

    def get(self,request):
        form = AnnTableForm()
        return render(request,'announcement/ann_create.html', {'form':form})
    
    def post(self,requset):
        form = AnnTableForm(data=requset.POST, files=requset.FILES)
        if form.is_valid():
            form.save()
            return redirect('annlist')
        return render(requset,'announcement/ann_create.html', {'form':form})
        
        
class AnnUserView(View):
    
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

