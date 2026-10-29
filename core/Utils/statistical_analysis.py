
import json
from django.db.models import Count, Avg, Q, F
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta
from core.models import Skill, SkillCategory, City
from companies.models import Job, JobApplication , CompanyProfile
from django.db.models import Count
from members.models import MemberProfile
import logging
logger = logging.getLogger(__name__)

#
# # 1. أفضل 10 مهارات طلباً
# def get_top_skills(limit=10):
#     top_skills = Skill.objects.annotate(
#         jobs_count=Count('required_skills')
#     ).order_by('-jobs_count')[:limit]
#
#     return [skill.name for skill in top_skills], [skill.jobs_count for skill in top_skills]
#
#
# # 2. توزيع الوظائف حسب القطاع (مجال الوظيفة)
# def get_top_categories():
#     top_categories = SkillCategory.objects.annotate(
#         jobs_count=Count('jobs')
#     ).order_by('-jobs_count')
#
#     return [cat.name for cat in top_categories], [cat.jobs_count for cat in top_categories]
#
def get_jobs():
    jobs = Job.objects.select_related('city').filter()[:9]
    return jobs

def get_companies(limit=-1):
    companies = CompanyProfile.objects.annotate(
        jobs_count=Count('jobs')
    ).select_related('user').filter()[:limit]
    return companies
#
# # 3. الخط الزمني للوظائف (مجمع شهرياً)
# def get_jobs_timeline():
#     timeline_data = Job.objects.annotate(
#         month=TruncMonth('created_at')
#     ).values('month').annotate(
#         count=Count('id')
#     ).order_by('month')
#
#     labels = [item['month'].strftime("%Y-%m") for item in timeline_data if item['month']]
#     data = [item['count'] for item in timeline_data]
#
#     return labels, data
#
#
# # 4. المهارات الناشئة الصاعدة (خلال آخر 30 يوم)
# def get_trending_skills(limit=5):
#     last_30_days = timezone.now() - timedelta(days=30)
#
#     trending = Skill.objects.annotate(
#         recent_jobs=Count('required_skills', filter=Q(required_skills__created_at__gte=last_30_days))
#     ).order_by('-recent_jobs')[:limit]
#
#     return [skill.name for skill in trending], [skill.recent_jobs for skill in trending]
#
#
# # 5. توزيع مستويات الخبرة (مبتدئ، متوسط، خبير) وترجمتها للعرض
# def get_experience_level_distribution():
#     exp_data = Job.objects.values('experience_level').annotate(
#         count=Count('id')
#     ).order_by('-count')
#
#     # قاموس لترجمة القيم المخزنة في قاعدة البيانات إلى نصوص عربية مفهومة في الرسم البياني
#     translations = {
#         'entry': 'مبتدئ',
#         'mid': 'متوسط خبرة',
#         'senior': 'خبير'
#     }
#
#     labels = [translations.get(item['experience_level'], item['experience_level']) for item in exp_data if
#               item['experience_level']]
#     data = [item['count'] for item in exp_data]
#
#     return labels, data
#
#
# # 6. حساب متوسط الرواتب بناءً على (min_salary و max_salary) لكل قطاع
# def get_salary_by_category():
#     # نقوم بحساب المتوسط الحسابي بين الحد الأدنى والأقصى للراتب، ثم نأخذ متوسط القطاع ككل
#     salary_data = Job.objects.values('category__name').annotate(
#         avg_salary=Avg((F('min_salary') + F('max_salary')) / 2)
#     ).filter(
#         category__name__isnull=False,
#         avg_salary__isnull=False
#     ).order_by('-avg_salary')[:10]
#
#     labels = [item['category__name'] for item in salary_data]
#     data = [round(item['avg_salary']) for item in salary_data]
#
#     return labels, data




# دالة مساعدة لبناء الفلاتر ديناميكياً بناءً على الطلب (Request)

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


