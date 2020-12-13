from django.db import models











# • Profile: id, name, email, address { street, suite, city, zipcode } ;
# • Comment: id, name, email, body, postId;
# • Post: id, title, body, userId.

class Profile(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField()
    street = models.CharField(max_length=128)
    city = models.CharField(max_length=64)
    zipcode = models.CharField(max_length=9)


class Post(models.Model):
    title = models.CharField(max_length=32)
    body = models.CharField(max_length=256)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Comment(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField()
    body = models.CharField(max_length=256)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
