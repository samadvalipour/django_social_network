from cProfile import label
from dataclasses import field
from pyexpat import model
from statistics import mode
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from home.models import Post,Comment

class RegistrationForm(forms.Form):
    username = forms.CharField(label='نام کاربری',error_messages={'required':"این کادر نباید خالی باشد"},widget=forms.TextInput(attrs={'class':'input input-bordered','placeholder':'نام کاربری'}) )
    email = forms.CharField(label='ایمیل',error_messages={'required':"این کادر نباید خالی باشد"},widget=forms.EmailInput(attrs={'class':'input input-bordered','placeholder':'ایمیل'}) )
    password = forms.CharField(label='رمز عبور',error_messages={'required':"این کادر نباید خالی باشد"},widget=forms.PasswordInput(attrs={'class':'input input-bordered','placeholder':'رمز عبور'}) )
    confirmpassword = forms.CharField(label='تکرار رمز عبور',error_messages={'required':"این کادر نباید خالی باشد"},widget=forms.PasswordInput(attrs={'class':'input input-bordered','placeholder':'تکرار رمز عبور'}) )

    def clean(self):

        cleaned_data = super().clean()
        user_data = cleaned_data['username']
        user_existed = User.objects.filter(username=user_data).exists()
        if user_existed:
            raise ValidationError("یک کاربر با این نام کاربری موجود است",code="invalid")

        email_data = cleaned_data['email']
        email_existed = User.objects.filter(email=email_data).exists()
        if email_existed:
            raise ValidationError("یک کاربر با این ایمیل موجود است",code="invalid")

        pass1 = cleaned_data.get('password')
        pass2 = cleaned_data.get('confirmpassword')
        if pass1!=pass2:
            raise ValidationError("کادر پسورد با تکرار پسورد مشابه نیست",code="invalid")
        
class LoginForm(forms.Form):
    username = forms.CharField(label='نام کاربری',error_messages={'required':"این کادر نباید خالی باشد"},widget=forms.TextInput(attrs={'class':'input input-bordered','placeholder':'نام کاربری'}) )
    password = forms.CharField(label='رمز عبور',widget=forms.PasswordInput(attrs={'class':'input input-bordered','placeholder':'رمز عبور'}) )

class PostCreateUpdateForm(forms.Form):
    title = forms.CharField(label='عنوان',error_messages={'required':"این کادر نباید خالی باشد"},widget=forms.TextInput(attrs={'class':'form-control input input-bordered w-1/2','placeholder':'عنوان'}) )
    body = forms.CharField(label='متن',error_messages={'required':"این کادر نباید خالی باشد"},widget=forms.Textarea(attrs={'class':'form-control textarea textarea-bordered h-64','placeholder':'متن'}) )

class CommentCreateForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=["body"]
        labels={
            "body":"متن کامنت"
        }
        widgets = {
            'body':forms.Textarea(attrs={'class':'form-control textarea textarea-bordered h-32','placeholder':'متن'}),
        }