def get_top_skills(filters=None, limit=10):
    # الاحتياط: إذا كان الفلتر فارغاً، نجلب المهارات لجميع الوظائف دون قيود
    job_queryset = Job.objects.all() if not filters else Job.objects.filter(filters)

    top_skills = Skill.objects.filter(
        required_skills__in=job_queryset
    ).annotate(
        jobs_count=Count('required_skills')
    ).order_by('-jobs_count')[:limit]

    return [skill.name for skill in top_skills], [skill.jobs_count for skill in top_skills]


def get_salary_by_category(filters=None):
    # نقوم بحساب المتوسط الحسابي، ونضمن استبعاد القيم الفارغة فقط مع احترام الفلتر الممرر (إن وجد)
    queryset = Job.objects.all() if not filters else Job.objects.filter(filters)
    salary_data = queryset.values('category__name').annotate(
        avg_salary=Avg((F('min_salary') + F('max_salary')) / 2)
    ).filter(
        category__name__isnull=False,
        avg_salary__isnull=False
    ).order_by('-avg_salary')[:10]

    labels = [item['category__name'] for item in salary_data]
    # احتياط حرج: الحماية من الـ NoneType عند عمل الـ round في بايثون
    data = [round(item['avg_salary']) for item in salary_data if item['avg_salary'] is not None]

    return labels, data

# ----------------------------------------------------------------------
# 2. توزيع الوظائف حسب القطاع (مفلتر وآمن)
# ----------------------------------------------------------------------
def get_top_categories(filters=None):
    # احتياط: إذا كان الفلتر فارغاً، نعتمد على كل الوظائف لضمان عرض إحصائيات الكل
    job_queryset = Job.objects.all() if not filters else Job.objects.filter(filters)

    top_categories = SkillCategory.objects.filter(
        jobs__in=job_queryset
    ).annotate(
        # نعد فقط الوظائف التي تنتمي للـ QuerySet المفلترة لمنع تداخل الأرقام
        jobs_count=Count('jobs', filter=Q(jobs__in=job_queryset))
    ).filter(jobs_count__gt=0).order_by('-jobs_count')

    return [cat.name for cat in top_categories], [cat.jobs_count for cat in top_categories]


# ----------------------------------------------------------------------
# 3. الخط الزمني للوظائف (مفلتر وآمن)
# ----------------------------------------------------------------------
def get_jobs_timeline(filters=None):
    # جلب البيانات وبناء المجموعات شهرياً بناءً على الفلتر الحالي

    queryset = Job.objects.all() if not filters else Job.objects.filter(filters)
    timeline_data = queryset.annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')

    labels = []
    data = []

    for item in timeline_data:
        # احتياط أمني: حماية ضد التواريخ المشوهة أو الـ None في قاعدة البيانات عند عمل strftime
        if item['month']:
            try:
                labels.append(item['month'].strftime("%Y-%m"))
                data.append(item['count'])
            except (AttributeError, ValueError):
                pass

    return labels, data


# ----------------------------------------------------------------------
# 4. المهارات الناشئة الصاعدة (مفلترة وآمنة)
# ----------------------------------------------------------------------
def get_trending_skills(filters=None, limit=5):
    last_30_days = timezone.now() - timedelta(days=30)

    # دمج فلتر الـ 30 يوم مع الفلاتر الحالية
    # الاحتياط: إذا كان filters فارغاً، سيعمل شرط الـ 30 يوم وحده على مستوى "الكل" وهو المطلوب
    query = Q(required_skills__created_at__gte=last_30_days)
    combined_filters = query if not filters else filters & query

    trending = Skill.objects.annotate(
        recent_jobs=Count('required_skills', filter=combined_filters)
    ).filter(recent_jobs__gt=0).order_by('-recent_jobs')[:limit]

    return [skill.name for skill in trending], [skill.recent_jobs for skill in trending]


