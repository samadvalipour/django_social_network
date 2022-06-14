from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="userlike")
    post = models.ForeignKey('post',on_delete=models.CASCADE,related_name="postlike")

    def __str__(self):
        return f"{self.user} liked {self.post}"

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="usercomment")
    post = models.ForeignKey('Post',on_delete=models.CASCADE,related_name="postcomment")
    reply = models.ForeignKey('self',on_delete=models.CASCADE,related_name="replycomment",blank=True,null=True)
    isreply = models.BooleanField(default=False)
    body = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.body}"

    def reply_count(self):
        return self.replycomment.count()

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

    def comment_count(self):
        return self.postcomment.count()

    def like_count(self):
        return self.postlike.count()
    
    def can_like(self,user):
        return not self.postlike.filter(user=user).exists()
