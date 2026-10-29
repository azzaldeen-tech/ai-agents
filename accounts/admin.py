
from django.contrib.auth.admin import UserAdmin

from core.models import Skill
from core.base_admin import BaseModelAdmin, BaseTabularInline
from .models import CustomUser
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from allauth.socialaccount.admin import (
    SocialAppAdmin as OldSocialAppAdmin,
    SocialAccountAdmin as OldSocialAccountAdmin,
    SocialTokenAdmin as OldSocialTokenAdmin,
)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # عرض الحقول الجديدة في صفحة التعديل
    fieldsets = UserAdmin.fieldsets + (
        (_('Additional settings'), {'fields': ('is_dark_mode', 'language_preference')}),
    )
    # عرض الحقول في قائمة المستخدمين الرئيسية
    list_display = ['username', 'email', 'is_dark_mode', 'is_staff']

admin.site.register(CustomUser, CustomUserAdmin)





# إلغاء التسجيل القديم لتجنب التكرار
# admin.site.unregister(SocialApp)
# admin.site.unregister(SocialAccount)
# admin.site.unregister(SocialToken)
#
# # إعادة التسجيل باستخدام تنسيق Unfold
# @admin.register(SocialApp)
# class SocialAppAdmin(OldSocialAppAdmin, ModelAdmin):
#     pass
#
# @admin.register(SocialAccount)
# class SocialAccountAdmin(OldSocialAccountAdmin, ModelAdmin):
#     pass
#
# @admin.register(SocialToken)
# class SocialTokenAdmin(OldSocialTokenAdmin, ModelAdmin):
#     pass