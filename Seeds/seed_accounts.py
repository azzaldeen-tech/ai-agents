import os
import sys
import django

# إعداد البيئة
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from accounts.models import Role
from members.models import MemberProfile

User = get_user_model()


def seed_users():
    # 1. إنشاء دور العضو (Member Role)
    identity_obj, _ = Role.objects.get_or_create(
        code="member",
        defaults={
            "name": "member",
            "description": "member",
            "is_identity": True,
            "requires_approval": False,
            "view_in_register": True
        }
    )

    # 2. بيانات المستخدمين
    users_data = [
        {
            "username": "user789",
            "email": "user789@gmail.com",
            "password": "Test@123",
            "birth_date": "2005-03-02",
            "first_name": "مستخدم",
            "last_name": "أساسي",
            "status": "active",
        },
        {
            "username": "ali7798",
            "email": "ali7798@gmail.com",
            "password": "Test@123",
            "first_name": "علي",
            "last_name": "أحمد",
            "birth_date": "2007-03-02",
            "status": "active",
        },
    ]

    print(f"🚀 Starting Seeding of {len(users_data)} diverse Member Profiles...")

    for item in users_data:
        # 3. إنشاء المستخدم
        user, u_created = User.objects.get_or_create(
            username=item['username'],
            defaults={
                'email': item['email'],
                'password': make_password(item['password']),
                'identity': identity_obj,
                'is_active': True
            }
        )

        # 4. إنشاء أو تحديث الملف الشخصي
        profile, p_created = MemberProfile.objects.update_or_create(
            user=user,
            defaults={
                'first_name': item['first_name'],
                'last_name': item['last_name'],
                'birth_date': item['birth_date']
            }
        )

        status = "Created" if p_created else "Updated"
        print(f"👤 [{status}] -> {item['first_name']} {item['last_name']} ({item['username']})")

    print(f"✅ Seeding Complete! {len(users_data)} unique member profiles are operational.")

if __name__ == '__main__':
    seed_users()

