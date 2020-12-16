from django.db import models

# • Profile: id, name, email, address { street, suite, city, zipcode } ;
# • Comment: id, name, email, body, postId;
# • Post: id, title, body, userId.


class Profile(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField()
    street = models.CharField(max_length=128)
    city = models.CharField(max_length=64)
    zipcode = models.CharField(max_length=12)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=128)
    body = models.TextField()
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField()
    body = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment {self.name}'
