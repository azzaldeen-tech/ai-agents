
import json
from django.db.models import Count, Avg, Q, F
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta
from core.models import Skill, SkillCategory, City
# from companies.models import Job, JobApplication , CompanyProfile
from django.db.models import Count
# from members.models import MemberProfile
import logging
logger = logging.getLogger(__name__)


def build_job_filters(request_params):
    filters = Q()

    # 1. الاحتياط الأول والأقوى: التحقق من وجود الكائن نفسه وأنه ليس None أو فارغاً
    if request_params is None:
        return filters

    # 2. الاحتياط الثاني: التأكد من أن الكائن يمتلك دالة "get" (لحمايتك من خطأ WSGIRequest السابق)
    if not hasattr(request_params, 'get'):
        # إذا تم تمرير كائن request كاملاً بالخطأ، نقوم باستخراج GET منه تلقائياً كخطة بديلة (Fallback)
        if hasattr(request_params, 'GET') and hasattr(request_params.GET, 'get'):
            params = request_params.GET
        else:
            # إذا لم يكن هذا ولا ذاك، نخرج بأمان ونعيد فلتر فارغ بدون كراش
            return filters
    else:
        params = request_params

    # -------------------------------------------------------------
    # 3. الفلترة الآمنة حسب المدينة (city_id)
    # -------------------------------------------------------------
    try:
        city_id = params.get('city_id')
        if city_id:  # التحقق من أن القيمة ليست فارغة أو None أو مصفوفة فارغة
            # نقوم بالتحويل المباشر مع الحماية من القوالب والمصفوفات الغريبة [1] أو ['1']
            if isinstance(city_id, list):
                city_id = city_id[0] if city_id else None

            city_id_int = int(str(city_id).strip())
            if city_id_int > 0:
                filters &= Q(city_id=city_id_int)
    except (ValueError, TypeError, AttributeError, IndexError):
        # امتصاص أي خطأ أياً كان نوعه (نصوص خبيثة، كائنات غريبة، إلخ) ومتابعة الكود بأمان
        pass

    # -------------------------------------------------------------
    # 4. الفلترة الآمنة حسب المجال (category_id)
    # -------------------------------------------------------------
    try:
        category_id = params.get('category_id')
        if category_id:
            if isinstance(category_id, list):
                category_id = category_id[0] if category_id else None

            category_id_int = int(str(category_id).strip())
            if category_id_int > 0:
                filters &= Q(category_id=category_id_int)
    except (ValueError, TypeError, AttributeError, IndexError):
        pass

    # -------------------------------------------------------------
    # 5. الفلترة الآمنة حسب العام (year)
    # -------------------------------------------------------------
    try:
        year = params.get('year')
        if year:
            if isinstance(year, list):
                year = year[0] if year else None

            year_int = int(str(year).strip())
            current_year = timezone.now().year

            # حصر النطاق الزمني لمنع استعلامات قواعد البيانات المنهكة بأرقام خيالية
            if 2000 <= year_int <= current_year:
                filters &= Q(created_at__year=year_int)
    except (ValueError, TypeError, AttributeError, IndexError):
        pass

    # يعود بـ Q() صافي (جلب كل البيانات) في حال كان الطلب فارغاً أو تالفاً
    return filters
