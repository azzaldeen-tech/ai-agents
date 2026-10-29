from companies.Utils.companyServices import CompanyService
from companies.decorators import company_required
from django.contrib.auth.decorators import login_required


def stats_processor(request):
    # إزالة @login_required و @member_required تماماً

    # التحقق يدويًا
    if not request.user.is_authenticated:
        return {}

    try:

        profile = getattr(request.user, 'company_profile', None)

        if profile:

            return {
                'company_global_stats': CompanyService.get_global_stats(profile.id)
            }
    except Exception:
        pass

    return {}