from datetime import datetime

from django.contrib import messages as django_messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from companies.Utils.services import get_job_simple_applications, get_filtered_applications, \
    change_job_application_status
from companies.decorators import company_required
from companies.forms import JobForm, CompanyProfileForm
from companies.models import Job, CompanyProfile, JobApplication, SimpleApplication
from core.app_links import AppLinks
from core.models import Skill

app_name = 'companies'

#
# def dashboard_view(request):
#     return render(request, 'companies/dashboard.html')



@company_required
@login_required
def dashboard_view(request):

    job_posts = Job.objects.filter(company=request.user.profile)
    applied_jobs = JobApplication.objects.filter(job__company=request.user.profile)\
        .select_related('job', 'member__user')\
        .order_by('-applied_at') #'-match_score',

    simplified_apps = [SimpleApplication(app) for app in applied_jobs]

    weekly_data = {
        'labels': ['السبت', 'الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة'],
        'apps':[12, 8, 15, 22, 18, 24, 0],
        'hires':[0, 0, 0, 1, 0, 1, 0]
    }

    stats_cards = [
        {
            'title': "الوظائف",
            'amount': job_posts.count,
            'icon': "megaphone",  # بديل احترافي لـ fa-bullhorn في Lucide
            'badge_type': "brand",
            'badge_amount': "+2",
            'badge_text': "هذا الأسبوع",
            'delay': "0.1s"
        },
        {
            'title': "إجمالي المتقدمين",
            'amount': request.user.profile.jobs_applications_number,
            'icon': "inbox",  # متوفرة بنفس الاسم في Lucide
            'badge_type': "brand",
            'badge_amount': "24+",
            'badge_text': "هذا الأسبوع",
            'delay': "0.2s"
        },
        {
            'title': "المقابلات",
            'amount': 6,
            'icon': "video",  # متوفرة بنفس الاسم في Lucide للمقابلات المرئية
            'badge_type': "amber",
            'badge_amount': "3",
            'badge_text': "اليوم",
            'badge_icon': "arrow-up",  # تغيير fa-arrow-up إلى نمط Lucide
            'delay': "0.3s"
        },
        {
            'title': "تم التعيين هذا الشهر",
            'amount': 0,
            'icon': "user-check",  # متوفرة بنفس الاسم في Lucide
            'badge_type': "brand",
            'badge_icon': "arrow-up",  # تغيير fa-arrow-up إلى نمط Lucide
            'badge_amount': "33%",
            'badge_text': "عن الشهر السابق",
            'delay': "0.4s"
        }
    ]

    funnel_data = [
        {'label': 'المتقدمون الإجمالي', 'count': request.user.profile.jobs_applications_number, 'pct': 10},
        {'label': 'اجتاز الفرز الأولي', 'count': 94, 'pct': 50.5},
        {'label': 'مقابلة هاتفية', 'count': 42, 'pct': 22.6},
        {'label': 'مقابلة شخصية', 'count': 18, 'pct': 9.7},
        {'label': 'عرض مقدم', 'count': 7, 'pct': 3.8},
        {'label': 'تم التعيين', 'count': 4, 'pct': 2.15},

    ]

    candidates = [
        {'name': 'محمد العتيبي', 'role': 'مطور Frontend', 'time': 'منذ 5 دقائق', 'avatar': 'م', 'color': '#0d7c5f',
         'match': 92},
        {'name': 'نورة الحربي', 'role': 'مصممة UX/UI', 'time': 'منذ 20 دقيقة', 'avatar': 'https://randomuser.me/api/portraits/women/44.jpg', 'color': '#e06040',
         'match': 87},
        {'name': 'فهد القحطاني', 'role': 'مطور Backend', 'time': 'منذ 45 دقيقة', 'avatar': 'https://randomuser.me/api/portraits/men/32.jpg', 'color': '#2a8fc7',
         'match': 84},
        {'name': 'ريم الدوسري', 'role': 'مديرة مشروع', 'time': 'منذ ساعة', 'avatar': 'https://api.dicebear.com/7.x/avataaars/svg?seed=Felix', 'color': '#c48a0a',
         'match': 79},
        {'name': 'عبدالله الشمري', 'role': 'مهندس DevOps', 'time': 'منذ ساعتين', 'avatar': 'ع', 'color': '#7c5cbf',
         'match': 76},
    ]

    # job_posts = [
    #     {'title': 'مطور Frontend (React)', 'dept': 'التقنية', 'apps': 42, 'views': 380, 'status': 'نشطة',
    #      'status_color': 'brand', 'days': 12},
    #     {'title': 'مصمم UX/UI أول', 'dept': 'التصميم', 'apps': 31, 'views': 265, 'status': 'نشطة',
    #      'status_color': 'brand', 'days': 8},
    #     {'title': 'مطور Backend (Python)', 'dept': 'التقنية', 'apps': 38, 'views': 310, 'status': 'نشطة',
    #      'status_color': 'brand', 'days': 15},
    #     {'title': 'مدير تسويق رقمي', 'dept': 'التسويق', 'apps': 56, 'views': 520, 'status': 'مغلقة',
    #      'status_color': 'muted', 'days': 30},
    #     {'title': 'محلل بيانات أول', 'dept': 'التحليلات', 'apps': 19, 'views': 145, 'status': 'نشطة',
    #      'status_color': 'brand', 'days': 4},
    # ]

    interviews = [
        {'candidate': 'ليلى أحمد', 'role': 'مصممة UX/UI', 'time': '10:00 ص', 'day': 'اليوم', 'type': 'فيديو',
         'icon': 'fa-video', 'color': 'sky'},
        {'candidate': 'عمر السعيد', 'role': 'مطور Frontend', 'time': '11:30 ص', 'day': 'اليوم', 'type': 'شخصية',
         'icon': 'fa-user', 'color': 'brand'},
        {'candidate': 'سارة الغامدي', 'role': 'مديرة مشروع', 'time': '2:00 م', 'day': 'اليوم', 'type': 'هاتفية',
         'icon': 'fa-phone', 'color': 'amber'},
        {'candidate': 'خالد الراشد', 'role': 'مطور Backend', 'time': '9:30 ص', 'day': 'غداً', 'type': 'فيديو',
         'icon': 'fa-video', 'color': 'sky'},
        {'candidate': 'هند العمري', 'role': 'محللة بيانات', 'time': '1:00 م', 'day': 'غداً', 'type': 'شخصية',
         'icon': 'fa-user', 'color': 'brand'},
    ]



    context = {
        'user_name': 'أحمد',
        'current_date': datetime.now(),
        'stats_cards': stats_cards,
        'funnel_data': funnel_data,
        'weekly_data': weekly_data,
        'candidates': simplified_apps,
        'job_posts': job_posts,
        'interviews': interviews,
        # 'statistics': statistics,
    }

    return render(request, 'companies/dashboard.html', context)

