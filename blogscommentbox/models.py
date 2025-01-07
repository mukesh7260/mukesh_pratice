from django.db import models
from account.models import User
from blogsapi.models import Blogs
# Create your models here.
class BlogsComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blogs = models.ForeignKey(Blogs, on_delete=models.CASCADE, related_name='comments',null=False)
    date = models.CharField(max_length=10)
    comment = models.TextField()
