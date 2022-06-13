from django.contrib import admin
from .models import Post,Comment,Like

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id","user",'slug','created','updated']
    search_fields = ("slug",)
    list_filter = ("created","updated")
    prepopulated_fields = {'slug':('title',)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["user","post","isreply","created"]
    raw_id_fields = ["user","post","reply"]

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ["user","post"]
    raw_id_fields = ["user","post"]

