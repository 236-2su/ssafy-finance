from django.db import models
from django.utils import timezone

class NewsArticle(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField()
    summary = models.TextField(blank=True)
    url = models.URLField(unique=True)
    published_date = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=100, blank=True)
    source = models.CharField(max_length=100, default='Naver Finance')
    image_url = models.URLField(blank=True, null=True)
    
    class Meta:
        ordering = ['-published_date']
        
    def __str__(self):
        return self.title