# ----------------------------------------------------------------------
# 5. توزيع مستويات الخبرة (مفلتر وآمن)
# ----------------------------------------------------------------------
def get_experience_level_distribution(filters=None):

    queryset = Job.objects.all() if not filters else Job.objects.filter(filters)
    exp_data = queryset.values('experience_level').annotate(
        count=Count('id')
    ).order_by('-count')

    translations = {
        'entry': 'مبتدئ',
        'mid': 'متوسط خبرة',
        'senior': 'خبير'
    }

    labels = []
    data = []

    for item in exp_data:
        # احتياط: التأكد من أن الحقل ليس فارغاً في قاعدة البيانات وليس نصاً أبيضاً
        level = item['experience_level']
        if level and str(level).strip():
            # ترجمة النص، وإذا لم تكن القيمة مسجلة في القاموس تظهر القيمة الأصلية كما هي بدون كراش
            labels.append(translations.get(level, level))
            data.append(item['count'])

    return labels, data






def get_statistical_data_api(request_params):
    # مصفوفات وهياكل افتراضية لضمان العودة الآمنة دائماً
    charts_data = {
        'top_skills': {'labels': [], 'data': []},
        'top_categories': {'labels': [], 'data': []},
        'jobs_timeline': {'labels': [], 'data': []},
        'trending_skills': {'labels': [], 'data': []},
        'experience_level': {'labels': [], 'data': []},
        'salary_by_category': {'labels': [], 'data': []},
    }

    counters_data = {
        'active_jobs_count': 0, 'total_companies': 0, 'total_members': 0,
        'total_applications': 0, 'successful_hires': 0, 'remote_percentage': 0,
        'total_applications_this_month': 0,
    }

    try:
        today = timezone.now()
        start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # 1. تنظيف الفلاتر وتحويلها لكائن Q موحد لحماية المحرك المهني
        filters = build_job_filters(request_params)
        if not filters:
            base_q = Q()
        elif isinstance(filters, Q):
            base_q = filters
        elif isinstance(filters, dict):
            base_q = Q(**filters)
        else:
            base_q = Q()

        # 2. [حل المشكلة هنا 🛠️] عزل فلتر الوظائف عن فلاتر الجداول الفرعية الأخرى إذا تطلب الأمر
        # نمرر الـ base_q للدوال مع حمايتها فردياً ببلوك try..except مستقل تماماً

        try:
            charts_data['top_skills']['labels'], charts_data['top_skills']['data'] = get_top_skills(base_q)
        except Exception as e:
            logger.error(f"❌ خطأ في دالة get_top_skills: {e}")

        try:
            charts_data['top_categories']['labels'], charts_data['top_categories']['data'] = get_top_categories(base_q)
        except Exception as e:
            logger.error(f"❌ خطأ في دالة get_top_categories: {e}")

        try:
            charts_data['jobs_timeline']['labels'], charts_data['jobs_timeline']['data'] = get_jobs_timeline(base_q)
        except Exception as e:
            logger.error(f"❌ خطأ في دالة get_jobs_timeline: {e}")

        try:
            charts_data['trending_skills']['labels'], charts_data['trending_skills']['data'] = get_trending_skills(
                base_q)
        except Exception as e:
            logger.error(f"❌ خطأ في دالة get_trending_skills: {e}")

        try:
            charts_data['experience_level']['labels'], charts_data['experience_level'][
                'data'] = get_experience_level_distribution(base_q)
        except Exception as e:
            logger.error(f"❌ خطأ في دالة get_experience_level_distribution: {e}")

        try:
            charts_data['salary_by_category']['labels'], charts_data['salary_by_category'][
                'data'] = get_salary_by_category(base_q)
        except Exception as e:
            logger.error(f"❌ خطأ في دالة get_salary_by_category: {e}")

        # -------------------------------------------------------------
        # 3. جلب العدادات (Counters) مع حماية فردية لكل عداد
        # -------------------------------------------------------------
        try:
            counters_data['active_jobs_count'] = Job.objects.filter(base_q, is_active=True).count()
        except Exception as e:
            logger.error(f"Error in active_jobs_count: {e}")

        try:
            counters_data['total_companies'] = CompanyProfile.objects.count()
        except Exception as e:
            logger.error(f"Error in total_companies: {e}")

        try:
            counters_data['total_members'] = MemberProfile.objects.count()
        except Exception as e:
            logger.error(f"Error in total_members: {e}")

        # جلب مجموعة الوظائف المفلترة لبناء مقارنات العلاقات الفرعية بأمان
        try:
            filtered_jobs = Job.objects.filter(base_q)
            total_jobs_count = filtered_jobs.count()

            counters_data['total_applications'] = JobApplication.objects.filter(job__in=filtered_jobs).count()
            counters_data['successful_hires'] = JobApplication.objects.filter(job__in=filtered_jobs,
                                                                              status=JobApplication.Status.ACCEPTED).count()

            # عداد مقبولي الشهر الحالي باستخدام الحقل الصحيح applied_at
            counters_data['total_applications_this_month'] = JobApplication.objects.filter(
                job__in=filtered_jobs,
                status=JobApplication.Status.ACCEPTED,
                applied_at__gte=start_of_month
            ).count()

            # نسبة العمل عن بعد
            remote_jobs_count = Job.objects.filter(base_q, employment_type=Job.EmploymentType.REMOTE).count()
            counters_data['remote_percentage'] = round(
                (remote_jobs_count / total_jobs_count) * 100) if total_jobs_count > 0 else 0
        except Exception as e:
            logger.error(f"❌ خطأ في حساب علاقات الوظائف الفرعية والعدادات: {e}")

        return {
            'charts': charts_data,
            'counters': counters_data
        }

    except Exception as e:
        logger.critical(f"Critical unhandled error in dashboard framework: {str(e)}", exc_info=True)
        return {
            'charts': charts_data,
            'counters': counters_data
        }

