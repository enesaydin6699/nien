from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Contact, Blog
import os
from django.conf import settings

# Create your views here.

def home(request):
    return render(request, 'homepage/home.html')

def galeri(request):
    # Get the gallery folder path - now under images/gallery
    gallery_path = os.path.join(settings.BASE_DIR, 'homepage', 'static', 'homepage', 'images', 'gallery')
    
    # Debug: Print the gallery path
    print(f"Gallery path: {gallery_path}")
    print(f"Path exists: {os.path.exists(gallery_path)}")
    
    # List of supported image extensions
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    
    gallery_images = []
    
    # Check if gallery folder exists
    if os.path.exists(gallery_path):
        # Get all files in the gallery folder
        files = os.listdir(gallery_path)
        print(f"Files in gallery folder: {files}")
        
        for filename in files:
            # Check if file is an image
            if any(filename.lower().endswith(ext) for ext in image_extensions):
                # Create image data
                image_data = {
                    'filename': filename,
                    'src': f'/static/homepage/images/gallery/{filename}',
                    'caption': generate_caption_from_filename(filename)
                }
                gallery_images.append(image_data)
                print(f"Added image: {image_data}")
    else:
        print(f"Gallery folder does not exist: {gallery_path}")
    
    # Sort images by filename
    gallery_images.sort(key=lambda x: x['filename'])
    
    print(f"Total gallery images: {len(gallery_images)}")
    
    return render(request, 'homepage/galeri.html', {
        'gallery_images': gallery_images
    })

def generate_caption_from_filename(filename):
    """
    Generate a readable caption from filename
    Removes extension and converts underscores/hyphens to spaces
    """
    # Remove file extension
    name_without_ext = filename.rsplit('.', 1)[0]
    
    # Replace underscores and hyphens with spaces
    caption = name_without_ext.replace('_', ' ').replace('-', ' ')
    
    # Capitalize first letter of each word
    caption = ' '.join(word.capitalize() for word in caption.split())
    
    return caption

def iletisim(request):
    return render(request, 'homepage/iletisim.html')

def hakkimizda(request):
    return render(request, 'homepage/hakkimizda.html')

def ekibimiz(request):
    return render(request, 'homepage/ekibimiz.html')

def login_view(request):
    if request.method == 'POST':
        email_or_username = request.POST.get('email')
        password = request.POST.get('password')
        
        # Try to authenticate with username first, then email
        user = authenticate(request, username=email_or_username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_staff:
                # Redirect to admin panel if user is staff
                return redirect('/admin/')
            else:
                # Redirect to home page for regular users
                return redirect('home')
        else:
            messages.error(request, 'Geçersiz kullanıcı adı/e-posta veya şifre.')
    
    return render(request, 'homepage/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def contact_form_submit(request):
    if request.method == 'POST':
        try:
            # Debug: Print received data
            print("Received form data:")
            print("firstName:", request.POST.get('firstName'))
            print("lastName:", request.POST.get('lastName'))
            print("phone:", request.POST.get('phone'))
            print("email:", request.POST.get('email'))
            print("service:", request.POST.get('service'))
            
            contact = Contact.objects.create(
                first_name=request.POST.get('firstName'),
                last_name=request.POST.get('lastName'),
                phone=request.POST.get('phone'),
                email=request.POST.get('email'),
                service=request.POST.get('service')
            )
            print("Contact created successfully:", contact)
            return JsonResponse({'success': True, 'message': 'Form başarıyla gönderildi!'})
        except Exception as e:
            print("Error creating contact:", str(e))
            return JsonResponse({'success': False, 'message': f'Bir hata oluştu: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Geçersiz istek.'})

@login_required
def contact_list(request):
    contacts = Contact.objects.all()
    return render(request, 'homepage/contact_list.html', {
        'contacts': contacts
    })

@login_required
def delete_contact(request, contact_id):
    if request.method == 'POST':
        try:
            contact = Contact.objects.get(id=contact_id)
            contact.delete()
            return JsonResponse({'success': True, 'message': 'Form başarıyla silindi!'})
        except Contact.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Form bulunamadı.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Bir hata oluştu: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Geçersiz istek.'})

@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validate current password
        if not request.user.check_password(current_password):
            messages.error(request, 'Mevcut şifre yanlış.')
            return render(request, 'homepage/change_password.html')
        
        # Validate new password
        if new_password != confirm_password:
            messages.error(request, 'Yeni şifreler eşleşmiyor.')
            return render(request, 'homepage/change_password.html')
        
        if len(new_password) < 6:
            messages.error(request, 'Yeni şifre en az 6 karakter olmalıdır.')
            return render(request, 'homepage/change_password.html')
        
        # Change password
        request.user.set_password(new_password)
        request.user.save()
        
        # Re-login user
        login(request, request.user)
        
        messages.success(request, 'Şifreniz başarıyla değiştirildi!')
        return redirect('home')
    
    return render(request, 'homepage/change_password.html')

def blog_list(request):
    """Blog yazılarının listesi"""
    blogs = Blog.objects.filter(is_published=True).order_by('-created_at')
    
    # Kategori filtresi
    category = request.GET.get('category')
    if category:
        blogs = blogs.filter(category=category)
    
    # Arama
    search = request.GET.get('search')
    if search:
        blogs = blogs.filter(title__icontains=search) | blogs.filter(content__icontains=search)
    
    # Sayfalama
    paginator = Paginator(blogs, 6)  # Sayfa başına 6 yazı
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'blogs': page_obj,
        'categories': Blog.CATEGORY_CHOICES,
        'current_category': category,
        'search': search,
    }
    
    return render(request, 'homepage/blog_list.html', context)

def blog_detail(request, slug):
    """Blog yazısı detay sayfası"""
    blog = get_object_or_404(Blog, slug=slug, is_published=True)
    
    # Benzer yazılar
    similar_blogs = Blog.objects.filter(
        category=blog.category,
        is_published=True
    ).exclude(id=blog.id)[:3]
    
    context = {
        'blog': blog,
        'similar_blogs': similar_blogs,
    }
    
    return render(request, 'homepage/blog_detail.html', context)
