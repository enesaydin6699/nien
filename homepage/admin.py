from django.contrib import admin
from .models import Contact, Blog

# Register your models here.

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'service', 'created_at']
    list_filter = ['service', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Kişisel Bilgiler', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Hizmet Bilgileri', {
            'fields': ('service',)
        }),
        ('Sistem Bilgileri', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'is_published', 'created_at']
    list_filter = ['category', 'is_published', 'created_at', 'author']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('İçerik', {
            'fields': ('title', 'slug', 'content', 'excerpt', 'image')
        }),
        ('Kategori ve Yazar', {
            'fields': ('category', 'author')
        }),
        ('Yayın Durumu', {
            'fields': ('is_published',)
        }),
        ('Sistem Bilgileri', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
