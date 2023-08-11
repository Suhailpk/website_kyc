from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.http import HttpResponse
from django.views.generic.edit import FormView
from django.core.mail import send_mail
from .forms import EmailForm, KycForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile, Kyc
import uuid
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404


# Create your views here.


class HomeView(View):

    def get(self, request):
        return render(request, 'base/index.html', {})


class LoginView(View):

    def get(self, request):
        return render(request, 'base/login.html', {})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=username).first()

        if user_obj is not None and user_obj.username  == 'admin':
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user=user)
                return redirect('home')
        
        else:

            if user_obj is None:
                messages.success(request, 'User is not found')
                return redirect('login')
            
            else:

                profile_obj = Profile.objects.filter(user=user_obj).first()

                if not profile_obj.is_verified:
                    messages.success(request, 'Profile is not verified please check your mail')
                    return redirect('login')

                user = authenticate(username=username, password=password)

                if user is None:
                    messages.success(request, 'Wrong password')
                    return redirect('login')

                login(request, user=user)
                return redirect('home')


class RegisterView(View):

    def get(self, request):
        return render(request, 'base/register.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            if User.objects.filter(username=username).first():
                messages.success(request, 'Username is already taken')
                return redirect('/register')
            
            if User.objects.filter(email=email).first():
                messages.success(request, 'Email is already taken')
                return redirect('/register')

            user_obj = User.objects.create(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()

            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user=user_obj, auth_token=auth_token)
            profile_obj.save()

            send_mail_for_verification(email=email, token=auth_token)
            return redirect('token')
        
        except Exception as e:
            print(e)

        return render(request, 'base/register.html')



class TokenView(View):

    def get(self, request):
        return render(request, 'base/token.html')
    

class SuccessView(View):

    def get(self, request):
        return render(request, 'base/success2.html')




def send_mail_for_verification(email,token):
    subject = 'Your accounts need to verified'
    message = f'Hi Paste the link to verify account http://127.0.0.1:8000/verify/{token} '
    from_mail = settings.EMAIL_HOST_USER


    send_mail(
        subject=subject,
        message=message,
        from_email=from_mail,
        recipient_list=[email]
        )


class VerifyView(View):

    def get(self, request, auth_token):
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified')
                return redirect('login')

            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified please login again')
            return redirect('login')

        else:
            return redirect('error')
    

class ErrorView(View):

    def get(self, request):
        return render(request, 'base/error.html')
    


class SendMailView(LoginRequiredMixin, FormView):
    template_name = 'base/mail.html'
    form_class = EmailForm
    success_url = 'success'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']

        send_mail(
            subject=subject,
            message=message,
            from_email='suhailpk24@gmail.com',
            recipient_list=[email]
        )


        context = {'email': email}
        return render(self.request, 'base/success.html', context)
    

class AboutView(View):

    def get(self, request):
        return render(request, 'base/about.html')
    


class PortFolioView(View):

    def get(self, request):
        return render(request, 'base/portfolio.html')


class TeamView(View):

    def get(self, request):
        return render(request, 'base/team.html')
    

#Kyc Views


class KycView(LoginRequiredMixin, View):
    template_name = 'base/kyc.html'
    
    
    def get(self, request):
        kyc_submitted = Kyc.objects.filter(user=request.user, submitted=True)
        if kyc_submitted:
            return render(request, self.template_name, {'kyc_submit':'kyc_submitted'})
        form = KycForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = KycForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            kyc_instance = form.save(commit=False)  # Don't save to the database yet
            kyc_instance.user = request.user  # Set the user
            kyc_instance.submitted = True
            kyc_instance.save()  # Now save to the database
            return redirect('successkyc')
        return render(request, self.template_name, {'form': form})


class KycStatus(LoginRequiredMixin, View):
    
    template_name = 'base/kycstatus.html'

    def get(self, request):
        user = request.user
        kyc_count = Kyc.objects.filter(user=user).count()
        kyc_waiting = Kyc.objects.filter(user=user, approved=False, waiting=False).exists()
        kyc_wait_rejected = Kyc.objects.filter(user=user, approved=False, waiting=True).exists()
        kyc_approved = Kyc.objects.filter(user=user, approved=True, waiting=True).exists()
        


        if kyc_count == 0:
            context = {'Approve': 'No data'}

        elif kyc_wait_rejected:
            context = {'Approve': 'Rejected'}

        elif kyc_waiting:
            context = {'Approve': 'Waiting'}

        elif kyc_approved:
            context = {'Approve': 'Approved'}




        return render(request, self.template_name, context)
    



class SuccessKycView(View):
    template_name = 'base/successkyc.html'
    
    def get(self, request):
        return render(request, self.template_name)



class KycChoose(LoginRequiredMixin,View):
    
    def get(self, request):
        return render(request, 'base/kycchoose.html')
    
    def post(self, request):
        if 'kyc_apply' in request.POST:
            return redirect('kyc')
    
        if 'kyc_status' in request.POST:
            return redirect('kycstatus')
    
#Kyc admin side views


class KycList(ListView):
    model = Kyc
    template_name = 'base/kyclist.html'
    context_object_name = 'kyc_lists'

class KycDetail(DetailView):
    model = Kyc
    template_name = 'base/kycdetails.html'
    context_object_name = 'kyc_list'



    def post(self, request, *args, **kwargs):
        kyc_instance = self.get_object()

        if 'approve' in request.POST:
            if request.user.is_staff: 
                kyc_instance.approved = True
                kyc_instance.waiting = True
                kyc_instance.save()
                return render(request, 'base/kycadmin.html',{'Approve':'Approved'})
            else:
                return HttpResponse('<h1>You do not have permission to approve<h1/>')

        elif 'reject' in request.POST:
            if request.user.is_staff: 
                kyc_instance.approved = False
                kyc_instance.waiting = True
                #kyc_instance.submitted = False
                kyc_instance.save()
                return render(request, 'base/kycadmin.html',{'Approve':'Rejected'})
            
        elif 'resubmit' in request.POST:
            if request.user.is_staff: 
                kyc_instance.delete()
                return render(request, 'base/kycadmin.html',{'Approve':'Resubmit'})
            else:
                return HttpResponse('<h1>You do not have permission to reject<h1/>')

        return HttpResponse('Invalid action')
    





    


    






