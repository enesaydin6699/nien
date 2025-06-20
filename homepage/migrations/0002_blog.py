# Generated by Django 5.2.3 on 2025-06-18 13:21

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Başlık')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='URL')),
                ('content', models.TextField(verbose_name='İçerik')),
                ('excerpt', models.TextField(blank=True, max_length=300, verbose_name='Özet')),
                ('category', models.CharField(choices=[('haberler', 'Haberler'), ('makaleler', 'Makaleler'), ('teknoloji', 'Teknoloji'), ('danışmanlık', 'Danışmanlık')], max_length=20, verbose_name='Kategori')),
                ('image', models.ImageField(blank=True, null=True, upload_to='blog/', verbose_name='Görsel')),
                ('is_published', models.BooleanField(default=False, verbose_name='Yayınlandı')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Oluşturulma Tarihi')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Yazar')),
            ],
            options={
                'verbose_name': 'Blog Yazısı',
                'verbose_name_plural': 'Blog Yazıları',
                'ordering': ['-created_at'],
            },
        ),
    ]
