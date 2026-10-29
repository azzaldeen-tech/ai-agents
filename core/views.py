# from django.shortcuts import render
import json
import threading
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render,redirect,reverse,get_object_or_404
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db.models import Count, Q
from accounts.models import CustomUser
from companies.models import Job, CompanyProfile, JobApplication
from core.Utils.JobServices import JobServices
from core.Utils.ai_statistical_analysis import get_ai_job_forecasting, get_student_future_trends
from core.Utils.statistical_analysis import get_statistical_analysis, get_statisticals, get_statistical_data_api, \
    build_job_filters
from django.core.serializers.json import DjangoJSONEncoder
from core.models import SkillCategory, City
from companies.models import Job
from django.db.models import Exists, OuterRef
from django.utils import timezone


# from core.Utils.services import start_sync_scraper

# @login_required
def waiting_approval_view(request):
    return render(request, 'core/waiting_approval.html')

# @login_required
def home(request):
    result=get_statisticals()
    return render(request, 'core/home.html',result)

def predictive_analytics(request):

    base_q = build_job_filters(request.GET)
    labels, data_values = get_ai_job_forecasting(base_q)
    ai_chart_data = {'labels': labels, 'data': data_values}

    # تحديث الشرط ليكون أكثر مرونة وأماناً
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('format') == 'json'

    if is_ajax:
        print("🚀 AJAX request captured successfully and data ready!")
        return JsonResponse({'success': True, 'chart': ai_chart_data})

    # إذا كان التحميل الأول للصفحة
    context = {
        'ai_chart': ai_chart_data,
        'cities': City.objects.all(),
        'categories': SkillCategory.objects.all(), # تعديل ليتوافق مع موديلك الحركي
    }
    return render(request, 'core/predictive_analytics.html', context)


def student_guidance_analytics(request):
    # استدعاء دالة التنبؤ بالتخصصات الواعدة
    labels, data_values, top_careers = get_student_future_trends()

    context = {
        'student_chart_labels': labels,
        'student_chart_data': data_values,
        'top_careers': top_careers  # سنستخدم هذه القائمة لبناء بطاقات نصية ذكية تفيد الطالب
    }
    return render(request, 'core/student_predictive.html', context)


def labor_market_trends(request):

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = get_statistical_data_api(request.GET)
        return JsonResponse(data)

    context = get_statistical_analysis(request)
    context['cities']= City.objects.all()
    context['categories']= SkillCategory.objects.all()
    context['years']= range(2022, timezone.now().year + 1)

    return render(request, 'core/labor_market_trends.html',context)


def companies_explore_view(request):
    # جلب جميع الشركات مع حساب عدد الوظائف النشطة (is_active=True) لكل شركة
    # واستخدام prefetch_related/select_related لرفع الأداء الإجمالي للـ Query
    companies_queryset = CompanyProfile.objects.annotate(
        active_jobs_count=Count('jobs', filter=Q(jobs__is_active=True))
    ).order_by('-active_jobs_count')

    # تجهيز البيانات للإرسال إلى القالب (Template)
    companies_data = []
    for company in companies_queryset:
        # استخراج اسم الشركة بأمان بناءً على الحقول المتوفرة لديك
        company_name = getattr(company, 'company_name', getattr(company, 'name', 'شركة مسجلة'))

        companies_data.append({
            'id': company.id,
            'instance': company,
            'name': company_name,
            # 'industry': getattr(company, 'industry', 'تقنية المعلومات'),  # قطاع العمل
            'location': getattr(company, 'location', 'الرياض، السعودية'),
            'logo': company.logo.url if hasattr(company, 'logo') and company.logo else None,
            'bio': getattr(company, 'bio', 'لا يوجد وصف مختصر متوفر حالياً لهذه الشركة.'),
            'active_jobs': company.active_jobs_count,
            'website': getattr(company, 'website', '#'),
        })

    context = {
        'companies': companies_data,
        'total_companies_count': companies_queryset.count(),
    }
    return render(request, 'core/companies_explore.html', context)


