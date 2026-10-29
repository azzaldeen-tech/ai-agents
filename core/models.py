from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _



class Country(models.Model):
    name = models.CharField(_("name"), max_length=255, blank=False)
    code = models.CharField(_("code"), max_length=10, unique=True, blank=False)
    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")

    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(_("name"), max_length=255, blank=False)
    code = models.CharField(_("code"), max_length=10, unique=True, blank=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="regions")
    class Meta:
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")
    def __str__(self):
        return f"{self.name}"

class City(models.Model):
    name = models.CharField(_("name"), max_length=255, blank=False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="cities")

    class Meta:
        verbose_name = _("City")  # سيتم البحث عن ترجمة هذه الكلمة
        verbose_name_plural = _("Cities")

    def __str__(self):
        return f"{self.name}"





class SkillCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name="Category")
    slug = models.SlugField(unique=True, help_text="Write the link in English here (e.g., web-development)")
    icon = models.CharField(max_length=50,null=True, blank=True, help_text="FontAwesome icon class")

    class Meta:
        verbose_name = _("Specializations")
        verbose_name_plural = _("Specializations")

    def __str__(self):
        return self.name


class Skill(models.Model):
    suggested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=100, unique=True)
    is_verified = models.BooleanField(default=True, verbose_name=_("Verified by the admin"))

    class Meta:
        verbose_name = _("Skill")
        verbose_name_plural = _("Skills")

    def __str__(self):
        return self.name










class FavoriteJobs(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorite_jobs',
        verbose_name="User Account"
    )
    # member = models.ForeignKey(MemberProfile, on_delete=models.CASCADE, related_name="favoriteJobs")
    job_id = models.CharField()
    # job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="favorite_jobs")
    created_at = models.DateTimeField(auto_now_add=True)

