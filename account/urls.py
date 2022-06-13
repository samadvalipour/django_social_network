from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('registration/', views.UserRegistration.as_view(), name='registration'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.UserLogout.as_view(), name='logout'),
    path('profile/<int:user_id>', views.UserProfile.as_view(), name='profile'),
    path('post/<slug:post_slug>/<int:post_id>/', views.PostDetail.as_view(), name='post_detail'),
    path('post/delete/<int:post_id>', views.DeletePost.as_view(), name='post_delete'),
    path('post/update/<int:post_id>', views.UpdatePost.as_view(), name='post_update'),
    path('post/create/', views.CreatePost.as_view(), name='post_create'),
    path('follow/<int:user_id>', views.FollowUser.as_view(), name='user_follow'),
    path('unfollow/<int:user_id>', views.UnfollowUser.as_view(), name='user_unfollow'),
    path('post/comment/<int:post_id>', views.CreateComment.as_view(), name='comment_create'),
    path('post/reply/<int:post_id>/<int:comment_id>', views.CreateReply.as_view(), name='reply_create'),
    path('post/like/<int:post_id>', views.LikePost.as_view(), name='post_like'),
    
]