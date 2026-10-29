
from members.Utils.services import MemberService


def stats_processor(request):
    # إزالة @login_required و @member_required تماماً

    # التحقق يدويًا
    if not request.user.is_authenticated:
        return {}

    try:
        # الوصول للعلاقة (تأكد من الاسم الصحيح في الموديل، غالباً member_profile)
        # استخدم getattr لتجنب توقف الكود إذا لم يكن للمستخدم بروفايل عضو
        profile = getattr(request.user, 'member_profile', None)

        if profile:
            return {
                'member_global_stats': MemberService.get_global_stats(profile.id)
            }
    except Exception:
        pass


    return {}