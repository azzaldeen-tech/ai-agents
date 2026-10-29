import os
import sys
import django
from core.models import Country,Region, City

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')
sys.path.append(project_root)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()




def seed_saudi_geo_data():

    saudi_arabia, created = Country.objects.get_or_create(
        name='السعودية',
        defaults={'code': 'KSA'}
    )

    if created:
        print("🇸🇦 Country 'Saudi Arabia' created for the first time.")

    data = {
        "منطقة الرياض": {
            "code": "RUH",
            "cities": ["الرياض", "الخرج", "المجمعة", "الدرعية"]
        },
        "منطقة مكة المكرمة": {
            "code": "MKH",
            "cities": ["مكة المكرمة", "جدة", "الطائف", "رابغ"]
        },
        "المنطقة الشرقية": {
            "code": "EPR",
            "cities": ["الدمام", "الخبر", "الجبيل", "الأحساء", "حفر الباطن"]
        },
        "منطقة المدينة المنورة": {
            "code": "MED",
            "cities": ["المدينة المنورة", "ينبع", "العلا"]
        },
        "منطقة القصيم": {
            "code": "QAS",
            "cities": ["بريدة", "عنيزة", "الرس"]
        },
        "منطقة عسير": {
            "code": "ASR",
            "cities": ["أبها", "خميس مشيط", "بيشة"]
        },
        "منطقة تبوك": {
            "code": "TAB",
            "cities": ["تبوك", "أملج"]
        },
    }

    print("🚀 Starting the process of entering geographic data...")

    for reg_name, info in data.items():
        region, created = Region.objects.get_or_create(
            name=reg_name,
            country=saudi_arabia,
            defaults={'code': info['code']}
        )
        if created:
            print(f"📍 The region was created: {reg_name}")

        for city_name in info['cities']:
            City.objects.get_or_create(
                name=city_name,
                region=region
            )
    print("✅ Region and city data updated successfully!")


if __name__ == '__main__':
    seed_saudi_geo_data()