# def get_statistical_data_api(request_params):
#     try:
#         today = timezone.now()
#         # تعديل لضمان نطاق زمني آمن لبداية الشهر الحالي
#         start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
#
#         # 1. بناء الفلاتر (سيعيد Q() صافي في حال غياب المعاملات، وهو ما يعني "الكل")
#         filters = build_job_filters(request_params)
#         if filters is None:
#             filters = Q()
#
#         # 2. استدعاء الدوال التحليلية (تم تأمينها مسبقاً لتعيد "الكل" عند تمرير Q فارغ)
#         s_labels, s_data = get_top_skills(filters)
#         c_labels, c_data = get_top_categories(filters)
#         t_labels, t_data = get_jobs_timeline(filters)
#         trend_labels, trend_data = get_trending_skills(filters)
#         exp_labels, exp_data = get_experience_level_distribution(filters)
#         salary_labels, salary_data = get_salary_by_category(filters)
#
#         # -------------------------------------------------------------
#         # 3. تأمين العدادات (Counters) لجلب إحصائيات الكل بأمان
#         # -------------------------------------------------------------
#
#         # أ) عداد الوظائف النشطة: دمج آمن ومباشر
#         active_jobs_query = Q(is_active=True)
#         active_jobs_count = Job.objects.filter(filters & active_jobs_query).count()
#
#         # ب) عدادات إجمالية للمنصة (ثابتة لا تتأثر بفلاتر الوظائف لتوضيح حجم المنصة)
#         total_companies = CompanyProfile.objects.count()
#         total_members = MemberProfile.objects.count()
#
#         # ج) تحديد مجموعة الوظائف المستهدفة بناءً على الفلتر الحالي
#         filtered_jobs = Job.objects.all() if not filters else Job.objects.filter(filters)
#
#         # د) عداد الطلبات الإجمالي للوظائف المحددة
#         total_applications = JobApplication.objects.filter(job__in=filtered_jobs).count()
#
#         # هـ) طلبات التوظيف المقبولة لهذا الشهر فقط
#         total_applications_this_month = JobApplication.objects.filter(
#             job__in=filtered_jobs,
#             status=JobApplication.Status.ACCEPTED,
#             applied_at__gte=start_of_month  # تأكد من اسم حقل التاريخ في موديل الطلبات (applied_at أو created_at)
#         ).count()
#
#         # و) عداد التوظيف الناجح الإجمالي
#         successful_hires = JobApplication.objects.filter(
#             job__in=filtered_jobs,
#             status=JobApplication.Status.ACCEPTED
#         ).count()
#
#         # ز) حساب نسبة العمل عن بعد (الدمج المباشر الصافي)
#         f_jobs_query = Q(employment_type=Job.EmploymentType.REMOTE)
#         remote_jobs_count = Job.objects.filter(filters & f_jobs_query).count()
#         total_jobs = filtered_jobs.count()
#
#         # حماية ضد القسمة على صفر (تضمن 0% بدل كراش الموقع)
#         remote_percentage = round((remote_jobs_count / total_jobs) * 100) if total_jobs > 0 else 0
#
#         return {
#             'charts': {
#                 'top_skills': {'labels': s_labels, 'data': s_data},
#                 'top_categories': {'labels': c_labels, 'data': c_data},
#                 'jobs_timeline': {'labels': t_labels, 'data': t_data},
#                 'trending_skills': {'labels': trend_labels, 'data': trend_data},
#                 'experience_level': {'labels': exp_labels, 'data': exp_data},
#                 'salary_by_category': {'labels': salary_labels, 'data': salary_data},
#             },
#             'counters': {
#                 'active_jobs_count': active_jobs_count,
#                 'total_companies': total_companies,
#                 'total_members': total_members,
#                 'total_applications': total_applications,
#                 'successful_hires': successful_hires,
#                 'remote_percentage': remote_percentage,
#                 'total_applications_this_month': total_applications_this_month,
#             }
#         }
#
#     except Exception as e:
#         # الاحتياط الأخير: لو انقطعت الكهرباء عن قاعدة البيانات أو حدث خطأ مجهول، يعود ببيانات صفرية ولا يتوقف الموقع
#         import logging
#         logging.getLogger(__name__).error(f"Critical error in dashboard statistics: {str(e)}")
#
#         return {
#             'charts': {
#                 'top_skills': {'labels': [], 'data': []}, 'top_categories': {'labels': [], 'data': []},
#                 'jobs_timeline': {'labels': [], 'data': []}, 'trending_skills': {'labels': [], 'data': []},
#                 'experience_level': {'labels': [], 'data': []}, 'salary_by_category': {'labels': [], 'data': []},
#             },
#             'counters': {
#                 'active_jobs_count': 0, 'total_companies': 0, 'total_members': 0,
#                 'total_applications': 0, 'successful_hires': 0, 'remote_percentage': 0,
#                 'total_applications_this_month': 0,
#             }
#         }




