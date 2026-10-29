from django.db import models
from django.utils.translation import gettext_lazy as _
from config import settings
from django.utils.timesince import timesince

from core.helpers import get_url_view
from core.models import SkillCategory, Skill, City
from members.models import MemberProfile
from django.contrib.humanize.templatetags.humanize import naturaltime

class CompanyProfile(models.Model):

    user = models.OneToOneField(  settings.AUTH_USER_MODEL,on_delete=models.CASCADE,
        related_name='company_profile', verbose_name=_("User Account") )
    name = models.CharField(max_length=150, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, default=_("السعودية"), null=True, blank=True)
    website = models.URLField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    logo = models.ImageField(_("Logo"), upload_to='companies/logos/',
        null=True, blank=True,help_text=_("Preferably 512x512 pixels"))

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")

    @property
    def adv_jobs_number(self):
        """Return the number of jobs advertised by this company."""
        return Job.objects.filter(company=self).count()

    @property
    def active_jobs(self):
        """Returning active jobs by this company"""
        return Job.objects.filter(company=self,is_active=True)

    @property
    def jobs_applications_number(self):
        """Return the total number of applications received for all company jobs"""
        return JobApplication.objects.filter(job__company=self).count()

    @property
    def get_url(self):
        return get_url_view("companies:profile")    \

    @property
    def get_logo_url(self):
        """Return the link to the website logo image"""
        if self.logo and hasattr(self.logo, 'url'):
            try: return self.logo.url
            except ValueError: return ""
        return ""

    def __str__(self):
        return self.name or self.user.username


class Job(models.Model):

    class EmploymentType(models.TextChoices):
        FULL_TIME = 'full-time', _('دوام كامل')
        PART_TIME = 'part-time', _('دوام جزئي')
        REMOTE = 'remote', _('عن بعد')
        CONTRACT = 'contract', _('عقد')

    class ExperienceChoices(models.TextChoices):
        ENTRY = 'entry', _('مبتدئ')
        MID = 'mid', _('متوسط خبرة')
        SENIOR = 'senior', _('خبير')

    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="jobs", verbose_name=_('City'), default=_('الرياض'))
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name="jobs")
    category = models.ForeignKey(SkillCategory, on_delete=models.PROTECT, related_name="jobs",verbose_name=_("مجال الوظيفة"))
    title = models.CharField(max_length=255, verbose_name=_("المسمى الوظيفي"))
    description = models.TextField(verbose_name=_("الوصف الوظيفي"))
    requirements = models.TextField(verbose_name=_("المتطلبات"))
    required_skills = models.ManyToManyField(Skill, related_name="required_skills")

    # Financial and Geographic Analysis Data
    location = models.CharField(max_length=100,default=_("الرياض"))
    employment_type = models.CharField(max_length=50, choices=EmploymentType,default=EmploymentType.FULL_TIME)
    experience_level = models.CharField(max_length=20, choices=ExperienceChoices, default=ExperienceChoices.MID)
    min_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField()

    @property
    def get_created_at(self):
        return f" منذ {naturaltime(self.created_at)}" if self.created_at else ''

    def __str__(self):
        return self.title


class JobApplication(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', _('قيد المراجعة')
        ACCEPTED = 'accepted', _('مقبول')
        REJECTED = 'rejected', _('مرفوض')

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    member = models.ForeignKey(MemberProfile, on_delete=models.CASCADE, related_name="applications")
    match_score = models.FloatField(default=0.0)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status, default=Status.PENDING)

    class Meta:
        verbose_name = _("Job Application")
        verbose_name_plural = _("Job Applications")
        unique_together = ('job', 'member')


class SimpleApplication:
    def __init__(self, app_instance):
        # Extracting "ready-made" data from a complex object
        self.id = app_instance.id
        self.name = app_instance.member.user.get_full_name()
        self.email = app_instance.member.user.email
        self.user_skills = app_instance.member.skills.all
        self.job_skills = app_instance.job.required_skills.all
        self.avater = app_instance.member.user.profile.avater
        self.role = app_instance.job.title
        self.job = app_instance.job
        self.match = app_instance.match_score
        self.status = app_instance.status
        self.status_display = app_instance.get_status_display()
        # self.time = app_instance.applied_at.strftime('%Y-%m-%d')
        self.time = f"منذ {timesince(app_instance.applied_at)}"

    def __str__(self):
        return f"{self.name}"










