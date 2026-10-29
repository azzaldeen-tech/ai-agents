import os
import sys

import django

# 1. إعداد البيئة
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import City, Skill, SkillCategory

import random
from datetime import date, timedelta
from decimal import Decimal
from companies.models import CompanyProfile, Job


def get_skills_from_list(skill_names):
    """دالة لجلب كائنات المهارات من قاعدة البيانات بناءً على أسمائها"""
    return Skill.objects.filter(name__in=skill_names)




 # تأكد من مسار تطبيق الشركات



def seed_system_jobs():
    print("🚀 جاري بدء توليد البيانات الافتراضية للوظائف وتحليل الاتجاهات...")

    # 1. جلب الكيانات الأساسية من قاعدة البيانات
    companies = list(CompanyProfile.objects.all())
    categories = list(SkillCategory.objects.all())
    cities = list(City.objects.all())

    if not companies or not categories or not cities:
        print("❌ خطأ: يجب تغذية جداول الشركات، فئات المهارات، والمدن أولاً قبل تشغيل هذا السكريبت!")
        return

    # خريطة لتسهيل جلب المهارات حسب الفئة لاحقاً
    skills_by_category = {cat.id: list(Skill.objects.filter(category=cat)) for cat in categories}

    # 2. مصفوفة القوالب الذكية لبناء وظائف تحاكي الواقع
    job_templates = [
        # --- قطاع التقنية والذكاء الاصطناعي ---
        {
            "category_keywords": ["البرمجة", "الذكاء"],
            "titles": [
                {"title": "مهندس ذكاء اصطناعي وتعلّم آلة", "exp": "mid", "sal": (14000, 19000)},
                {"title": "مطور تطبيقات وب كامل (Full-Stack Developer)", "exp": "entry", "sal": (8000, 12000)},
                {"title": "أخصائي أمن سيبراني واختبار اختراق", "exp": "senior", "sal": (20000, 27000)},
                {"title": "مهندس سحابة وعمليات (DevOps Engineer)", "exp": "mid", "sal": (13000, 18000)},
                {"title": "عالم بيانات أول (Senior Data Scientist)", "exp": "senior", "sal": (22000, 32000)}
            ],
            "desc": "نبحث عن محترف للانضمام إلى فريقنا للمساهمة في بناء الأنظمة وتحليل البيانات الضخمة ودعم التحول الرقمي.",
            "req": "شهادة بكالوريوس في علوم الحاسب أو هندسة البرمجيات، مع معرفة جيدة بالتقنيات الحديثة والعمل الجماعي."
        },
        # --- قطاع الهندسة والاستدامة ---
        {
            "category_keywords": ["الهندسة", "الاستدامة"],
            "titles": [
                {"title": "مهندس نظم طاقة متجددة", "exp": "mid", "sal": (12000, 16000)},
                {"title": "أخصائي نمذجة ذكية للمباني (BIM Specialist)", "exp": "entry", "sal": (7500, 11000)},
                {"title": "مهندس إنترنت الأشياء وأتمتة (IoT Engineer)", "exp": "mid", "sal": (11000, 15500)},
                {"title": "مستشار تصميم هندسي مستدام", "exp": "senior", "sal": (18000, 25000)}
            ],
            "desc": "مطلوب مهندس كفوء للعمل على تصميم وإدارة المشاريع الهندسية الحديثة ومتابعة معايير الاستدامة المعتمدة.",
            "req": "بكالوريوس في الهندسة (ميكانيكية/كهربائية/مدنية)، ترخيص من الهيئة السعودية للمهندسين، وإتقان برامج النمذجة."
        },
        # --- قطاع التجارة والاقتصاد الرقمي ---
        {
            "category_keywords": ["التجارة", "الاقتصاد"],
            "titles": [
                {"title": "مدير متجر إلكتروني وتجزئة رقمية", "exp": "mid", "sal": (9000, 14000)},
                {"title": "محلل ذكاء أعمال (Business Intelligence Analyst)", "exp": "mid", "sal": (11000, 16000)},
                {"title": "أخصائي تسويق رقمي وجلب نمو", "exp": "entry", "sal": (6500, 9500)},
                {"title": "خبير تكنولوجيا مالية (FinTech Expert)", "exp": "senior", "sal": (19000, 26000)}
            ],
            "desc": "الهدف من الوظيفة هو قيادة العمليات التسويقية والمالية الرقمية، وتطوير سلاسل الإمداد لرفع الكفاءة التشغيلية.",
            "req": "شهادة في التسويق، المالية، أو نظم المعلومات الإدارية، وإلمام تام بتحليلات السوق والحملات المدفوعة."
        },
        # --- قطاع الإدارة والاستراتيجية ---
        {
            "category_keywords": ["الأعمال", "الإدارة"],
            "titles": [
                {"title": "مدير مشاريع رشاقة (Agile Project Manager)", "exp": "senior", "sal": (18000, 24000)},
                {"title": "أخصائي تخطيط استراتيجي ومستقبلي", "exp": "mid", "sal": (13000, 17500)},
                {"title": "محلل مخاطر والزام مؤسسي", "exp": "mid", "sal": (11500, 15000)},
                {"title": "أخصائي استقطاب مواهب وتحليلات HR", "exp": "entry", "sal": (7000, 10000)}
            ],
            "desc": "المساهمة في رسم الخطط الاستراتيجية وإدارة حوكمة المشاريع والمخاطر، وتوجيه فرق العمل بكفاءة عالية.",
            "req": "بكالوريوس إدارة أعمال أو مالي، ويفضل حمل شهادات مهنية مثل PMP أو SHRM مع مهارات قيادية متميزة."
        },
        # --- قطاع الرعاية الصحية الرقمية ---
        {
            "category_keywords": ["الطب", "الرعاية"],
            "titles": [
                {"title": "مدير منصة طب اتصالي ورعاية عن بعد", "exp": "mid", "sal": (12000, 16500)},
                {"title": "أخصائي جودة صحية واعتماد طبي", "exp": "senior", "sal": (16000, 22000)},
                {"title": "محلل بيانات صحية وطبية", "exp": "entry", "sal": (8000, 11000)}
            ],
            "desc": "العمل على إدارة الأنظمة الصحية الرقمية ومراقبة معايير الجودة الطبية وضمان الامتثال للتشريعات الصحية الحديثة.",
            "req": "شهادة في المعلوماتية الصحية، إدارة الرعاية الصحية أو الطب البشري، مع معرفة بأنظمة الجودة المحلية."
        },
        # --- قطاع التصميم وواجهات المستخدم ---
        {
            "category_keywords": ["التصميم", "واجهات"],
            "titles": [
                {"title": "مصمم تجربة وواجهات مستخدم (UI/UX Designer)", "exp": "mid", "sal": (9500, 14000)},
                {"title": "أخصائي موشن جرافيك وتحرير فيديو", "exp": "entry", "sal": (6000, 9000)},
                {"title": "مصمم هوية بصرية وشعارات", "exp": "mid", "sal": (7500, 11500)}
            ],
            "desc": "ابتكار وتطوير التصاميم الإبداعية للهويات الرقمية وتحسين رحلة المستخدم عبر منصاتنا المختلفة.",
            "req": "معرض أعمال (Portfolio) قوي ومثبت، وإتقان تام لأدوات Figma و Adobe Creative Suite."
        }
    ]

    total_created = 0

    # 3. حلقة التوليد المكثف لضمان توزيع عادل للـ 34 شركة
    # سنقوم بإنشاء وظيفتين لكل شركة (المجموع الإجمالي 68 وظيفة افتراضية)
    for company in companies:
        for _ in range(2):
            # اختيار عشوائي لقالب قطاع تشغيلي
            template = random.choice(job_templates)

            # العثور على الفئة المناسبة من قاعدة البيانات المطابقة للقالب
            category_obj = None
            for cat in categories:
                if any(kw in cat.name for kw in template["category_keywords"]):
                    category_obj = cat
                    break

            if not category_obj:
                category_obj = random.choice(categories)

            # اختيار مسمى وظيفي عشوائي من القالب ومطابقة تفاصيله الماليّة والخبرة
            title_detail = random.choice(template["titles"])

            # تحديد المدينة: نفضل اختيار مدينة الشركة الأساسية أو اختيار مدينة عشوائية أخرى لتمثيل الفروع
            city_obj = City.objects.filter(name__icontains=company.location).first()
            if not city_obj or random.random() > 0.7:
                city_obj = random.choice(cities)

            # اختيار نوع الدوام عشوائياً
            emp_type = random.choice(
                [Job.EmploymentType.FULL_TIME, Job.EmploymentType.FULL_TIME, Job.EmploymentType.PART_TIME,
                 Job.EmploymentType.REMOTE])

            # حساب تواريخ منطقية
            random_days_deadline = random.randint(15, 45)
            deadline_date = date.today() + timedelta(days=random_days_deadline)

            # إنشاء سجل الوظيفة
            job = Job.objects.create(
                city=city_obj,
                company=company,
                category=category_obj,
                title=title_detail["title"],
                description=template["desc"],
                requirements=template["req"],
                location=city_obj.name,
                employment_type=emp_type,
                experience_level=title_detail["exp"],
                min_salary=Decimal(str(title_detail["sal"][0])),
                max_salary=Decimal(str(title_detail["sal"][1])),
                is_active=True,
                deadline=deadline_date
            )

            # 4. ربط المهارات عشوائياً لدعم الـ Trends
            # نأخذ مهارات من نفس الفئة، ونضيف مهارة ناعمة أو لغة لإثراء التحليل
            available_skills = skills_by_category.get(category_obj.id, [])

            # جلب مهارات ناعمة ولغات كمهارات إضافية عامة للوظيفة
            general_cats = SkillCategory.objects.filter(
                name__in=["المهارات الناعمة والمستقبلية", "اللغات والترجمة الاحترافية"])
            extra_skills = []
            for g_cat in general_cats:
                extra_skills.extend(list(Skill.objects.filter(category=g_cat)))

            # دمج المهارات واختيار من 3 إلى 5 مهارات للوظيفة الواحدة
            combined_pool = list(available_skills) + list(extra_skills)
            if combined_pool:
                skills_count = min(len(combined_pool), random.randint(3, 5))
                chosen_skills = random.sample(combined_pool, k=skills_count)
                job.required_skills.set(chosen_skills)

            total_created += 1

    print(
        f"📊 Completed successfully! A virtual job ({total_created}) was generated and distributed to companies, cities, and skills to support the Trends system.")
