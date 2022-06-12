from django.shortcuts import render
from .models import Post
from django.views import View
from account.forms import RegistrationForm,LoginForm

class HomeView(View):
    def get(self,request):
        registrationform = RegistrationForm()
        loginform = LoginForm()
        all_posts = Post.objects.all()
        return render(request,'home/index.html',context={'title':'home','registrationform':registrationform,'loginform':loginform,"posts":all_posts})
   
    def post(self,request):
        return render(request,'home/index.html',context={"title":"home" })
