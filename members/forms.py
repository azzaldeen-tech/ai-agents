from datetime import date

from django import forms

from core.forms import BaseModelForm
from django.utils.translation import gettext_lazy as _

from members.models import MemberProfile


class MemberProfileForm(BaseModelForm):


    class Meta:
        model= MemberProfile

        fields=('first_name', 'last_name','skills', 'birth_date', 'avater')

        labels = {
            'first_name': ' الاسم الاول',
            'last_name': ' الاسم الاخير',
            'skills': ' المهارات',
            'birth_date': ' تأريخ الميلاد',
            'avater': 'الصورة الشخصية',
        }
        # exclude = ['is_available']

        widgets = {
            'birth_date': forms.DateInput(attrs={'class': 'bg-white','type': 'date'}),
            # 'last_name': forms.NumberInput(attrs={'class': 'max-w-md'}),
            # 'graduation_year': forms.NumberInput(attrs={'placeholder': '2025'}),
            # 'gpa': forms.NumberInput(attrs={'step': '0.01', 'placeholder': '4.00'}),
            # 'skills': forms.SelectMultiple(attrs={'class': 'select2-enable '}),  # إذا كنت تستخدم مكتبة Select2
        }


        error_messages = {

            'avater': {
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




    def clean_avater(self):
        picture = self.cleaned_data.get('avater')
        if picture:
            # 1. التحقق من الحجم (مثلاً: حد أقصى 1 ميجابايت)
            if picture.size > 1 * 1024 * 1024:
                raise forms.ValidationError(
                    self.fields['avater'].error_messages['image_too_large'],
                    code='image_too_large'
                )

            # 2. التحقق من الامتداد (اختياري لأن ImageField يفعل ذلك جزئياً)
            extension = picture.name.split('.')[-1].lower()
            if extension not in ['jpg', 'jpeg', 'png']:
                raise forms.ValidationError(
                    self.fields['avater'].error_messages['invalid_image_format'],
                    code='invalid_image_format' )
        return picture

    def clean_birth_date(self):
        """التحقق من صحة تاريخ الميلاد"""
        birth_date = self.cleaned_data.get('birth_date')
        today = date.today()

        if birth_date:
            # 1. منع التواريخ المستقبلية
            if birth_date > today:
                raise forms.ValidationError(
                    _("تاريخ الميلاد لا يمكن أن يكون في المستقبل."),
                    code='future_date'
                )

            # 2. التحقق من الحد الأدنى للعمر (مثلاً 15 سنة)
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            if age < 15:
                raise forms.ValidationError(
                    _("عذراً، يجب أن يكون عمرك 15 عاماً على الأقل للتسجيل في المنصة."),
                    code='too_young'
                )

            # 3. منع التواريخ القديمة جداً (غير المنطقية)
            if birth_date.year < 1920:
                raise forms.ValidationError(
                    _("يرجى إدخال تاريخ ميلاد صحيح."),
                    code='invalid_year'
                )

        return birth_date