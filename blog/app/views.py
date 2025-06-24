from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib import messages
from datetime import datetime
from app.models import GeneralInfo, Service, Testimonial, FrequentlyAskedQuestion, ContactFormLog, Blog
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.
def index(request):
    general_info = GeneralInfo.objects.first()
    services = Service.objects.all()
    testimonials = Testimonial.objects.all()
    faqs = FrequentlyAskedQuestion.objects.all()
    recents_blogs = Blog.objects.all().order_by("-created_at")[:3]  # Get the 3 most recent blogs
    for blog in recents_blogs:
        print(f"blog: {blog}")
        print(f"blog.created_at: {blog.created_at}")
        print(f"blog.author: {blog.author}")
        print(f"blog.author.country: {blog.author.country}")
        print("")
    default_value = ""
    context = {
        "location": getattr(general_info,"company_address", default_value),
        "email": getattr(general_info,"email" , default_value),
        "phone": getattr(general_info,"phone", default_value),
        "open_hours": getattr(general_info, "open_hours", default_value),
        "video_url": getattr(general_info, "video_url", default_value),
        "twitter_url": getattr(general_info, "twitter_url", default_value),
        "facebook_url": getattr(general_info, "facebook_url", default_value),
        "instagram_url": getattr(general_info, "instagram_url", default_value),
        "linkedin_url": getattr(general_info, "linkedin_url", default_value),
        "company_name": getattr(general_info, "company_name", default_value),
        "services": services, 
        "testimonials": testimonials,
        "faqs": faqs,
        "recents_blogs": recents_blogs,
    }
    #print("Context data:", context)  # Debugging line to check context data
    return render(request, 'index.html', context)

def contact_form(request):

    if request.method == 'POST':
        print("\nContact form data received:")
        print(f"request.POST = {request.POST}")
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        context = {
            "name": name,
            "email": email,
            "subject": subject,
            "message": message,
        }
        html_content = render_to_string('email.html', context)
        is_successful = False
        is_error = False
        error_message = ""
        try:
            send_mail(
                subject = subject,
                message = None,  # No plain text message
                html_message = html_content,  # HTML content for the email
                from_email = settings.EMAIL_HOST_USER,
                recipient_list = [settings.EMAIL_HOST_USER],
                fail_silently = False,  # Default is True
            )
        except Exception as e:
            is_error = True
            error_message = str(e)
            messages.error(request, "There was an error sending your message. Please try again later.")
        else:
            is_successful = True
            messages.success(request, "Your message has been sent successfully!")

        ContactFormLog.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message,
            submitted_at=timezone.now(),
            is_successful= is_successful,
            is_error= is_error,
            error_message=error_message ,
        )
    # if request.method == 'GET':
    #     print("\nContact form data is accessed using URL") 
    return redirect('home')

def blog_detail(request, blog_id):
    try:
        blog = Blog.objects.get(id=blog_id)
    except Blog.DoesNotExist:
        return HttpResponse("Blog not found", status=404)

    recents_blogs = Blog.objects.all().exclude(id=blog.id).order_by("-created_at")[:2]

    context = {
        "blog": blog,
        "recents_blogs": recents_blogs,
    }
    return render(request, 'blog_detail.html', context)

def blogs(request):
    all_blogs = Blog.objects.all().order_by("-created_at")
    blogs_per_page = 3  # Number of blogs to display per page
    paginator = Paginator(all_blogs, blogs_per_page)  # Show 3 blogs per page
    page = request.GET.get('page')
    # print(f"page: {page}")
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)
    # print(f"paginator>num_pages: {paginator.num_pages}")
    context = {
        "all_blogs": blogs,
    }
    return render(request, 'blogs.html', context)