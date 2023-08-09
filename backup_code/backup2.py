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
