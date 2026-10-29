from django.contrib import admin
from django.utils.html import format_html
from companies.models import JobApplication, CompanyProfile, Job
from django.utils.translation import gettext_lazy as _

from core.base_admin import BaseModelAdmin


# Register your models here.



# Register your models here.
@admin.register(CompanyProfile)
class CompanyProfileAdmin(BaseModelAdmin):
    list_display = (
        'view_logo',
        'name',
        'user',
        'location',
        'is_verified',
        # 'status'
    )
    search_fields = ('name','user__email')
    list_filter = ('location','is_verified')
    list_editable = ('is_verified',)

    def view_logo(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="width: 40px; height: 40px; border-radius: 8px; object-fit: cover; border: 1px solid #ddd;" />',
                obj.logo.url
            )
        return _("No Logo")

    view_logo.short_description = _("Logo")


@admin.register(Job)
class JobAdmin(BaseModelAdmin):
    list_display = ('title', 'company', 'category', 'city','employment_type','min_salary','is_active')
    search_fields = ('title', 'company', 'category', 'city','employment_type','required_skills')
    list_filter = ('employment_type','experience_level','category', 'city',)


@admin.register(JobApplication)
class JobApplicationAdmin(BaseModelAdmin):
    list_display = ('job', 'member', 'applied_at', 'status')
    # search_fields = ('name',)
    list_filter = ('job', 'status')
