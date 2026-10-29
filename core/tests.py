# from django.db import models
# from django.contrib.auth.models import User
# import json
# from django.utils.translation import gettext_lazy as _
# from accounts.models import CustomUser
# from config import settings
#
#
# # دالة مساعدة لإنشاء هيكل لغوي افتراضي
# def default_lang_dict():
#     return {"ar": "", "en": ""}
#
#
# # 1. جدول المسميات الوظيفية الموحدة
# class StandardTitle(models.Model):
#     # نخزن الأسماء كـ Text ونحولها لـ JSON برمجياً لضمان التوافق
#     names_json = models.TextField(default=json.dumps(default_lang_dict()), verbose_name="المسميات (JSON)")
#     slug = models.SlugField(unique=True, help_text="رابط فريد للمسمى الوظيفي")
#     category = models.CharField(max_length=100, verbose_name="التصنيف المهني")
#
#     @property
#     def name(self):
#         """دالة لاسترجاع الاسم كـ Dictionary"""
#         try:
#             return json.loads(self.names_json)
#         except:
#             return default_lang_dict()
#
#     def __str__(self):
#         return self.name.get('ar') or self.name.get('en') or self.slug
#
#
# # 2. جدول المهارات الموحدة
# class StandardSkill(models.Model):
#     # SKILL_TYPES = [
#     #     ('tech', 'تقنية / Hard Skill'),
#     #     ('soft', 'ناعمة / Soft Skill'),
#     #     ('tool', 'أداة / Tool'),
#     # ]
#     class SkillTypes(models.TextChoices):
#         TECH = 'tech', _('Tech')
#         SOFT = 'soft', _('Soft')
#         TOOL = 'tool', _('Tool')
#
#
#     names_json = models.TextField(default=json.dumps(default_lang_dict()), verbose_name="اسم المهارة (JSON)")
#     skill_type = models.CharField(max_length=20, choices=SkillTypes, default='tech')
#     search_keywords = models.TextField(help_text="كلمات يستخدمها الـ Scraper للمطابقة (فصل بينها بفاصلة)")
#
#     @property
#     def name(self):
#         try:
#             return json.loads(self.names_json)
#         except:
#             return default_lang_dict()
#
#     def __str__(self):
#         return self.name.get('en') or self.name.get('ar')
#
#
# # 3. جدول الإعلانات الوظيفية (الهجين)
# class JobAdvertisement(models.Model):
#     SOURCE_CHOICES = [
#         ('scraped', 'سحب آلي / Scraped'),
#         ('manual', 'إضافة يدوية / Employer'),
#     ]
#
#     # الربط بالمسميات الموحدة (المرجع)
#     title_ref = models.ForeignKey(
#         StandardTitle,
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name="ads",
#         verbose_name="المسمى الموحد"
#     )
#
#     # الربط بالمهارات (علاقة متعدد لمتعدد)
#     skills = models.ManyToManyField(StandardSkill, related_name="jobs", verbose_name="المهارات المطلوبة")
#
#     # بيانات الإعلان
#     raw_title = models.CharField(max_length=500, verbose_name="العنوان الأصلي")
#     company_name = models.CharField(max_length=255, verbose_name="اسم الشركة")
#     description = models.TextField(verbose_name="الوصف الوظيفي")
#     location = models.CharField(max_length=255, default="اليمن", verbose_name="الموقع")
#
#     # المصدر والتوثيق
#     source_type = models.CharField(max_length=10, choices=SOURCE_CHOICES, default='scraped')
#     source_url = models.URLField(max_length=500, null=True, blank=True)
#     employer = models.ForeignKey(CustomUser,
#                                  on_delete=models.SET_NULL,
#                                  null=True,
#                                  blank=True,
#                                  related_name="posted_jobs")
#
#     scraped_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         ordering = ['-scraped_at']
#
#     def __str__(self):
#         return f"{self.raw_title} @ {self.company_name}"
#
#
# # 4. جدول ملف الطالب (للمطابقة والتقديم)
# class StudentProfile(models.Model):
#
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='profile',
#         verbose_name=_("User Account")
#     )
#
#     major = models.CharField(max_length=200, verbose_name="التخصص الجامعي")
#
#     # مهارات الطالب (المفتاح للمطابقة الذكية)
#     skills = models.ManyToManyField(StandardSkill, related_name="students", verbose_name="مهاراتي")
#
#     bio = models.TextField(blank=True, verbose_name="نبذة شخصية")
#     cv_file = models.FileField(upload_to='cvs/', null=True, blank=True)
#
#     def __str__(self):
#         return self.user.username
#
#
# # 5. جدول طلبات التوظيف (بوابة التوظيف)
# class JobApplication(models.Model):
#     STATUS_CHOICES = [
#         ('pending', 'قيد المراجعة'),
#         ('accepted', 'مقبول مبدئياً'),
#         ('rejected', 'مرفوض'),
#     ]
#     student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="applications")
#     job_ad = models.ForeignKey(JobAdvertisement, on_delete=models.CASCADE, related_name="applications")
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
#     applied_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         unique_together = ('student', 'job_ad')  # لمنع الطالب من التقديم مرتين على نفس الوظيفة