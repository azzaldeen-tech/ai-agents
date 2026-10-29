from django.contrib.auth.models import AbstractUser, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.helpers import get_identities_apps, get_identities_dashboards, get_url_view, app_is_exists, \
    get_identity_app_name
from core.app_links  import AppLinks
from .base_models import *
from django.contrib.auth.base_user import BaseUserManager



class Role(BaseRole):

    permissions = models.ManyToManyField(Permission, blank=True, verbose_name=_("Permissions"))
    is_identity = models.BooleanField(default=True)
    requires_approval = models.BooleanField(
        default=False,
        verbose_name = _("Require Approval"),
        help_text=_("Does a member of this role need administrative approval before activating their account?")
    )

    view_in_register = models.BooleanField(default=False, verbose_name=_("Show in Register"))

    def __str__(self):
        return self.name

    def get_all_permissions(self):
        """إرجاع قائمة بجميع codenames الصلاحيات المرتبطة بهذا الدور"""
        return list(self.permissions.values_list('codename', flat=True))

    def has_permission(self, perm_codename):
        """
        التحقق من الصلاحية باستخدام codename الخاص بـ Django
        """
        return self.permissions.filter(codename=perm_codename).exists()

    def needs_manual_activation(self):
        """هل هذا الدور يتطلب موافقة الإدارة قبل السماح للمستخدم بالعمل؟"""
        return self.requires_approval


    @classmethod
    def get_public_roles(cls):
        """جلب الأدوار المسموح للمستخدمين اختيارها عند التسجيل"""
        return cls.objects.filter(view_in_register=True)

    def get_permissions_for_model(self, model_name):
        """جلب الصلاحيات المرتبطة بموديل معين فقط"""
        return self.permissions.filter(content_type__model=model_name)

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(BaseCustomUser):

    objects = CustomUserManager()

    identity = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        limit_choices_to={'is_identity': True},  # لا يظهر هنا إلا الهويات
        verbose_name="Identity type",
        related_name="identity_users"
    )


    @property
    def profile(self):
        if self.identity and self.identity.code:
            return getattr(self, f'{self.identity.code}_profile', None)
        return None

    @property
    def display_name(self):
        name= "".join([n for n in self.username[:1]]).upper() if not self.profile else self.profile.name
        return  name

    def has_role(self, role_code):
        """
        التحقق من دور المستخدم الحالي (0% أخطاء - تعامل مباشر مع ForeignKey)
        """
        if not self.identity:
            return False
        return self.identity.code == role_code

    @property
    def is_company(self):
        return self.has_role('company')

    @property
    def is_member(self):
        return self.has_role('member')

    @property
    def is_fully_active(self):
        """
        التحقق من التفعيل بناءً على الهوية الواحدة (Identity) والبروفايل:
        """
        # 1. إذا لم يكن للمستخدم هوية أصلاً
        if not self.identity:
            return False

        # 2. إذا كانت الهوية لا تتطلب موافقة (مثل طالب) -> مفعل فوراً
        if not self.identity.requires_approval:
            return True

        # 3. إذا كانت تتطلب موافقة (مثل شركة) -> نتحقق من البروفايل المرتبط
        # نستخدم self.profile الذي يعمل عبر GenericForeignKey
        if self.profile and hasattr(self.profile, 'is_verified'):
            return self.profile.is_verified

        # الافتراضي: غير مفعل حتى يثبت العكس
        return False

    @property
    def is_identity(self):
        if not self.identity:
            return False
        return getattr(self.identity, 'is_identity', False)



    @property
    def get_app_name(self):
        if self.is_authenticated and self.is_identity:
            role_code = getattr(self.identity, 'code', None)
            if role_code:
                app_name =  get_identity_app_name(role_code)
                if app_name:
                    return app_name
        return None


    @property
    def get_dashboard_url(self):
        if self.is_authenticated and self.is_identity:
            role_code = getattr(self.identity, 'code', None)
            if role_code:
                app_name = self.get_app_name
                if role_code and app_is_exists(app_name):
                    dashboards = get_identities_dashboards()
                    if dashboards:
                        dashboard_url = dashboards.get(role_code, AppLinks.Core.HOME)
                        return get_url_view(dashboard_url)

        return None