def company_profile(request, pk):
    # 1. جلب الشركة المطلوبة أو إظهار 404
    company = get_object_or_404(CompanyProfile.objects.select_related('user'), pk=pk)

    # 2. بناء استعلام الوظائف النشطة التابعة لهذه الشركة فقط
    # نستخدم الفلتر بناءً على حقل الربط (تأكد من اسم الحقل في موديل Job لديك، هنا افترضنا أنه company)
    company_jobs = Job.objects.filter(company=company, is_active=True)
    member=None
    # 3. التحقق مما إذا كان المستخدم الحالي مسجلاً ومن نوع "member"
    if request.user.is_authenticated and getattr(request.user, 'is_member', False):
        member = getattr(request.user, 'profile', None) or getattr(request.user, 'member_profile', None)

        if member:
            # استخدام Exists لدمج فحص التقديم مباشرة داخل استعلام قاعدة البيانات
            is_applied_subquery = JobApplication.objects.filter(
                member=member,
                job_id=OuterRef('pk')
            )
            # إضافة حقل ديناميكي اسمه 'is_applied_to_job' لكل وظيفة
            company_jobs = company_jobs.annotate(is_applied_to_job=Exists(is_applied_subquery))

    # 4. تجهيز مصفوفة البيانات لإرسالها بالقالب مع الروابط الديناميكية
    jobs_data = []
    for job in company_jobs:
        job_join_url = ""
        job_cancel_url = ""
        if member:
            try:
                job_join_url = reverse('members:job_join', args=[job.id])
                job_cancel_url = reverse('members:job_cancel', args=[job.id])
            except Exception:
                job_join_url = f"/members/job_join/{job.id}/"
                job_cancel_url = f"/members/job_cancel/{job.id}/"

        jobs_data.append({
            'id': job.id,
            'title': job.title,
            'location': job.location,
            'employment_type': job.employment_type,
            'job_join_url': job_join_url,
            'job_cancel_url': job_cancel_url,
            'created_at': job.get_created_at,
            # إذا لم يكن مستخدماً من نوع member، ستكون القيمة الافتراضية دائماً False
            'is_applied': getattr(job, 'is_applied_to_job', False)
        })

    # 5. إرسال البيانات المجهزة بالكامل إلى القالب
    return render(request, 'core/company-profile.html', {
        'company': company,
        'company_jobs': jobs_data
    })


def explore_jobs_view(request):
    # 1. جلب معرفات الوظائف التي تقدم إليها المستخدم الحالي (إن كان مسجلاً)

    exclude_job_id = 0
    applied_jobs_ids = []

    if request.user.is_authenticated and request.user.is_member:
        member = request.user.profile

        exclude_app = JobApplication.objects.select_related('job')\
            .filter(member=member,status=JobApplication.Status.ACCEPTED)\
            .first()

        if exclude_app:
            exclude_job_id = exclude_app.job.id

        applied_jobs_ids = list(JobApplication.objects.filter(member=member)
                                .exclude(status=JobApplication.Status.REJECTED)
                                .exclude(status=JobApplication.Status.ACCEPTED)
                                .values_list('job_id', flat=True))

        # current_job=JobApplication.objects.filter(member=member,status=JobApplication.Status.ACCEPTED).first()
        # if current_job:
        #     current_job_id = current_job.id


    # 2. جلب الوظائف النشطة
    jobs_queryset = Job.objects.filter(is_active=True)\
        .exclude(id=exclude_job_id)\
        .select_related('category', 'company')\
        .prefetch_related('required_skills')

    jobs_data = []

    for job in jobs_queryset:
        company_name = "شركة مسجلة"
        if job.company:
            company_name = getattr(job.company, 'company_name', getattr(job.company, 'name', str(job.company)))

        try:
            job_join_url = reverse('members:job_join', args=[job.id])
            job_cancel_url = reverse('members:job_cancel', args=[job.id])
        except Exception:
            # روابط بديلة مؤقتة في حال وجود اختلاف في الـ namespace الخاص بالـ urls
            job_join_url = f"/members/job_join/{job.id}/"
            job_cancel_url = f"/members/job_cancel/{job.id}/"

        jobs_data.append({
            'id': job.id,
            'title': job.title,
            'company': company_name,
            'category': str(job.category.id) if job.category else "all",
            'location': job.location,
            'employment_type': job.employment_type,
            'experience_level': job.experience_level,
            'min_salary': float(job.min_salary) if job.min_salary else 0,
            'max_salary': float(job.max_salary) if job.max_salary else 0,
            'required_skills': [skill.name for skill in job.required_skills.all()],
            # 'created_at': job.created_at.strftime('%Y-%m-%d') if job.created_at else "",
            'created_at': job.get_created_at,

            # الحقول الجديدة التي يطلبها الجافاسكريبت الآن لقراءة الأزرار
            'is_applied': job.id in applied_jobs_ids if applied_jobs_ids else False,
            # 'his_current_job': True if current_job_id>0 else False,
            'job_join_url': job_join_url,
            'job_cancel_url': job_cancel_url
        })

    categories = SkillCategory.objects.all()

    context = {
        'categories': categories,
        # 'currentJobId': current_job_id,
        'jobs_json': json.dumps(jobs_data, cls=DjangoJSONEncoder, ensure_ascii=False)
    }

    return render(request, 'core/jobs_explore.html', context)

