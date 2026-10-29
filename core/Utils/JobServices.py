from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from companies.models import Job
from core.models import Skill


class JobServices:

    @staticmethod
    def get_jobs_count():
        return  Job.objects.count()\

    @staticmethod
    def get_jobs():
        return  Job.objects.all()

    @staticmethod
    def search_jobs(query=None):

        if query:
            jobs = Job.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(requirements__icontains=query) |
                Q(required_skills__name__icontains=query) |
                Q(category__name__icontains=query),
                is_active=True
            ).distinct()[:20]  # تحديد العدد لسرعة الاستجابة
        else:
            jobs = [] # Job.objects.all()[:20]
        return jobs


    @staticmethod
    def search_skills(query=None):

        if query:
            skills = Skill.objects.filter(
                Q(name__icontains=query) |
                Q(category__name__icontains=query)
            ).distinct()[:20]  # تحديد العدد لسرعة الاستجابة
        else:
            skills = Skill.objects.all()[:20]
        return skills

    @staticmethod
    def get_paginated_skills(query=None, page_number=1):

        if query:
            queryset = Skill.objects.filter(
                Q(name__icontains=query) |
                Q(category__name__icontains=query)
            ).distinct().order_by('id')
        else:
            queryset = Skill.objects.all().order_by('id')


        paginator = Paginator(queryset, 20)

        try:
            skills_page = paginator.page(page_number)
        except PageNotAnInteger:
            # إذا كان رقم الصفحة ليس رقماً، ارجع للصفحة الأولى
            skills_page = paginator.page(1)
        except EmptyPage:
            # إذا كانت الصفحة فارغة (خارج النطاق)، ارجع لآخر صفحة
            skills_page = paginator.page(paginator.num_pages)

        return skills_page