def get_statistical_analysis(request_params):
    return  get_statistical_data_api(request_params)



# # 7. الدالة الرئيسية المجمعة لإرسالها للـ View
# def get_statistical_analysis():
#     today = timezone.now()
#     start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
#
#
#     s_labels, s_data = get_top_skills()
#     c_labels, c_data = get_top_categories()
#     t_labels, t_data = get_jobs_timeline()
#     trend_labels, trend_data = get_trending_skills()
#     exp_labels, exp_data = get_experience_level_distribution()
#     salary_labels, salary_data = get_salary_by_category()
#
#
#     active_jobs_count = Job.objects.filter(is_active=True).count()
#     # 2. إجمالي الشركات المسجلة في المنصة
#     total_companies = CompanyProfile.objects.count()
#     total_members = MemberProfile.objects.count()
#
#     # 3. إجمالي طلبات التقديم (عدلها وفقاً للموديل لديك، هنا نضع قيمة افتراضية إذا لم يكن الموديل جاهزاً)
#     total_applications = JobApplication.objects.count()
#
#
#     # 2. حساب عدد التقديمات التي تمت من بداية الشهر وحتى هذه اللحظة
#     # (تأكد من تغيير 'created_at' إلى الاسم الحقيقي لحقل التاريخ في موديل JobApplication لديك)
#     total_applications_this_month = JobApplication.objects.filter(
#         status=JobApplication.Status.ACCEPTED,
#         applied_at__gte=start_of_month
#     ).count()
#
#     # 4. عمليات التوظيف الناجحة (مثلاً الطلبات التي تم قبولها 'accepted')
#     successful_hires = JobApplication.objects.filter(status=JobApplication.Status.ACCEPTED).count()
#
#     # 5. نسبة الوظائف التي تتيح العمل عن بعد (Remote)
#     remote_jobs_count = Job.objects.filter(employment_type=Job.EmploymentType.REMOTE).count()
#     total_jobs = Job.objects.count()
#     remote_percentage = round((remote_jobs_count / total_jobs) * 100) if total_jobs > 0 else 0
#
#     return {
#         # بيانات الرسومات البيانية السابقة
#         'top_skills_labels': json.dumps(s_labels, ensure_ascii=False),
#         'top_skills_data': json.dumps(s_data),
#         'top_jobs_labels': json.dumps(c_labels, ensure_ascii=False),
#         'top_jobs_data': json.dumps(c_data),
#         'top_time_labels': json.dumps(t_labels),
#         'top_time_data': json.dumps(t_data),
#         'trending_skills_labels': json.dumps(trend_labels, ensure_ascii=False),
#         'trending_skills_data': json.dumps(trend_data),
#         'exp_labels': json.dumps(exp_labels, ensure_ascii=False),
#         'exp_data': json.dumps(exp_data),
#         'salary_labels': json.dumps(salary_labels, ensure_ascii=False),
#         'salary_data': json.dumps(salary_data),
#         'get_jobs': get_jobs(),
#
#         # الأرقام والإحصائيات الثابتة الجديدة (تمرر كأرقام مباشرة وليس JSON)
#         'active_jobs_count': active_jobs_count,
#         'total_companies': total_companies,
#         'total_members': total_members,
#         'total_applications': total_applications,
#         'successful_hires': successful_hires,
#         'remote_percentage': remote_percentage,
#         'total_applications_this_month': total_applications_this_month,
#     }


