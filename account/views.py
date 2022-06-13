
from math import fabs
from django.shortcuts import redirect, render,get_object_or_404
from django.views import View
from account.forms import LoginForm, RegistrationForm, PostCreateUpdateForm, CommentCreateForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post,Comment,Like
from .models import FollowRelation

class UserRegistration(View):

    def get(self,request):
        return redirect("home:home")

    def post(self,request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'],cd['email'],cd['password'])
            messages.success(request,"ثبت نام با موفقیت انجام شد",'success')
            return redirect('home:home')
        else:
            messages.error(request,form.errors.get("__all__")[0],'error')
            return redirect('home:home')

class UserLogin(View):

    def get(self,request):
        messages.warning(request,"لطفا وارد شوید و در صورتی که حساب کاربری ندارید ثبت نام کنید.",'warning')
        return redirect("home:home")

    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd["username"], password=cd["password"])
            print("user  :  ",user)
            if user is not None:
                login(request,user)
                messages.success(request,"ورود با موفقیت انجام شد",'success')
                return redirect('home:home')

            else:
                messages.error(request,"نام کاربری یا رمز عبور اشتباه است",'error')
                return redirect('home:home')
        else:
            messages.error(request,"لطفا فرم را به درستی پر کنید",'error')
            return redirect('home:home')

class UserLogout(LoginRequiredMixin,View):
    def get(self,request):
        logout(request)
        messages.success(request,"با موفقیت خارج شدید",'success')
        return redirect("home:home")

class UserProfile(LoginRequiredMixin,View):
    def get(self,request,user_id):
        user = get_object_or_404(User,pk=user_id)
        user_posts=user.posts.all()
        relaion = FollowRelation.objects.filter(from_user=request.user,to_user=user).exists()
        return render(request,"account/profilepage.html",{"user":user,"posts":user_posts,"relation":relaion})

class PostDetail(View):
    def get(self,request,post_slug,post_id):
        post = get_object_or_404(Post,pk=post_id,slug=post_slug)
        Comments = post.postcomment.filter(isreply=False)
        if request.user.is_authenticated:
            can_like = post.can_like(request.user)
        else:
            can_like = True
        return render(request,"account/postdetail_page.html",{"post":post,"comments":Comments,"can_like":can_like})

class DeletePost(View):
    def get(self,request,post_id):
        post = get_object_or_404(Post,pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request,"پست با موفقیت حذف شد",'success')
        else:
            messages.error(request,"شما نمیتوانید این پست را حذف کنید",'error')
        return redirect('home:home')

class UpdatePost(LoginRequiredMixin,View):
    form_class = PostCreateUpdateForm

    def setup(self, request, *args,**kwargs):
        self.post_instance = get_object_or_404(Post,pk=kwargs["post_id"])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self,request,*args,**kwargs):
        if self.post_instance.user.id != request.user.id:
            messages.error(request,"شما نمیتوانید این پست را ویرایش کنید","error")
            return redirect("home:home")
        return super().dispatch(request,*args,**kwargs)

    def get(self,request,post_id):
        form = self.form_class(initial={"title":self.post_instance.title,"body":self.post_instance.body})
        return render(request,"account/updatepost.html",{"form":form})
        
    def post(self,request,post_id):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            self.post_instance.title = cd["title"]
            self.post_instance.body = cd["body"]
            self.post_instance.save()
            messages.success(request,"پست با موفقیت ویرایش شد","success")
            return redirect("home:home")
        else:
            messages.error(request,"لطفا فرم را به درستی پر کنید","error")
            return redirect("account:post_update",post_id)
            
class CreatePost(LoginRequiredMixin,View):
    def get(self,request):
        form = PostCreateUpdateForm()
        return render(request,"account/createpost.html",{"form":form})
    def post(self,request):
        form = PostCreateUpdateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post = Post(title=cd["title"],body=cd["body"],user=request.user)
            post.slug=request.user.username
            post.save()
            messages.success(request,"پست با موفقیت ایجاد شد",'success')
            return redirect('home:home')
        else:
            messages.error(request,"لطفا فرم را به درستی پر کنید",'error')
            return redirect('home:home')

class FollowUser(LoginRequiredMixin,View):
    def get(self,request,user_id):
        user = User.objects.get(pk=user_id)
        relation = FollowRelation.objects.filter(from_user=request.user,to_user=user)
        if relation.exists():
            messages.error(request,"شما قبلا این کاربر را دنبال کرده اید","error")
        else:
            relation = FollowRelation(from_user=request.user,to_user=user)
            relation.save()
            messages.success(request,"شما با موفقیت این کاربر را دنبال کردید","success")
        return redirect("account:profile",user_id)

class UnfollowUser(LoginRequiredMixin,View):
    def get(self,request,user_id):
        user = User.objects.get(pk=user_id)
        relation = FollowRelation.objects.filter(from_user=request.user,to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request,"شما با موفقیت این کاربر را انفالو کردید","success")
        else:
            messages.error(request,"شمااین کاربر را فالو نکرده اید","error")
        return redirect("account:profile",user_id)

class CreateComment(LoginRequiredMixin,View):
    
    def setup(self, request, *args,**kwargs):
        self.post_instance = get_object_or_404(Post,pk=kwargs["post_id"])
        return super().setup(request, *args, **kwargs)

    def get(self,request,post_id):
        form = CommentCreateForm()
        return render(request,"account/createcomment_page.html",{"form":form,"post":self.post_instance,"iscreatecommentpage":True})
    def post(self,request,post_id):
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            comment = Comment(user=request.user,post=self.post_instance,body=cd["body"])
            comment.save()
            messages.success(request,"نظر شما با موفقیت ارسال شد","success")
        else:
            messages.error(request,"نظر شما ارسال نشد","error")
        return redirect("account:post_detail",self.post_instance.slug,self.post_instance.id)


class CreateReply(LoginRequiredMixin,View):
    
    def setup(self, request, *args,**kwargs):
        self.post_instance = get_object_or_404(Post,pk=kwargs["post_id"])
        self.comment_instance = get_object_or_404(Comment,pk=kwargs["comment_id"])
        return super().setup(request, *args, **kwargs)

    def get(self,request,*args,**kwargs):
        form = CommentCreateForm()
        return render(request,"account/createcomment_page.html",{"form":form,"post":self.comment_instance,"iscreatereplypage":True})

    def post(self,request,*args,**kwargs):
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            comment = Comment(user=request.user,post=self.post_instance,reply=self.comment_instance,body=cd["body"],isreply=True)
            comment.save()
            messages.success(request,"نظر شما با موفقیت ارسال شد","success")
        else:
            messages.error(request,"نظر شما ارسال نشد","error")
        return redirect("account:post_detail",self.post_instance.slug,self.post_instance.id)

class LikePost(LoginRequiredMixin,View):

    def get(self,request,post_id):
        post = get_object_or_404(Post,pk=post_id)
        relation = Like.objects.filter(user=request.user,post=post)
        if relation.exists():
            relation.delete()
        else:
            relation = Like(user=request.user,post=post)
            relation.save()
        return redirect("account:post_detail",post.slug,post.id)