def companies(request):
    companies=CompanyProfile.objects.all()
    return render(request, 'core/companies.html',{'companies':companies})

@login_required
def toggle_theme(request):
    user = request.user
    user.is_dark_mode = not user.is_dark_mode
    user.save()
    return JsonResponse({'status': 'success', 'is_dark_mode': user.is_dark_mode})

@login_required
def search_users(request):
    query = request.GET.get('search', '') # تأكد أن name="search" في الـ input
    if query:
        users = CustomUser.objects.filter(username__icontains=query)
    else:
        users = []

    # التغيير هنا: نرسل قالب النتائج فقط
    return render(request, 'core/partials/user_list_results.html', {'users': users})

# @login_required
# def live_jobs_view(request):
#     query = request.GET.get('q', '')  # جلب كلمة البحث من مربع النص في المتصفح
#     results = []
#
#     if query:
#         # تشغيل السكرابر وجلب النتائج مباشرة للمتصفح
#         results = start_sync_scraper(query)
#
#     return render(request, 'core/search_results.html', {
#         'jobs': results,
#         'query': query
#     })

# @login_required
# def trigger_scraper_view(request):
#     if request.method == "POST":
#         query = request.POST.get('q', 'Software Engineer')
#
#         # تشغيل في مسار خلفي (Thread) لكي لا تتجمد الصفحة
#         def bg_task():
#             start_sync_scraper(query)
#
#         thread = threading.Thread(target=bg_task)
#         thread.start()
#
#         messages.info(request, f"بدأت عملية السحب لـ '{query}'. ستظهر النتائج في الجدول خلال لحظات.")
#         return redirect('jobs_list')  # أو أي صفحة تريدها
#
#     return render(request, 'scraper_control.html')

@login_required
def search_skills(request):

    query = request.GET.get('search', '').strip()
    skills=JobServices.search_skills(query)
    # إذا كان الطلب من Tom Select (AJAX)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'json' in request.path:
        # print("****************************")
        results = [{'id': s.id, 'name': s.name} for s in skills]

        return JsonResponse({'results': results})

    # للاستخدامات الأخرى بـ HTMX التي تحتاج HTML
    return render(request, f'core/partials/skill_list_results.html', {'skills': skills})\

@login_required
def search_jobs(request):

    query = request.GET.get('search', '').strip()
    jobs=JobServices.search_jobs(query)
    # إذا كان الطلب من Tom Select (AJAX)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'json' in request.path:
        # print("****************************")
        results = [{'id': s.id, 'title': s.title} for s in jobs]

        return JsonResponse({'results': results})

    # للاستخدامات الأخرى بـ HTMX التي تحتاج HTML
    return render(request, f'core/partials/search_job_results.html', {'jobs': jobs})