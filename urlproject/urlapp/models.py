from django.db import models

class Url(models.Model):
    url =models.URLField()
    short_code=models.CharField(max_length=10, unique=True)
    create_time=models.DateTimeField(auto_now_add=True)
    validity =models.IntegerField(default=30)
    clicks=models.IntegerField(default=0)

class Detail(models.Model):
    short=models.ForeignKey(Url, on_delete=models.CASCADE)
    click_time=models.DateTimeField(auto_now_add=True)
    referrer=models.CharField(max_length=255, blank=True, null=True)
    location=models.CharField(max_length=255, blank=True, null=True)
