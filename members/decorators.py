from django.shortcuts import redirect
from functools import wraps

from core.app_links import AppLinks


def member_required(view_func):
    """
    هذه هي الخاصية التي ستوضع فوق الدالة.
    تقوم بالتحقق: إذا لم يكن جهة تدريب، يتم التوجيه للرئيسية.
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect(AppLinks.Auth.LOGIN)

        if not request.user.is_member:
            return redirect(AppLinks.Core.HOME)

        return view_func(request, *args, **kwargs)


    return _wrapped_view