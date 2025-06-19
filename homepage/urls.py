"""
URL configuration for mywebsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
import os
from homepage import views

def sitemap(request):
    """Generate sitemap.xml"""
    urls = [
        {'loc': '/', 'priority': '1.0', 'changefreq': 'weekly'},
        {'loc': '/galeri/', 'priority': '0.8', 'changefreq': 'weekly'},
        {'loc': '/iletisim/', 'priority': '0.8', 'changefreq': 'monthly'},
        {'loc': '/hakkimizda/', 'priority': '0.7', 'changefreq': 'monthly'},
        {'loc': '/ekibimiz/', 'priority': '0.7', 'changefreq': 'monthly'},
    ]
    
    sitemap_xml = render_to_string('sitemap.xml', {
        'urls': urls,
        'domain': request.get_host()
    })
    
    return HttpResponse(sitemap_xml, content_type='application/xml')

def robots_txt(request):
    """Serve robots.txt"""
    robots_content = """User-agent: *
Allow: /

# Sitemap
Sitemap: https://{}/sitemap.xml

# Disallow admin area
Disallow: /admin/

# Disallow static files that don't need indexing
Disallow: /static/admin/
Disallow: /media/""".format(request.get_host())
    
    return HttpResponse(robots_content, content_type='text/plain')

urlpatterns = [
    path('', views.home, name='home'),
    path('galeri/', views.galeri, name='galeri'),
    path('iletisim/', views.iletisim, name='iletisim'),
    path('hakkimizda/', views.hakkimizda, name='hakkimizda'),
    path('ekibimiz/', views.ekibimiz, name='ekibimiz'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('contact-submit/', views.contact_form_submit, name='contact_submit'),
    path('contact-list/', views.contact_list, name='contact_list'),
    path('contact-delete/<int:contact_id>/', views.delete_contact, name='delete_contact'),
    path('change-password/', views.change_password, name='change_password'),
    path('sitemap.xml', sitemap, name='sitemap'),
    path('robots.txt', robots_txt, name='robots'),
    path('admin/', admin.site.urls),
]
