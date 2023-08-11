def kyc(request):


    if request.method == 'POST':
        form = KycForm(request.POST)
        if form.is_valid():
            kyc_obj = form.save(commit=False)
            kyc_obj.user = request.user
            kyc_obj.save()
            return render(request, 'successkyc.html')

    else:
        form = KycForm()
        return render(request, 'kyc.html',{'form':form})
        
        
        
def kyc(request):
    if request.method == 'POST':
        form = KycForm(user=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            kyc_instance = form.save()
            return redirect('successkyc')
    else:
        form = KycForm(user=request.user)
    return render(request, 'kyc.html', {'form': form})
    
   
   
class AdminNotes(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #kyc = models.OneToOneField(Kyc, on_delete=models.CASCADE)<th scope="col">Address</th>
    
    
    
'''class AdminReason(View):
    
    def get(self, request):
        form = AdminReasonForm()
        return render(request,'kycreason.html', {'form':form})
    
    def post(self, request):
        form = AdminReasonForm(data=request.POST)
        if form.is_valid():
            admin_reason = form.save(commit=False)
            admin_reason.user = request.user
            admin_reason.submit_note = True
            admin_reason.save()
            return HttpResponse('<h1>Reason send to user<h1/>')
        return render(request, 'kycreason.html', {'form':form})'''

'''note = request.POST.get('note')
        admin_note = AdminNotes.objects.create(user=request.user, rejected_reason=note, submit_note=True)
        admin_note.save()
        return HttpResponse('<h1>Notes send to user<h1/>')'''

class AdminReason(View):
    
    def get(self, request):
        form = AdminReasonForm()
        return render(request, 'kycreason.html', {'form': form})
    
    def post(self, request):
        form = AdminReasonForm(data=request.POST)
        if form.is_valid():
            user_name_id = form.cleaned_data['user_name_id']
            user_instance = User.objects.get(pk=user_name_id)
            print(user_instance.id,'fdggggggggggggggggggg')
            admin_reason, created = AdminNotes.objects.get_or_create(user=user_instance.id)
            admin_reason.rejected_reason = form.cleaned_data['rejected_reason']
            admin_reason.submit_note = True
            admin_reason.save()
            return HttpResponse('<h1>Reason sent to user</h1>')
        return render(request, 'kycreason.html', {'form': form})
        
        
    path('kycreason/', views.AdminReason.as_view(), name='kycreason'),
    
    
    
 class AdminReasonForm(forms.ModelForm):
    class Meta:
        model = AdminNotes
        fields = '__all__'
        exclude = ['submit_note']

class KycRejectionForm(forms.Form):
    rejection_reason = forms.CharField(widget=forms.Textarea)


kyc_rej_reason = AdminNotes.objects.all()
'Reasons':kyc_rej_reason}

