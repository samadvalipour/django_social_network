from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="usercomment")
    post = models.ForeignKey('Post',on_delete=models.CASCADE,related_name="postcomment")
    reply = models.ForeignKey('self',on_delete=models.CASCADE,related_name="replycomment",blank=True,null=True)
    isreply = models.BooleanField(default=False)
    body = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.body}"

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="posts")
    title = models.CharField(max_length=255)
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created"]
    def __str__(self) -> str:
        return self.slug

    def get_absolute_url(self):
        return reverse("account:post_detail", args=(self.slug, self.id))
