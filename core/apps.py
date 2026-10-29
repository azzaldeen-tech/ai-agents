from django.apps import AppConfig

from core.AutoGenerator import GeneratorIdentityApps



class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # TODO: Auto Generator Identity apps
        # الكود الذي تضعه هنا سيعمل مرة واحدة عند تشغيل المشروع
        print("<< the server is Start working >>")
        GeneratorIdentityApps()