# def seed_jobs_data():
#     print("🚀 جاري ربط الوظائف والفرص بالشركات والمهارات وتحليل الاتجاهات...")
#
#     # 1. جلب فئات المهارات (المجالات) لربطها بالحقل category
#     tech_category = SkillCategory.objects.filter(name__icontains="البرمجة").first()
#     finance_category = SkillCategory.objects.filter(name__icontains="التجارة").first()
#     admin_category = SkillCategory.objects.filter(name__icontains="الأعمال").first()
#     health_category = SkillCategory.objects.filter(name__icontains="الطب").first()
#
#     # خريطة لربط الشركات بأسماء السجلات المضافة سابقاً
#     companies_dict = {c.name: c for c in CompanyProfile.objects.all()}
#
#     # قائمة بيانات الوظائف المتوافقة مع الموديل الجديد والمهارات المعربة
#     jobs_data = [
#         {
#             "company_name": "مجموعة إس تي سي (stc)",
#             "title": "مهندس حوسبة سحابية أقدم",
#             "description": "نبحث عن مهندس سحابي محترف لإدارة البنية التحتية لخدماتنا الرقمية على منصات AWS و Azure.",
#             "requirements": "خبرة لا تقل عن 5 سنوات في إدارة السيرفرات السحابية والتعامل مع أدوات الأتمتة.",
#             "category": tech_category,
#             "city_name": "الرياض",
#             "employment_type": "full-time",
#             "experience_level": "senior",
#             "min_salary": Decimal("16000.00"),
#             "max_salary": Decimal("22000.00"),
#             "skill_names": ["الحوسبة السحابية (AWS/Azure)", "هندسة العمليات والـ DevOps", "التفكير النقدي والتحليلي"]
#         },
#         {
#             "company_name": "مصرف الراجحي",
#             "title": "محلل ذكاء أعمال (BI Analyst)",
#             "description": "مسؤول عن استخراج البيانات المالية وتحليل سلوك المستهلك لتطوير لوحات تحكم تفاعلية.",
#             "requirements": "إتقان لغة SQL، والتعامل مع أدوات تحليل البيانات مثل PowerBI أو Tableau.",
#             "category": finance_category,
#             "city_name": "الرياض",
#             "employment_type": "full-time",
#             "experience_level": "mid",
#             "min_salary": Decimal("11000.00"),
#             "max_salary": Decimal("15000.00"),
#             "skill_names": ["ذكاء الأعمال (Business Intelligence)", "علم وتحليل البيانات الضخمة (Big Data)", "النمذجة المالية والمحاسبة"]
#         },
#         {
#             "company_name": "شركة علم (Elm)",
#             "title": "مطور تطبيقات واجهات أمامية (React)",
#             "description": "بناء وتطوير واجهات المستخدم للمنصات الحكومية الرقمية والشركات.",
#             "requirements": "خبرة ممتازة في JavaScript وإطار عمل React مع فهم أساسيات الـ UI/UX.",
#             "category": tech_category,
#             "city_name": "الرياض",
#             "employment_type": "full-time",
#             "experience_level": "entry",
#             "min_salary": Decimal("8500.00"),
#             "max_salary": Decimal("11000.00"),
#             "skill_names": ["تطوير المواقع والتطبيقات (Full-Stack)", "تصميم وتجربة المستخدم (UI/UX)", "حل المشكلات المعقدة"]
#         },
#         {
#             "company_name": "مجموعة الدكتور سليمان الحبيب الطبية",
#             "title": "أخصائي إدارة جودة صحية",
#             "description": "مراقبة تطبيق معايير الجودة الطبية والتحول الرقمي للخدمات الاستشفائية داخل المنشأة.",
#             "requirements": "شهادة في إدارة الصحة العامة أو الجودة، وخبرة في الأنظمة الصحية المستدامة.",
#             "category": health_category,
#             "city_name": "الرياض",
#             "employment_type": "full-time",
#             "experience_level": "mid",
#             "min_salary": Decimal("13000.00"),
#             "max_salary": Decimal("17000.00"),
#             "skill_names": ["جودة الرعاية الصحية والاعتماد", "تحليل البيانات الصحية والطبية", "إدارة المشاريع (Agile/Scrum)"]
#         },
#         {
#             "company_name": "طيران الرياض",
#             "title": "مدير مشروع أجايل (Project Manager)",
#             "description": "قيادة وإدارة الفرق التقنية والتشغيلية لبناء الحلول والأنظمة الرقمية لخطوط الطيران الجديدة.",
#             "requirements": "شهادة PMP أو Scrum Master مع خبرة في إدارة المشاريع الهجينة والرشاقة.",
#             "category": admin_category,
#             "city_name": "الرياض",
#             "employment_type": "full-time",
#             "experience_level": "senior",
#             "min_salary": Decimal("20000.00"),
#             "max_salary": Decimal("28000.00"),
#             "skill_names": ["إدارة المشاريع (Agile/Scrum)", "إدارة التغيير المؤسسي", "القيادة التكيفية وإدارة فرق العمل"]
#         },
#         {
#             "company_name": "الخطوط السعودية",
#             "title": "أخصائي تجربة مستخدم (UI/UX Designer)",
#             "description": "تطوير وتحسين تجربة حجز تذاكر الطيران عبر التطبيقات الذكية والموقع الإلكتروني.",
#             "requirements": "إتقان تام لأداة Figma وبناء النماذج الأولية وإجراء بحوث المستخدمين.",
#             "category": tech_category,
#             "city_name": "جدة",
#             "employment_type": "remote",
#             "experience_level": "mid",
#             "min_salary": Decimal("10000.00"),
#             "max_salary": Decimal("14000.00"),
#             "skill_names": ["تصميم الواجهات والتنفيذ عبر Figma", "تصميم وتجربة المستخدم (UI/UX)", "التفكير النقدي والتحليلي"]
#         }
#     ]
#
#     for data in jobs_data:
#         # 1. مطابقة جلب الشركة
#         company_obj = companies_dict.get(data['company_name'])
#         if not company_obj:
#             print(f"⚠️ لم يتم العثور على ملف الشركة في قاعدة البيانات: {data['company_name']}")
#             continue
#
#         # 2. مطابقة جلب كائن المدينة الحقيقي لربطه بالـ ForeignKey
#         city_obj = City.objects.filter(name__icontains=data['city_name']).first()
#         if not city_obj:
#             print(f"⚠️ المدينة '{data['city_name']}' غير موجودة بجدول المدن. سيتم تجاوز الوظيفة.")
#             continue
#
#         if not data['category']:
#             print(f"⚠️ فئة الوظيفة (Category) غير صالحة أو غير متوفرة لـ {data['title']}")
#             continue
#
#         # 3. إنشاء أو تحديث سجل الوظيفة بناءً على البنية الجديدة
#         job, created = Job.objects.update_or_create(
#             company=company_obj,
#             title=data['title'],
#             defaults={
#                 'description': data['description'],
#                 'requirements': data['requirements'],
#                 'category': data['category'],
#                 'city': city_obj,
#                 'location': data['city_name'],  # حقل النص الموازي
#                 'employment_type': data['employment_type'],
#                 'experience_level': data['experience_level'],
#                 'min_salary': data['min_salary'],
#                 'max_salary': data['max_salary'],
#                 'is_active': True,
#                 'deadline': date.today() + timedelta(days=30),  # الموعد النهائي تلقائياً بعد شهر
#             }
#         )
#
#         # 4. ربط المهارات الحقيقية (ManyToMany) لدعم محرك تحليل الاتجاهات
#         existing_skills = get_skills_from_list(data['skill_names'])
#         if existing_skills.exists():
#             job.required_skills.set(existing_skills)
#             print(f"   ✅ تم ربط ({existing_skills.count()}) مهارات بالوظيفة.")
#         else:
#             print(f"   ❓ تنبيه: لم يتم العثور على مهارات متطابقة لـ '{job.title}' في جدول المهارات الأساسي.")
#
#         status = "إنشاء" if created else "تحديث"
#         print(f"📌 [{status} وظيفة] -> {job.title} لدى ({company_obj.name})")
#
#     print("✅ تم الانتهاء من تغذية بيانات الوظائف والاتجاهات المهارية بنجاح!")


if __name__ == '__main__':
    seed_system_jobs()