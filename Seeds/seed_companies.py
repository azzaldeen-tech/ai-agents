import os
import sys

import django


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from companies.models import CompanyProfile
from accounts.models import Role






User = get_user_model()

def seed_bulk_companies():
    # 1. جلب أو إنشاء دور "صاحب العمل / الشركة"
    identity_obj, _ = Role.objects.get_or_create(
        code="company",
        defaults={
            "name": "company",
            "description": "Organizations and employers looking for talents and analyzing market trends",
            "is_identity": True,
            "requires_approval": True,
            "view_in_register": True
        }
    )

    # قائمة ضخمة تحتوي على 34 شركة متنوعة
    companies_data = [
        # --- قطاع الطاقة والصناعة ---
        {
            "username": "aramco_corp", "email": "careers@aramco.com", "password": "Test@123",
            "name": "شركة أرامكو السعودية", "location": "الظهران", "website": "https://www.aramco.com",
            "is_verified": True, "status": "active",
            "bio": "الشركة الرائدة عالمياً في مجال الطاقة والكيميائيات، ونوفر فرص عمل للكفاءات المتميزة المتقدمة."
        },
        {
            "username": "sabic_industries", "email": "recruitment@sabic.com", "password": "Test@123",
            "name": "الشركة السعودية للصناعات الأساسية (سابك)", "location": "الجبيل", "website": "https://www.sabic.com",
            "is_verified": True, "status": "active",
            "bio": "شركة عالمية رائدة في مجال البتروكيماويات والمواد المتخصصة والمبتكرة."
        },
        {
            "username": "maaden_mining", "email": "hr@maaden.com.sa", "password": "Test@123",
            "name": "شركة التعدين العربية السعودية (معادن)", "location": "الرياض", "website": "https://www.maaden.com.sa",
            "is_verified": True, "status": "active",
            "bio": "قائد قطاع التعدين بالمملكة، نعمل على تطوير الثروات المعدنية عبر حلول مستدامة."
        },
        {
            "username": "se_electricity", "email": "jobs@se.com.sa", "password": "Test@123",
            "name": "الشركة السعودية للكهرباء", "location": "الرياض", "website": "https://www.se.com.sa",
            "is_verified": True, "status": "active",
            "bio": "المزود الرئيسي للخدمة الكهربائية بالمملكة، نسعى لتمكين بيئة طاقة مستدامة وموثوقة."
        },

        # --- قطاع الاتصالات والتقنية ---
        {
            "username": "stc_carrier", "email": "recruitment@stc.com.sa", "password": "Test@123",
            "name": "مجموعة إس تي سي (stc)", "location": "الرياض", "website": "https://www.stc.com.sa",
            "is_verified": True, "status": "active",
            "bio": "الممكن الرقمي الرائد في المنطقة، نقدم خدمات الاتصالات وتقنية المعلومات والحلول المتقدمة."
        },
        {
            "username": "mobily_telecom", "email": "careers@mobily.com.sa", "password": "Test@123",
            "name": "شركة اتحاد اتصالات (موبايلي)", "location": "الرياض", "website": "https://www.mobily.com.sa",
            "is_verified": True, "status": "active",
            "bio": "شركة اتصالات رائدة تقدم خدمات الهاتف المحمول والبيانات والحلول الذكية للأفراد والشركات."
        },
        {
            "username": "zain_saudi", "email": "jobs@sa.zain.com", "password": "Test@123",
            "name": "شركة زين السعودية", "location": "الرياض", "website": "https://www.sa.zain.com",
            "is_verified": True, "status": "active",
            "bio": "رائد شبكات الجيل الخامس والخدمات الرقمية المبتكرة في منظومة الاتصالات المتكاملة."
        },
        {
            "username": "elm_company", "email": "talent@elm.sa", "password": "Test@123",
            "name": "شركة علم (Elm)", "location": "الرياض", "website": "https://www.elm.sa",
            "is_verified": True, "status": "active",
            "bio": "شركة رائدة في تقديم الحلول الرقمية المتكاملة، وتطوير المنتجات الإلكترونية والخدمات الاستشارية."
        },
        {
            "username": "thiqah_tech", "email": "hr@thiqah.sa", "password": "Test@123",
            "name": "شركة ثقة لخدمات الأعمال", "location": "الرياض", "website": "https://www.thiqah.sa",
            "is_verified": True, "status": "active",
            "bio": "شريك ذكي يقدم حلولاً إبداعية تعتمد على البيانات لدعم وتطوير قطاع الأعمال الذكي."
        },
        {
            "username": "lean_business", "email": "careers@lean.sa", "password": "Test@123",
            "name": "شركة لين لخدمات الأعمال", "location": "الرياض", "website": "https://www.lean.sa",
            "is_verified": True, "status": "active",
            "bio": "تمكين القطاع الصحي رقمياً عبر ابتكار حلول ومنتجات تقنية ترفع من جودة الرعاية الصحية."
        },

        # --- قطاع البنوك والمالية ---
        {
            "username": "rajhi_bank", "email": "careers@alrajhibank.com.sa", "password": "Test@123",
            "name": "مصرف الراجحي", "location": "الرياض", "website": "https://www.alrajhibank.com.sa",
            "is_verified": True, "status": "active",
            "bio": "أحد أكبر المصارف الإسلامية في العالم، نلتزم بتقديم حلول مصرفية متكاملة ومبتكرة."
        },
        {
            "username": "snb_bank", "email": "recruitment@alahli.com", "password": "Test@123",
            "name": "البنك الأهلي السعودي (SNB)", "location": "جدة", "website": "https://www.alahli.com",
            "is_verified": True, "status": "active",
            "bio": "أكبر مؤسسة مالية في المملكة العربية السعودية، ندير التحولات المالية الكبرى بكفاءة واحترافية."
        },
        {
            "username": "riyad_bank", "email": "careers@riyadbank.com", "password": "Test@123",
            "name": "بنك الرياض", "location": "الرياض", "website": "https://www.riyadbank.com",
            "is_verified": True, "status": "active",
            "bio": "مؤسسة مالية عريقة تسعى لتقديم خدمات تمويلية واستثمارية مرنة للأفراد والشركات الكبرى."
        },
        {
            "username": "alinma_bank", "email": "hr@alinma.com", "password": "Test@123",
            "name": "مصرف الإنماء", "location": "الرياض", "website": "https://www.alinma.com",
            "is_verified": True, "status": "active",
            "bio": "مصرفية متوافقة مع الأحكام الشريعة برؤية عصرية ومستقبل رقمي يضمن تلبية تطلعات الشركاء."
        },
        {
            "username": "albilad_bank", "email": "jobs@bankalbilad.com", "password": "Test@123",
            "name": "بنك البلاد", "location": "الرياض", "website": "https://www.bankalbilad.com",
            "is_verified": True, "status": "active",
            "bio": "حلول مصرفية مبتكرة تعتمد على التحول الرقمي الشامل لخدمة المجتمع والاقتصاد النامي."
        },

        # --- قطاع التطوير العقاري والمشاريع الكبرى ---
        {
            "username": "neom_project", "email": "careers@neom.com", "password": "Test@123",
            "name": "شركة نيوم (NEOM)", "location": "تبوك", "website": "https://www.neom.com",
            "is_verified": True, "status": "active",
            "bio": "أرض المستقبل وموطن الابتكار العالمي، نعمل على صياغة مفهوم جديد للمعيشة المستدامة."
        },
        {
            "username": "redsea_global", "email": "jobs@redseaglobal.com", "password": "Test@123",
            "name": "البحر الأحمر الدولية", "location": "جدة", "website": "https://www.redseaglobal.com",
            "is_verified": True, "status": "active",
            "bio": "نقود التطوير العقاري المتجدد عبر مشاريع سياحية فاخرة تحمي البيئة وتعزز التنوع."
        },
        {
            "username": "roshn_property", "email": "careers@roshn.sa", "password": "Test@123",
            "name": "مجموعة روشن العقارية", "location": "الرياض", "website": "https://www.roshn.sa",
            "is_verified": True, "status": "active",
            "bio": "مطور عقاري وطني رائد يعمل على رفع جودة المعيشة وتطوير مجتمعات سكنية عصرية ومستدامة."
        },
        {
            "username": "diriyah_gate", "email": "hr@dgda.gov.sa", "password": "Test@123",
            "name": "هيئة تطوير بوابة الدرعية", "location": "الدرعية", "website": "https://www.diriyah.sa",
            "is_verified": True, "status": "active",
            "bio": "نعمل على تحويل الدرعية التاريخية إلى وجهة ثقافية وسياحية عالمية تحتفي بالهوية السعودية."
        },
        {
            "username": "quddiya_investment", "email": "jobs@qiddiya.com", "password": "Test@123",
            "name": "شركة التطوير والاستثمار لـ القدية", "location": "الرياض", "website": "https://qiddiya.com",
            "is_verified": True, "status": "active",
            "bio": "عاصمة الترفيه والرياضة والفنون المستقبلية بالمملكة، نبني تجارب ترفيهية غير مسبوقة."
        },

        # --- قطاع النقل والطيران لوجستيات ---
        {
            "username": "saudia_airlines", "email": "jobs@saudia.com", "password": "Test@123",
            "name": "الخطوط السعودية", "location": "جدة", "website": "https://www.saudia.com",
            "is_verified": True, "status": "active",
            "bio": "الناقل الوطني للمملكة العربية السعودية، نربط العالم بالمملكة عبر تجارب طيران مميزة."
        },
        {
            "username": "riyadh_air", "email": "careers@riyadhair.com", "password": "Test@123",
            "name": "طيران الرياض", "location": "الرياض", "website": "https://www.riyadhair.com",
            "is_verified": True, "status": "active",
            "bio": "الناقل الجوي الوطني الجديد، نتبنى أحدث معايير التقنية والاستدامة لنقود قطاع الطيران مستقبلاً."
        },
        {
            "username": "flynas_hr", "email": "recruitment@flynas.com", "password": "Test@123",
            "name": "طيران ناس (flynas)", "location": "الرياض", "website": "https://www.flynas.com",
            "is_verified": True, "status": "active",
            "bio": "الطيران الاقتصادي الرائد في الشرق الأوسط، نربط الوجهات بخيارات سفر ذكية وقيمة منافسة."
        },
        {
            "username": "spl_post", "email": "careers@splonline.com.sa", "password": "Test@123",
            "name": "البريد السعودي (سبل)", "location": "الرياض", "website": "https://www.splonline.com.sa",
            "is_verified": True, "status": "active",
            "bio": "المشغل اللوجستي الوطني، نطور حلول بريدية وخدمات إمداد متطورة لدعم الاقتصاد الرقمي."
        },
        {
            "username": "bahri_shipping", "email": "hr@bahri.sa", "password": "Test@123",
            "name": "الشركة الوطنية السعودية للنقل البحري (البحري)", "location": "الرياض", "website": "https://www.bahri.sa",
            "is_verified": True, "status": "active",
            "bio": "رائد عالمي في قطاع النقل والخدمات اللوجستية، ندير أساطيل شحن بحرية عملاقة ومتنوعة."
        },

        # --- قطاع الرعاية الصحية والأدوية ---
        {
            "username": "habib_medical", "email": "careers@hmg.com", "password": "Test@123",
            "name": "مجموعة الدكتور سليمان الحبيب الطبية", "location": "الرياض", "website": "https://hmg.com",
            "is_verified": True, "status": "active",
            "bio": "مؤسسة طبية رائدة توفر رعاية صحية شاملة وتعتمد على أحدث التقنيات الرقمية والكوادر المتميزة."
        },
        {
            "username": "dallah_health", "email": "jobs@dallahhealth.com", "password": "Test@123",
            "name": "شركة دله للرعاية الصحية", "location": "الرياض", "website": "https://www.dallahhealth.com",
            "is_verified": True, "status": "active",
            "bio": "منظومة طبية عريقة تلتزم بتقديم أفضل الخدمات الاستشفائية وفق أعلى المعايير العالمية."
        },
        {
            "username": "bupa_arabia", "email": "recruitment@bupa.com.sa", "password": "Test@123",
            "name": "بوبا العربية للتأمين التعاوني", "location": "جدة", "website": "https://www.bupa.com.sa",
            "is_verified": True, "status": "active",
            "bio": "شريك الرعاية الصحية والتأمين الطبي الأكبر بالمملكة، نوفر رعاية متميزة لبيئات العمل العصرية."
        },
        {
            "username": "spimaco_pharma", "email": "hr@spimaco.sa", "password": "Test@123",
            "name": "الشركة السعودية للصناعات الدوائية والمستلزمات الطبية (سبيماكو)", "location": "القصيم", "website": "https://www.spimaco.com.sa",
            "is_verified": True, "status": "active",
            "bio": "رائد صناعة الأدوية في المملكة، نساهم في تحقيق الأمن الدوائي عبر منتجات علاجية موثوقة."
        },

        # --- قطاع التجزئة والأغذية والأعمال ---
        {
            "username": "jarir_bookstore", "email": "hr@jarir.com", "password": "Test@123",
            "name": "مكتبة جرير", "location": "الخبر", "website": "https://www.jarir.com",
            "is_verified": True, "status": "active",
            "bio": "الشركة الرائدة في التكنولوجيا، الأدوات المكتبية، والكتب التعليمية والمترجمة في الشرق الأوسط."
        },
        {
            "username": "almarai_co", "email": "recruitment@almarai.com", "password": "Test@123",
            "name": "شركة المراعي", "location": "الرياض", "website": "https://www.almarai.com",
            "is_verified": True, "status": "active",
            "bio": "أكبر شركة متكاملة لمنتجات الألبان والعصائر في العالم، نغذي الجودة كل يوم بكفاءاتنا الوطنية."
        },
        {
            "username": "savola_group", "email": "careers@savola.com", "password": "Test@123",
            "name": "مجموعة صافولا", "location": "جدة", "website": "https://www.savola.com",
            "is_verified": True, "status": "active",
            "bio": "مجموعة استثمارية صناعية رائدة تركز على قطاع الأغذية والتجزئة بأسواق الشرق الأوسط الواعدة."
        },
        {
            "username": "panda_retail", "email": "jobs@panda.com.sa", "password": "Test@123",
            "name": "شركة العزيزية بندة المتحدة", "location": "جدة", "website": "https://www.panda.com.sa",
            "is_verified": True, "status": "active",
            "bio": "سلسلة أسواق التجزئة الكبرى والأوسع انتشاراً بالمملكة العربية السعودية لخدمة ملايين العملاء."
        },
        {
            "username": "nahdi_medical", "email": "careers@nahdi.sa", "password": "Test@123",
            "name": "شركة النهدي الطبية", "location": "جدة", "website": "https://www.nahdi.sa",
            "is_verified": True, "status": "active",
            "bio": "أكبر سلسلة صيدليات تجزئة بالمنطقة، ننبض بالأمل ونقدم رعاية وخدمات مجتمعية متكاملة."
        }
    ]

    print(f"🚀 Starting Bulk Seeding of {len(companies_data)} diverse Company Profiles...")

    for item in companies_data:
        # 1. إنشاء أو جلب حساب المستخدم (User Auth)
        user, u_created = User.objects.get_or_create(
            username=item['username'],
            defaults={
                'email': item['email'],
                'password': make_password(item['password']),
                'identity': identity_obj,
                'is_active': True
            }
        )

        # 2. إنشاء أو تحديث ملف الشركة (Company Profile)
        profile, p_created = CompanyProfile.objects.update_or_create(
            user=user,
            defaults={
                'name': item['name'],
                'location': item['location'],
                'website': item['website'],
                'bio': item['bio'],
                'is_verified': item['is_verified'],
                # 'status': item['status'],
                # 'is_available': True
            }
        )

        status = "Created" if p_created else "Updated"
        print(f"🏢 [{status}] -> {item['name']} ({item['location']})")

    print(f"✅ Seeding Complete! {len(companies_data)} unique company profiles are operational.")

if __name__ == '__main__':
    seed_bulk_companies()