@company_required
@login_required
def delete_job(request, pk):

    job = get_object_or_404(Job, pk=pk)
    if job.company.user != request.user:
        django_messages.error(request, "ليس لديك صلاحية لحذف هذه الوظيفة.")
        return redirect(f'{app_name}:advertised_jobs')

    if request.method == 'POST':
        job.delete()
        django_messages.success(request, "تم حذف الوظيفة بنجاح.")

    return redirect(f'{app_name}:advertised_jobs')


    # return render(request, f'{app_name}/jobs/confirm_delete.html', {'job': job})


@company_required
@login_required
def manage_job(request, pk=None):
    # إذا كان هناك pk، فنحن في حالة "تعديل"، وإلا فنحن في حالة "إضافة"
    company=request.user.profile
    job_instance = get_object_or_404(Job, pk=pk) if pk else None
    skills_list = Skill.objects.all().values('id', 'name')
    # selected_skill_ids = list(job_instance.required_skills.values_list('id', flat=True))
    if request.method == 'POST':
        # تمرير الـ instance هنا هو السر: إذا وجد سيقوم بالتحديث، وإذا لم يجد سيقوم بالإنشاء
        form = JobForm(request.POST, instance=job_instance)

        if form.is_valid():
            job = form.save(commit=False)

            # في حالة الإضافة فقط، نربط الوظيفة بشركة المستخدم الحالي
            if not job_instance:
                job.company = company

            job.save()
            form.save_m2m()  # ضروري جداً لأنك تستخدم ManyToMany لـ required_skills

            return redirect( f'{app_name}:advertised_jobs')  # أو أي صفحة تريدها بعد النجاح
    else:
        form = JobForm(instance=job_instance)

    context = {
        'form': form,
        'is_edit': pk is not None,  # لنعرف في القالب (Template) هل نكتب "تعديل" أم "إضافة"
        'job': job_instance,
        # 'selected_skills': selected_skill_ids,
        'skills_list': skills_list,
    }

    return render(request, f'{app_name}/jobs/job_form.html',context)

@company_required
@login_required
def profile_view(request):

    profile, created = CompanyProfile.objects.get_or_create(user=request.user)
    skills_list = Skill.objects.all().values('id', 'name')

    if request.method == "POST":
        form = CompanyProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect(AppLinks.Dashboards.COMPANY)
    else:
        form = CompanyProfileForm(instance=profile)

    return render(request, f'{app_name}/profile/form.html',{
        'skills_list': skills_list,
        'form':form,
    })


@company_required
@login_required
def advertised_jobs(request):
    # print(f"<<<<advertised_jobs>>>>")
    advertised_jobs = Job.objects.filter(company=request.user.profile)\
        .order_by('-created_at')

    return render(request, f'{app_name}/jobs/job_list.html', {'jobs': advertised_jobs})

@company_required
@login_required
def job_applications(request):
    company=request.user.profile
    my_filter = {'job__company': company}
    job_applications = get_filtered_applications(**my_filter)
    simplified_apps = get_job_simple_applications(job_applications)
    return render(request, f'{app_name}/jobs/job_applications.html',
                  {'job_applications': simplified_apps})

@login_required
@company_required
def job_detail(request, pk):
    is_owner = False
    job = get_object_or_404(Job, pk=pk)

    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        is_owner = (job.company == request.user.profile)

    job_applications=get_filtered_applications(job_id=pk)
    simplified_apps = get_job_simple_applications(job_applications)

    return  render(request,f"{app_name}/jobs/detail.html",{
        'job':job,
        'is_owner':is_owner,
        'job_applications':simplified_apps,
    })

@login_required
@company_required
def job_applicant_detail(request, pk):

    job_apps=get_filtered_applications(id=pk)
    simplified_job_apps = get_job_simple_applications(job_apps)
    simplified_job_app = next(iter(simplified_job_apps), None)

    return  render(request,f"{app_name}/jobs/job_applicant_detail.html",{
        'job_application':simplified_job_app,
    })

@login_required
@company_required
def job_app_accept(request, pk):
    change_job_application_status(pk,JobApplication.Status.ACCEPTED)
    destination = request.META.get('HTTP_REFERER')
    return redirect(destination)

@login_required
@company_required
def job_app_reject(request, pk):
    change_job_application_status(pk,JobApplication.Status.REJECTED)
    destination = request.META.get('HTTP_REFERER')
    return redirect(destination)