from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
# Create your models here.
class GeneralInfo(models.Model):
    company_name = models.CharField(max_length=255, default='My Company')
    company_address = models.CharField(max_length=255, default='123 Main St, Anytown, USA')
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    open_hours = models.CharField(max_length=100, default='9 AM - 5 PM')
    video_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.company_name

class Service(models.Model):
    icon = models.CharField(max_length=255,blank=True, null=True)
    title = models.CharField(max_length=255,unique=True)
    description = models.TextField()
    
    def __str__(self):
        return self.title

class Testimonial(models.Model):
    user_image = models.CharField(max_length=255,blank=True, null=True)
    stars_count = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    rating_count = models.IntegerField(choices=stars_count)
    user_name = models.CharField(max_length=255)
    user_job_title = models.CharField(max_length=255)
    review = models.TextField()
    def __str__(self):
        return f"{self.user_name} - {self.user_job_title}"

class FrequentlyAskedQuestion(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    
    def __str__(self):
        return self.question
    
class ContactFormLog(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255) 
    subject = models.CharField(max_length=255)
    message = models.TextField()
    submitted_at = models.DateTimeField(null=True, blank=True)
    is_successful = models.BooleanField(default=False)
    is_error = models.BooleanField(default=False)
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.email

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True, null=True)
    joined_date = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.first_name

class Blog(models.Model):
    blog_image = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.PROTECT, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    content = RichTextField()   #models.TextField()
    def __str__(self):
        return self.title