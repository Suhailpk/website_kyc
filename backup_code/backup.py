
# code before email verification


class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')
    
    

class CustomRegisterView(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse_lazy('home')
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super(CustomRegisterView, self).form_valid(form)
    
    def get(self, *agrs, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super(CustomRegisterView, self).get(*agrs, **kwargs)



class Home(TemplateView):
    template_name = 'index.html'



class SendMailView(LoginRequiredMixin, FormView):
    template_name = 'mail.html'
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
        return render(self.request, 'success.html', context)
        
        
# function based views after email verification


def login2(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')


        user_obj = User.objects.filter(username=username).first()

        print('user is  ===',user_obj)

        if user_obj is None:
            messages.success(request, 'User is not found')
            redirect('login2')

        else:

            profile_obj = Profile.objects.filter(user = user_obj).first()

            if not profile_obj.is_verified:
                messages.success(request, 'Profile is not verified please check your mail')
                return redirect('login2')
        
            user = authenticate(username=username, password=password)

            if user is None:
                messages.success(request, 'Wrong username or wrong password')
                return redirect('login2')
            
            login(request, user=user)
            return redirect('home')
            

    return render(request, 'login2.html', {})
    
    



def home(request):
    return render(request, 'index.html', {})
    
    
    
def register2(request):
     
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')


        try:

            if User.objects.filter(username=username).first():
                messages.success(request,'username is already taken')
                return redirect('/register2')
            
            if User.objects.filter(email=email).first():
                messages.success(request,'email is already taken')
                return redirect('/register2')
            

            user_obj = User.objects.create(username=username,email=email)
            user_obj.set_password(password)
            user_obj.save()

            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user=user_obj,auth_token = auth_token)
            profile_obj.save()
            send_mail_for_verification(email=email, token=auth_token)
            return redirect('token')
        
        except Exception as e:
            print(e)



    return render(request, 'register2.html')
    
    
    
def token(request):
    return render(request, 'token.html')
    
    
    
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
    
def verify(request, auth_token):

    profile_obj = Profile.objects.filter(auth_token = auth_token).first()

    if profile_obj:
        if profile_obj.is_verified:
            messages.success(request, 'Your account is already verified')
            return redirect('login2')
        
        profile_obj.is_verified = True
        profile_obj.save()
        messages.success(request,'Your account has been verifed')
        return redirect('login2')

    else:
        return redirect('error')
    
def error(request):
    return render(request, 'error.html')
    
    
def success2(request):
    return render(request, 'success2.html')
    
    
#old urls


'''urlpatterns = [
    path('',views.Home.as_view(),name='home'),
    path('login/',views.CustomLoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),
    path('register/',views.CustomRegisterView.as_view(),name='register'),
    path('mail/',views.SendMailView.as_view(),name='mail'),

]'''


#unwanted libaries


from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import TemplateView
import django_mailbox


