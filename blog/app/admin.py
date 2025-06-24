from django.contrib import admin
from app.models import GeneralInfo, Service, Testimonial, FrequentlyAskedQuestion, ContactFormLog, Blog, Author

# Register your models here.
@admin.register(GeneralInfo)
class GeneralInfoAdmin(admin.ModelAdmin):
    
    list_display = ('company_name', 'company_address', 'email', 'phone', 'open_hours')

    def has_add_permission(self, request, obj=None):
        # Disable the add button
        return False

    def has_delete_permission(self, request, obj=None):
        # Disable the delete button
        return False

    def has_change_permission(self, request, obj=None):
        # Disable the change button
        return True

    def has_view_permission(self, request, obj=None):
        # Disable the view button
        return True

    readonly_fields = [
        'company_name'
    ]

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title',)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'user_job_title', 'display_rating_count')
    search_fields = ('user_name', 'user_job_title')
    def display_rating_count(self, obj):
        return "*" * obj.rating_count
    display_rating_count.short_description = 'Rating'

@admin.register(FrequentlyAskedQuestion)
class FrequentlyAskedQuestionAdmin(admin.ModelAdmin):
    list_display = ('question','answer')
    search_fields = ('question',)

@admin.register(ContactFormLog)
class ContactFormLogAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_at', 'is_successful', 'is_error')
    def has_add_permission(self, request, obj=None):
        # Disable the add button
        return False
    def has_delete_permission(self, request, obj=None): 
        # Disable the delete button
        return False        
    def has_change_permission(self, request, obj=None):
        # Disable the change button
        return False

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('author', 'category', 'title', 'blog_image', 'created_at')

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'joined_date')
    search_fields = ('first_name', 'last_name')
    
  