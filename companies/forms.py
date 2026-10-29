from datetime import date
from accounts.forms import BaseStyledForm
from core.forms import BaseModelForm
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import Job, CompanyProfile
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


class CompanyProfileForm(BaseModelForm):


    class Meta:
        model= CompanyProfile

        fields=('name', 'bio','location', 'website', 'logo')

        labels = {
            'name': 'الاسم',
            'bio': 'النبذة',
            'location': ' الموقع',
            'website': 'رابط الموقع',
            'logo': 'الصورة الشخصية',
        }
        # exclude = ['is_available']


        error_messages = {

            'logo': {
                'image_too_large': _("Image file too large (Max 1MB)"),
                'invalid_image_format': _("Unsupported file extension. Use JPG or PNG."),
            }

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # if self.instance and self.instance.pk:
            # --- منطق التخصصات (كودك الحالي) ---
        #     selected_major = self.instance.major
        #     if selected_major:
        #         college = selected_major.college
        #         university = college.university
        #         self.initial['university'] = university
        #         self.initial['college'] = college
        #         self.initial['major'] = selected_major
        #         self.fields['college'].queryset = College.objects.filter(university=university)
        #         self.fields['major'].queryset = Major.objects.filter(college=college)
        #         self.fields['college'].widget.attrs.pop('disabled', None)
        #
        #
        # # إجبار المستخدم على اختيار التخصص في الواجهة
        # self.fields['major'].required = True
        # self.fields['major'].empty_label = _("Choose your academic major")

        # for field_name, field in self.fields.items():
        #     # 1. الحفاظ على أي كلاسات تمت إضافتها يدوياً في الـ widgets
        #     existing = field.widget.attrs.get('class', '')
        #     # 3. دمج الكلاسات وتحديث الحقل
        #     if field_name!='skills':
        #         field.widget.attrs['class'] = f"{existing}   ".strip()


    def clean_logo(self):
        picture = self.cleaned_data.get('logo')
        if picture:
            # 1. التحقق من الحجم (مثلاً: حد أقصى 1 ميجابايت)
            if picture.size > 1 * 1024 * 1024:
                raise forms.ValidationError(
                    self.fields['logo'].error_messages['image_too_large'],
                    code='image_too_large'
                )

            # 2. التحقق من الامتداد (اختياري لأن ImageField يفعل ذلك جزئياً)
            extension = picture.name.split('.')[-1].lower()
            if extension not in ['jpg', 'jpeg', 'png']:
                raise forms.ValidationError(
                    self.fields['logo'].error_messages['invalid_image_format'],
                    code='invalid_image_format' )
        return picture



    def clean_website(self):
        url = self.cleaned_data.get('website')
        if url:
            validate = URLValidator()
            try:
                validate(url)
            except ValidationError:
                raise forms.ValidationError("Please enter a valid web address (example: https://example.com)")

        return url


class JobForm(BaseModelForm):
    class Meta:
        model = Job
        # نحدد الحقول التي نريد للشركة تعبئتها (استبعدنا الحقول التلقائية مثل created_at)
        fields = [
            'category',
            'title',
            'description',
            'required_skills',
            'city',
            'employment_type',
            'experience_level',
            'min_salary',
            'max_salary',
            'deadline',
            'requirements',
            # 'company',
        ]


        labels = {
            'category': 'مجال الوظيفة',
            'title': 'المسمى الوظيفي',
            'description': 'وصف الوظيفة',
            'requirements': 'المتطلبات الإضافية',
            'required_skills': 'المهارات المطلوبة',
            'city': 'المدينة',
            'location': 'موقع الوظيفة',
            'employment_type': 'نوع الدوام',
            'experience_level': 'مستوى الخبرة',
            'min_salary': 'الحد الأدنى للراتب',
            'max_salary': 'الحد الأعلى للراتب',
            'deadline': 'موعد انتهاء التقديم',
        }
        # إضافة Widgets لتنسيق الحقول ومنحها كلاسات CSS
        widgets = {
            'title': forms.TextInput( attrs={'class': 'input input-bordered ', 'placeholder':'ادخل المسمى الوظيفي'}),
            'category': forms.Select(attrs={'class': 'select select-bordered ','placeholder':'أختر التخصص'}),
            'description': forms.Textarea(attrs={'class': 'textarea textarea-bordered ', 'rows': 2, 'placeholder':'ادخل الوصف الوظيفي'}),
            'requirements': forms.Textarea(attrs={'class': 'textarea textarea-bordered ', 'rows': 2, 'placeholder':'ادخل المطلبات  الإضافية (إختياري)'}),
            # 'required_skills': forms.SelectMultiple(attrs={'class': 'select2-skills w-full',  'multiple': 'multiple'}),
            'location': forms.TextInput(attrs={
                'class': 'input ',
                'placeholder': 'ادخل موقع الوظيفة'
            }),
            'employment_type': forms.Select(attrs={
                'class': 'select ',
            }),
            'experience_level': forms.Select(attrs={
                'class': 'select',
            }),
            'min_salary': forms.NumberInput(attrs={
                'class': 'input ',
                'placeholder': 'الحد الأدنى'
            }),
            'max_salary': forms.NumberInput(attrs={
                'class': 'input ',
                'placeholder': 'الحد الأعلى'
            }),
            'deadline': forms.DateInput(attrs={'class': 'input input-bordered w-full', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #
        # if 'company' in self.fields:
        #     self.fields['company'].widget = forms.HiddenInput()
        #     self.fields['company'].required = False

        for field_name, field in self.fields.items():
            existing = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f"{existing}   w-full  rounded-xl py-2.5 px-4 text-[13px]  focus:border-brand/40 transition-color".strip()



    def clean(self):
        cleaned_data = super().clean()
        min_salary = cleaned_data.get("min_salary")
        max_salary = cleaned_data.get("max_salary")

        if min_salary and max_salary and min_salary > max_salary:
            raise forms.ValidationError("يجب أن يكون الحد الأدنى للراتب أقل من الحد الأعلى.")
        return cleaned_data