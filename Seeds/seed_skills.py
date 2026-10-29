import os
import sys
import django
from django.utils.text import slugify


# 1. إعداد المسارات (للتأكد من رؤية التطبيقات)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')
sys.path.append(project_root)

# 2. إعداد بيئة Django (يجب أن يتم قبل استيراد أي موديل)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings') # تأكد من اسم مجلد الإعدادات لديك
django.setup()


from core.models import Skill, SkillCategory




def seed_skills():

    # هيكل البيانات: الفئة -> الأيقونة -> المهارات
    data = {
        "البرمجة والذكاء الاصطناعي": {
            "icon": "terminal",
            "skills": [
                "برمجة Python (Django/FastAPI)",
                "الذكاء الاصطناعي وتعلم الآلة (AI/ML)",
                "علم وتحليل البيانات الضخمة (Big Data)",
                "الأمن السيبراني واختبار الاختراق",
                "الحوسبة السحابية (AWS/Azure)",
                "تطوير المواقع والتطبيقات (Full-Stack)",
                "هندسة العمليات والـ DevOps"
            ]
        },
        "الهندسة والاستدامة": {
            "icon": "cpu",
            "skills": [
                "هندسة نظم الطاقة المتجددة",
                "الروبوتات والأتمتة الصناعية",
                "النمذجة الذكية للمباني (BIM)",
                "هندسة إنترنت الأشياء (IoT)",
                "الهندسة الطبية الحيوية",
                "التصميم الهندسي المستدام"
            ]
        },
        "الطب والرعاية الصحية الرقمية": {
            "icon": "heart-pulse",
            "skills": [
                "إدارة منصات الطب الاتصالي (عن بُعد)",
                "تحليل البيانات الصحية والطبية",
                "الأبحاث السريرية وعلم الجينوم",
                "إدارة الصحة العامة والأوبئة",
                "الاستشارات والصحة النفسية",
                "جودة الرعاية الصحية والاعتماد"
            ]
        },
        "التجارة والاقتصاد الرقمي": {
            "icon": "trending-up",
            "skills": [
                "التكنولوجيا المالية (FinTech)",
                "إدارة المتاجر والتجارة الإلكترونية",
                "سلاسل الإمداد والخدمات اللوجستية الذكية",
                "ذكاء الأعمال (Business Intelligence)",
                "التسويق الرقمي وجلب النمو (Growth Hacking)",
                "تحسين محركات البحث والإعلانات الرقمية (SEO)"
            ]
        },
        "الأعمال والإدارة الاستراتيجية": {
            "icon": "briefcase",
            "skills": [
                "إدارة المشاريع (Agile/Scrum)",
                "إدارة التغيير المؤسسي",
                "التخطيط الاستراتيجي والمستقبلي",
                "تحليلات الموارد البشرية واستقطاب المواهب",
                "النمذجة المالية والمحاسبة",
                "إدارة المخاطر والالتزام"
            ]
        },
        "التصميم وواجهات المستخدم": {
            "icon": "palette",
            "skills": [
                "تصميم وتجربة المستخدم (UI/UX)",
                "تصميم الواجهات والتنفيذ عبر Figma",
                "الموشن جرافيك وتحرير الفيديو",
                "تصميم الهوية البصرية والشعارات",
                "التصميم ثلاثي الأبعاد (3D Modeling)"
            ]
        },
        "المهارات الناعمة والمستقبلية": {
            "icon": "users",
            "skills": [
                "التفكير النقدي والتحليلي",
                "حل المشكلات المعقدة",
                "القيادة التكيفية وإدارة فرق العمل",
                "العمل الجماعي وتكامل المهارات",
                "الذكاء العاطفي والاجتماعي",
                "الإلقاء والتحدث أمام الجمهور"
            ]
        },
        "اللغات والترجمة الاحترافية": {
            "icon": "languages",
            "skills": [
                "اللغة الإنجليزية للأعمال",
                "الكتابة الإبداعية وصياغة المحتوى العربي",
                "الترجمة الفورية والتحريرية",
                "الكتابة والتوثيق التقني"
            ]
        }
    }

    for cat_name, info in data.items():

        generated_slug = slugify(cat_name, allow_unicode=True)
        category, created = SkillCategory.objects.get_or_create(
            name=cat_name,
            defaults={
                'icon': info['icon'],
                'slug': generated_slug
            }
        )


        # تحديث الأيقونة إذا كانت الفئة موجودة مسبقاً بأيقونة مختلفة
        if not created and category.icon != info['icon']:
            category.icon = info['icon']
            category.save()

        # 2. إنشاء المهارات وربطها بالفئة
        for skill_name in info['skills']:
            Skill.objects.get_or_create(
                name=skill_name,
                category=category
            )

print("✅ The categories, icons, and skills data were successfully fed in.")


if __name__ == '__main__':
    seed_skills()