from datetime import date
from email._header_value_parser import ContentType

from django import forms
from setuptools.config._validate_pyproject import ValidationError
from django.utils.translation import gettext_lazy as _
from companies.models import CompanyProfile
from core.helpers import get_identity_domain
from members.models import MemberProfile
from .models import *
from allauth.account.forms import SignupForm
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import uuid

class BaseStyledForm(forms.Form):  # وراثة مباشرة من forms.Form
    base_classes = (
        "bg-base text-content border border-stroke-soft px-4 py-2 mt-1 rounded-lg "
        "focus:ring-2 transition duration-200 outline-none w-full shadow-sm"
    )
    error_classes = "border-red-500 focus:ring-red-500 text-red-600"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_tailwind_styles()

    def apply_tailwind_styles(self):
        for field_name, field in self.fields.items():
            existing = field.widget.attrs.get('class', '')
            current_classes = self.base_classes
            if self.errors.get(field_name):
                current_classes += f" {self.error_classes}"
            field.widget.attrs['class'] = f"{existing} {current_classes}".strip()


class BaseAccountSignupForm(SignupForm, BaseStyledForm):
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )
    identity = forms.ModelChoiceField(
        queryset=Role.objects.filter(view_in_register=True, is_identity=True),
        widget=forms.HiddenInput(),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # إخفاء اليوزرنيم وجعله غير مطلوب في الـ HTML
        if 'username' in self.fields:
            self.fields['username'].widget = forms.HiddenInput()
            self.fields['username'].required = False

        role_code = getattr(self, 'role_code', None)
        if role_code:
            if 'email' in self.fields:
                domain = get_identity_domain(role_code)
                domain = 'gmail' if not domain else domain
                self.fields['email'].widget.attrs.update({
                    'placeholder': f'example@{domain}.com'
                })

            role = Role.objects.filter(code=role_code, view_in_register=True, is_identity=True).first()
            if role:
                self.fields['identity'].initial = role.id

        self.apply_tailwind_styles()

    # استخدام clean الشاملة لضمان توليد اسم المستخدم بشكل صحيح تماماً
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        if email:
            # 1. أخذ الجزء الأول فقط من الإيميل وتحويله لنص مناسب (Slug)
            base_username = email.split('@')[0]
            username = slugify(base_username)

            # إذا كان الـ slug فارغاً لأي سبب (مثلاً الإيميل بلغة تسبب مسح الحروف)
            if not username:
                username = "user"

            User = get_user_model()

            # 2. التأكد من عدم تكرار اليوزرنيم
            while User.objects.filter(username=username).exists():
                username = f"{slugify(base_username)}_{uuid.uuid4().hex[:4]}"

            # 3. حقن اليوزرنيم داخل البيانات التي تم التحقق منها
            cleaned_data['username'] = username
            self.errors.pop('username', None)  # حذف أي خطأ سابق يخص اليوزرنيم

        return cleaned_data


# الآن تصبح الكلاسات الفرعية بسيطة جداً وممركزة
class MemberSignupForm(BaseAccountSignupForm):

    role_code = "member"

    first_name = forms.CharField(max_length=50, label=_('First Name'),
                                 widget=forms.TextInput(attrs={'placeholder': _('Enter first name')}))
    last_name = forms.CharField(max_length=50, label=_('Last Name'),
                                widget=forms.TextInput(attrs={'placeholder': _('Enter last name')}))

    birth_date = forms.DateField(label=_("Birth Date"),widget=forms.DateInput(attrs={"type":"date"}))

    field_order = ['first_name', 'last_name','birth_date', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'birth_date' in self.fields:
            self.fields['birth_date'].widget.attrs['max'] = date.today().isoformat()

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if not birth_date:
            return birth_date

        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        if age < 16:
            # استخدم forms.ValidationError لضمان التوافق
            raise forms.ValidationError("يجب أن يكون عمرك 16 عاماً على الأقل للتسجيل.")

        if age > 100:
            raise forms.ValidationError("الرجاء إدخال تاريخ ميلاد منطقي.")

        return birth_date

    def save(self, request):
        # 1. إنشاء المستخدم الأساسي عبر الكلاس الأب
        user = super().save(request)

        # 2. ربط الـ Role (كما فعلت أنت)
        role = Role.objects.filter(code=self.role_code).first()
        if role:
            user.identity = role
        user.save()

        # 3. إنشاء البروفايل مع تمرير كائن الـ user (هنا حل المشكلة)
        profile = MemberProfile.objects.create(
            user=user,  # <--- هذا السطر هو المفتاح لحل IntegrityError
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            birth_date=self.cleaned_data.get('birth_date'),
        )

        # 4. ربط الـ Generic Foreign Key (إذا كنت تستخدمه للبروفايلات المختلفة)
        user.profile_type = ContentType.objects.get_for_model(profile)
        user.profile_id = profile.id
        user.save()

        return user



class CompanySignupForm(BaseAccountSignupForm):
    role_code = "company"

    name = forms.CharField(max_length=150, label=_('Company Name'),
                           widget=forms.TextInput(attrs={'placeholder': _('Enter company name')}))
    bio = forms.CharField(
        label=_('About the Company'),
        widget=forms.Textarea(attrs={'placeholder': _('Brief description of your company...'),
                                     'rows': 3}),
        required=False
    )
    location = forms.CharField(
        max_length=100,
        label=_('Location'),
        widget=forms.TextInput(attrs={'placeholder':f"{ _('City')} , {_('Country')}"})
    )


    field_order = ['name', 'location', 'bio', 'email', 'password1', 'password2']

    class Meta:
        model = CustomUser
        # widgets = {
        #     'email': forms.DateInput(attrs={'type': 'email'}),
        # }

    def save(self, request):
        # القيمة تم توليدها وتجهيزها مسبقاً في دالة clean الشاملة
        user = super().save(request)
        user.name = self.cleaned_data.get('name')
        user.identity = Role.objects.filter(code=self.role_code).first()
        user.save()

        CompanyProfile.objects.create(
            user=user,
            name=self.cleaned_data.get('name'),
            location=self.cleaned_data.get('location'),
            bio=self.cleaned_data.get('bio')
        )
        return user

    # def save(self, request):
    #     self.cleaned_data['username'] = self.clean_username()
    #     user = super().save(request)
    #     user.name = self.cleaned_data.get('name')
    #     user.identity = Role.objects.filter(code=self.role_code).first()
    #     user.save()
    #
    #     CompanyProfile.objects.create(
    #         user=user,
    #         name=self.cleaned_data.get('name'),
    #         location=self.cleaned_data.get('location'),
    #         # registration_number=self.cleaned_data.get('registration_number'),
    #         bio=self.cleaned_data.get('bio')
    #     )
    #     return user




# 2. الكلاس الموحد والنهائي (استخدم هذا الاسم فقط)
# class CustomSignupForm(SignupForm, BaseStyledForm):
#
#     identity = forms.ModelChoiceField(
#         queryset=Role.objects.filter(view_in_register=True, is_identity=True),
#         label="Account Type",
#         empty_label="--- Select account type ---",
#         required=True
#     )
#
#     def __init__(self, *args, **kwargs):
#         # تشغيل الـ init الخاص بـ Allauth
#         super(CustomSignupForm, self).__init__(*args, **kwargs)
#         if 'username' in self.fields:
#             self.fields['username'].widget = forms.HiddenInput()
#             self.fields['username'].required = False
#         # تطبيق تنسيق Tailwind على كل الحقول (بما فيها الباسورد والايميل)
#         self.apply_tailwind_styles()
#
#     def save(self, request):
#         email=self.cleaned_data.get('email')
#         self.cleaned_data['username']=email
#         # حفظ المستخدم عبر Allauth أولاً
#         user = super(CustomSignupForm, self).save(request)
#
#         # حفظ الحقول الإضافية في موديل CustomUser
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         user.identity = self.cleaned_data['identity']
#
#         user.save()
#         return user


#
# # --- 2. نموذج تعديل البيانات الأساسية (User Model) ---
# class UserUpdateForm(BaseStyledForm):
#     class Meta:
#         model = CustomUser
#         # أضفنا الجوال وتاريخ الميلاد هنا لأنك وضعتهما في BaseCustomUser
#         fields = ('first_name', 'last_name', 'username','email', 'phone_number', 'birth_date')
#         widgets = {
#             'birth_date': forms.DateInput(attrs={'type': 'date'}),
#         }
#
# # --- 3. نموذج تعديل الملف الشخصي (Profile Model) ---
# class ProfileUpdateForm(BaseStyledForm):
#     class Meta:
#         model = Profile  # التغيير الجذري هنا: نربطه بموديل Profile
#         fields = ('picture', 'bio') # لاحظ الفاصلة بعد العنصر الأخير إذا كان واحداً
#         widgets = {
#             'bio': forms.Textarea(attrs={'rows': 3}),
#         }
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if 'bio' in self.fields:
#             self.fields['bio'].widget.attrs.update({'class': self.tailwind_fields_classes + ' w-full resize-none'})
