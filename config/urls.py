"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import redirect_by_role # استيراد دالة التوجيه
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

admin.site.site_header = _("Labor Market Trends Analysis")
admin.site.site_title = _("Dashboard")
admin.site.index_title = _("Welcome to the Dashboard")



urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path("__reload__/", include("django_browser_reload.urls")),
]

# الروابط التي تترجم وتظهر بادئة اللغة في رابطها (مثل /ar/ و /en/)
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('accounts/account/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
    path('', include('core.urls')),

    # === [AUTO_GENERATED_URLS_START] ===

    path('companies/', include('companies.urls')),
    path('members/', include('members.urls')),

    # === [AUTO_GENERATED_URLS_END] ===
    # هذا الخيار يمنع ظهور /ar/ في الرابط للغة الافتراضية إذا أردت ذلك
    # ولكن يفضل تركه False لتجبر النظام على إدراك اللغة
    prefix_default_language=True,
)
# إعدادات الملفات الساكنة والوسائط في وضع التطوير
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)