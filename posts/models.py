from django.db import models
from authentication.models import Profile


# Create your models here.

class AuthorManager(models.Manager):
    def create_author(self, email, password, **kwargs):        
        #Create Profile
        new_profile = Profile.objects.create_user(
            email=email, 
            password=password, 
            username=email)        
        #new_profile.token_generated = password
        new_profile.save()
        #Create Model
        new_entity = Author.objects.create(user=new_profile, **kwargs)
        new_entity.save()
        return new_entity

class Author(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True)

    objects = AuthorManager()

    def __str__(self):
        return '%s %s' % (self.name, self.last_name)

class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

