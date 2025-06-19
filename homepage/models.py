from django.db import models
from django.utils import timezone

# Create your models here.

class Contact(models.Model):
    SERVICE_CHOICES = [
        ('yazılım', 'Yazılım'),
        ('donanım', 'Donanım'),
        ('danışmanlık', 'Danışmanlık'),
    ]
    
    first_name = models.CharField(max_length=100, verbose_name='Ad')
    last_name = models.CharField(max_length=100, verbose_name='Soyad')
    phone = models.CharField(max_length=20, verbose_name='Telefon')
    email = models.EmailField(verbose_name='E-posta')
    service = models.CharField(max_length=20, choices=SERVICE_CHOICES, verbose_name='Hizmet')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Oluşturulma Tarihi')
    
    class Meta:
        verbose_name = 'İletişim Formu'
        verbose_name_plural = 'İletişim Formları'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.service}"
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    full_name.short_description = 'Ad Soyad'

class Blog(models.Model):
    CATEGORY_CHOICES = [
        ('haberler', 'Haberler'),
        ('makaleler', 'Makaleler'),
        ('teknoloji', 'Teknoloji'),
        ('danışmanlık', 'Danışmanlık'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Başlık')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL')
    content = models.TextField(verbose_name='İçerik')
    excerpt = models.TextField(max_length=300, blank=True, verbose_name='Özet')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name='Kategori')
    image = models.ImageField(upload_to='blog/', blank=True, null=True, verbose_name='Görsel')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Yazar')
    is_published = models.BooleanField(default=False, verbose_name='Yayınlandı')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Oluşturulma Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')
    
    class Meta:
        verbose_name = 'Blog Yazısı'
        verbose_name_plural = 'Blog Yazıları'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f'/blog/{self.slug}/'
