from django.db import models
from django.contrib.auth.models import User

class FollowRelation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')   

    def __str__(self):
        return '{} follows {}'.format(self.from_user, self.to_user)