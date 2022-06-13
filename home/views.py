from django.shortcuts import render
from .models import Post
from django.views import View
from account.forms import RegistrationForm,LoginForm
from home.forms import SearchForm

class HomeView(View):
    def get(self,request):
        registrationform = RegistrationForm()
        loginform = LoginForm()
        searchform = SearchForm()
        all_posts = Post.objects.all()
        search = request.GET.get("search")
        if search:
            all_posts = Post.objects.filter(body__icontains=search)
        return render(request,'home/index.html',context={'title':'home','registrationform':registrationform,'loginform':loginform,"posts":all_posts,"is_homepage":True,"searchform":searchform})