def get_statisticals():
    today = timezone.now()
    start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    active_jobs_count = Job.objects.filter(is_active=True).count()
    # 2. إجمالي الشركات المسجلة في المنصة
    total_companies = CompanyProfile.objects.count()
    total_members = MemberProfile.objects.count()

    # 3. إجمالي طلبات التقديم (عدلها وفقاً للموديل لديك، هنا نضع قيمة افتراضية إذا لم يكن الموديل جاهزاً)
    total_applications = JobApplication.objects.count()


    # 2. حساب عدد التقديمات التي تمت من بداية الشهر وحتى هذه اللحظة
    # (تأكد من تغيير 'created_at' إلى الاسم الحقيقي لحقل التاريخ في موديل JobApplication لديك)
    total_applications_this_month = JobApplication.objects.filter(
        status=JobApplication.Status.ACCEPTED,
        applied_at__gte=start_of_month
    ).count()

    # 4. عمليات التوظيف الناجحة (مثلاً الطلبات التي تم قبولها 'accepted')
    successful_hires = JobApplication.objects.filter(status=JobApplication.Status.ACCEPTED).count()

    # 5. نسبة الوظائف التي تتيح العمل عن بعد (Remote)
    remote_jobs_count = Job.objects.filter(employment_type=Job.EmploymentType.REMOTE).count()
    total_jobs = Job.objects.count()
    remote_percentage = round((remote_jobs_count / total_jobs) * 100) if total_jobs > 0 else 0

    return {


        'get_companies': get_companies(6),
        'get_jobs': get_jobs(),
        'cities': City.objects.values_list('name', flat=True).distinct(),
        'active_jobs_count': active_jobs_count,
        'total_companies': total_companies,
        'total_members': total_members,
        'total_applications': total_applications,
        'successful_hires': successful_hires,
        'remote_percentage': remote_percentage,
        'total_applications_this_month': total_applications_this_month,
    }

