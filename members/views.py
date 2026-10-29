from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages as django_messages
from django.utils.translation import gettext_lazy as _

from companies.Utils.services import get_filtered_applications, get_job_simple_applications
from companies.models import Job, JobApplication
from core.Utils.JobServices import JobServices
from core.app_links import AppLinks
from core.helpers import  get_current_date
from core.models import Skill
from members.decorators import member_required
from members.forms import MemberProfileForm
from members.models import MemberProfile

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Avg



app_name = 'members'

# @member_required
# @login_required
# def statistics(request):
#     jobs_count=JobServices.get_jobs_count()

@member_required
@login_required
def dashboard_view(request):
    user = request.user
    member = user.profile
    # 1. إحصائيات طلبات التوظيف
    # تفترض البنية وجود علاقة Related Name أو استعلام مباشر من موديل الطلبات
    # applied_jobs_queryset = JobApplication.objects.filter(member=member)

    # محاكاة برمجية ذكية مبنية على قاعدة بياناتك:
    total_applications = member.applications.count() if hasattr(member, 'applications') else 0
    accepted_applications =   member.applications.filter(status=JobApplication.Status.ACCEPTED).count()
    pending_applications =  member.applications.filter(status=JobApplication.Status.PENDING).count()
    rejected_applications =  member.applications.filter(status=JobApplication.Status.REJECTED).count()

    # 2. إحصائيات المهارات والتدريب (Labor-Market-Trend-Anyalysis Training)

    total_skills_count = user.profile.skills.count() if hasattr(user, 'profile') else 0

    # حساب نسبة اكتمال الملف الشخصي لرفع الجاهزية للموقع
    # profile_completion_percentage = 85  # حساب ديناميكي بناءً على الحقول المكتملة

    # 3. تجهيز قائمة بآخر الطلبات وحالتها لعرضها في جدول
    # جلب آخر 10 طلبات تقديم تم إرسالها بواسطة العضو
    recent_applications_list = JobApplication.objects.filter(member=member).order_by('-applied_at')[:10]

    context = {
        'total_applications': total_applications,
        'accepted_applications': accepted_applications,
        'pending_applications': pending_applications,
        'rejected_applications': rejected_applications,
        'total_skills_count': total_skills_count,
        # 'profile_completion_percentage': profile_completion_percentage,
        'recent_applications': recent_applications_list,
    }

    # return render(request, 'member_dashboard.html', context)
    return render(request, f'{app_name}/dashboard.html',context)

@member_required
@login_required
def member_dashboard_view(request):
    # جلب ملف العضو المرتبط بالمستخدم الحالي
        # (افترضنا أن العلاقة OneToOne بين المستخدم و MemberProfile تسمى member_profile)
    member_profile = get_object_or_404(MemberProfile, user=request.user)

    # 1. جلب كافة طلبات التقديم الخاصة بهذا العضو مع تحسين الأداء عبر select_related
    applications = JobApplication.objects.filter(member=member_profile).select_related('job', 'job__company')

    # 2. حساب الإحصائيات الحية ديناميكياً
    total_applications = applications.count()
    accepted_count = applications.filter(status=JobApplication.Status.ACCEPTED).count()
    pending_count = applications.filter(status=JobApplication.Status.PENDING).count()
    rejected_count = applications.filter(status=JobApplication.Status.REJECTED).count()

    # 3. حساب متوسط نسبة المطابقة (Match Score) لمهارات العضو مع الوظائف التي قدم عليها
    avg_match_score = applications.aggregate(Avg('match_score'))['match_score__avg'] or 0.0
    # تحويلها لنسبة مئوية صحيحة (مثلاً 0.85 تصبح 85%) إذا كنت تخزنها ككسر، أو تركها كما هي
    profile_match_percentage = round(avg_match_score if avg_match_score > 1 else avg_match_score * 100)

    # 4. بناء مصفوفة الطلبات الأخيرة للجدول لتقرأ من موديلك مباشرة
    recent_applications_list = []

    # خريطة لربط الحالات بالألوان المتناسقة مع تصميمك
    status_configs = {
        JobApplication.Status.PENDING: {'text': 'قيد المراجعة', 'color': 'warning'},
        JobApplication.Status.ACCEPTED: {'text': 'مقبول', 'color': 'success'},
        JobApplication.Status.REJECTED: {'text': 'مرفوض', 'color': 'error'},
    }

    for app in applications.order_by('-applied_at')[:5]:  # آخر 5 طلبات
        config = status_configs.get(app.status, {'text': app.get_status_display(), 'color': 'neutral'})

        # استخراج اسم الشركة بأمان
        company_name = "شركة مسجلة"
        if app.job.company:
            company_name = getattr(app.job.company, 'company_name',
                                   getattr(app.job.company, 'name', str(app.job.company)))

        recent_applications_list.append({
            'job_title': app.job.title,
            'company': company_name,
            'date': app.applied_at.strftime('%Y-%m-%d'),
            'match_score': round(app.match_score if app.match_score > 1 else app.match_score * 100),
            'status_text': config['text'],
            'status_color': config['color']
        })

    context = {
        'total_applications': total_applications,
        'accepted_count': accepted_count,
        'pending_count': pending_count,
        'rejected_count': rejected_count,
        'profile_match_percentage': profile_match_percentage,
        'recent_applications': recent_applications_list,
    }

    return render(request, 'member_dashboard.html', context)


