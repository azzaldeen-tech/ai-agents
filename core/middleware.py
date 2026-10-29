from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from core.app_links import AppLinks


class ApprovalCompanyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # تنفيذ التحقق فقط للمستخدمين المسجلين وليس لمسؤولي النظام (Superusers)
        if request.user.is_authenticated :
            user = request.user

            # 1. قائمة المسارات المستثناة لمنع التوجيه اللانهائي
            # تشمل صفحات إكمال البيانات، تسجيل الخروج، والملفات الثابتة
            excluded_paths = [
                reverse(AppLinks.WAITING_APPROVAL),
                reverse(AppLinks.Auth.LOGOUT),
                '/admin/',
                '/static/',
                '/media/',
            ]

            # إذا كان المسار الحالي ليس من المسارات المستثناة
            if user.is_company and not any(request.path.startswith(path) for path in excluded_paths):
                profile = user.profile
                if profile and not user.is_fully_active:
                    messages.warning(request, _("!! Sorry, your registration request is under review.") )
                    return redirect(AppLinks.WAITING_APPROVAL)


        response = self.get_response(request)
        return response