from django.db import models
from django.utils.translation import gettext_lazy as _
from config import settings
from core.helpers import get_url_view
from core.models import Skill

class MemberProfile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='member_profile',verbose_name=_("User Account") )
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    skills = models.ManyToManyField(Skill, null=True, blank=True,related_name="skills")
    avater = models.ImageField(  _("Avater"),  upload_to='members/avaters/', null=True,blank=True,help_text=_("Preferably 512x512 pixels"))
    class Meta:
        verbose_name = _("Member")
        verbose_name_plural = _("Members")
    def __str__(self):
        return self.name
    @property
    def name(self):
        return f"{self.first_name or ''} {self.last_name or ''}".strip()  or self.user.username
    @property
    def get_url(self):
        return get_url_view("members:profile")
    @property
    def get_avater_url(self):
        if self.avater and hasattr(self.avater, 'url'):
            try:
                return self.avater.url
            except ValueError:
                return ""
        return ""
    @property
    def nav_stats(self):
        from .services import MemberService
        return MemberService.get_global_stats(self.id)