@member_required
@login_required
def profile_view(request):

    profile, created = MemberProfile.objects.get_or_create(user=request.user)
    skills_list = Skill.objects.all().values('id', 'name')

    if request.method == "POST":
        form = MemberProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect(AppLinks.Dashboards.MEMBER)
    else:
        form = MemberProfileForm(instance=profile)

    return render(request, f'{app_name}/profile/form.html',{
        'skills_list': skills_list,
        'form':form,
    })


@member_required
@login_required
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    has_applied = JobApplication.objects.filter(job=job, member=request.user.profile).exists()
    return  render(request,f"{app_name}/jobs/detail.html",{
        'job':job,
        'has_applied':has_applied
    })


@member_required
@login_required
def job_join(request, pk):
    job = get_object_or_404(Job, pk=pk)
    next_url = request.META.get('HTTP_REFERER')
    fallback_url = redirect(f"{app_name}:advertised_jobs").url
    destination = next_url if next_url else fallback_url
    if not hasattr(request.user, 'profile'):
        django_messages.error(request, _('يرجى إكمال ملفك الشخصي أولاً.'))
        return redirect(destination)

    member = request.user.profile
    exists = JobApplication.objects.filter(job=job, member=member).exists()

    if exists:
        django_messages.warning(request, _('لقد قمت بطلب الانضمام لهذه الوظيفة مسبقاً.'))
    else:
        JobApplication.objects.create(
            job=job,
            member=member,
        )
        django_messages.success(request, _('تم ارسال طلب الانضمام للوظيفة بنجاح.'))

    return redirect(destination)


@login_required
def cancel_job_join(request, pk):
    job = get_object_or_404(Job, pk=pk)
    next_url = request.META.get('HTTP_REFERER')
    fallback_url = redirect(f"{app_name}:advertised_jobs").url
    destination = next_url if next_url else fallback_url
    if hasattr(request.user, 'profile'):
        member = request.user.profile
        application = JobApplication.objects.filter(job=job, member=member).first()
        if application:
            application.delete()
            django_messages.success(request, _('تم إلغاء طلب الانضمام للوظيفة بنجاح.'))
        else:
            django_messages.warning(request, _('أنت غير مسجل في هذه الوظيفة أصلاً.'))
    else:
        django_messages.error(request, _('لا تملك ملف تعريف عضو لإتمام هذه العملية.'))

    return redirect(destination)


@member_required
@login_required
def advertised_jobs(request):
    # current_date=get_current_date()

    exclude_job_id = 0
    applied_jobs_ids = []

    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        member = request.user.profile
        exclude_app=JobApplication.objects.select_related('job').filter(member=member,status=JobApplication.Status.ACCEPTED).first()
        if exclude_app:
            exclude_job_id=exclude_app.job.id

        applied_jobs_ids = JobApplication.objects.filter(member=member) \
            .exclude(status=JobApplication.Status.REJECTED)\
            .exclude(status=JobApplication.Status.ACCEPTED)\
            .values_list('job_id', flat=True)

    jobs = Job.objects.filter(is_active=True)\
        .exclude(id=exclude_job_id)\
        .order_by('-created_at')

    context = {
        'jobs': jobs,
        'applied_jobs_ids': applied_jobs_ids,
    }


    return render(request, f'{app_name}/jobs/advertised_jobs.html', context)\


@member_required
@login_required
def job_applications(request):
    member=request.user.profile
    # my_filter = {'job__company': company}
    job_applications = get_filtered_applications(member=member)
    simplified_apps = get_job_simple_applications(job_applications)
    return render(request, f'{app_name}/jobs/job_applications.html',
                  {'job_applications': simplified_apps})


@login_required
@member_required
def applied_jobs(request):


    applied_jobs = []

    if request.user.is_authenticated and hasattr(request.user, 'profile'):

        # جلب أرقام الوظائف التي قدم عليها هذا المستخدم فقط
        job_ids = JobApplication.objects.filter(member=request.user.profile).values_list('job', flat=True)

        # 2. جلب الوظائف التي تنتمي لهذه القائمة
        applied_jobs = Job.objects.filter(id__in=job_ids).order_by('-created_at')

        context = {
            'jobs': applied_jobs,
        }


    return render(request, f'{app_name}/jobs/applied_jobs.html', context)

@login_required
@member_required
def search_jobs(request):

    query = request.GET.get('search', '').strip()
    jobs=JobServices.search_jobs(query)

    return render(request, f'{app_name}/partials/search_job_results.html', {'jobs': jobs})

