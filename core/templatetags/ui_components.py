from django import template
import json
from django.utils.translation import gettext_lazy as _

from core.app_links import AppLinks
from core.helpers import get_url_view

register = template.Library()


""" takes_context=True:
للسماح للمكون بالوصول إلى سياق الصفحة (Context)،
مما يتيح التحقق من حالة المستخدم (Logged-in)، الصلاحيات (Permissions)،
  أو بيانات الطلب (Request) دون تمريرها يدوياً.
"""

@register.inclusion_tag('core/components/ui_multi_tag_select.html')
def ui_multi_tag_select(name, label=None, choices=None, placeholder=None, selected_values=None):

    print(selected_values)
    return {
        'name': name,
        'label': label,
        'choices': choices or [],
        'placeholder': placeholder or "ابحث واختر...",
        'selected_values': selected_values or [], # للقيم المختارة مسبقاً في التعديل
    }


@register.inclusion_tag('core/components/back-button.html', takes_context=True)
def back_button(context,label=None, url=None, extra_classes="",icon=None):
    _url=""
    if url:
        _url=get_url_view(url)

    return {
        'label': label or _("Back"),
        'url': _url or 'javascript:history.back()',
        'extra_classes': extra_classes ,
        # 'icon': icon,
        # 'content_color': content_color,
        # 'bg_color': bg_color,
        'LANGUAGE_BIDI': context.get('LANGUAGE_BIDI'),
    }

@register.inclusion_tag('core/components/profile_dropdown.html')
def profile_dropdown(img_url=None, display_name="", initials=None, sub_text="",profile_url="", settings_url="#", support_url="#", logout_url=None):
    _initials=""
    if not initials and display_name and not img_url and len(display_name)>=1:
        _initials = "".join([n for n in display_name[:1]]).upper()

    return {
        'img_url': img_url,
        'display_name': display_name,
        'initials': initials or _initials,
        'sub_text': sub_text,
        'profile_url': profile_url,
        'settings_url': settings_url,
        'support_url': support_url,
        'logout_url': logout_url or AppLinks.Auth.LOGOUT,
    }


@register.inclusion_tag('core/components/user-card.html')
def user_card(name, email,user_id=None, image_url=None,redirect_link=None):
    default_img = "/static/images/default-avatar.png" # رابط افتراضي من تطبيق theme
    return {
        'name': name,
        'email': email,
        'image': image_url if image_url else default_img,
        'id': user_id or '000',
        'redirect_link': redirect_link or '',
    }



@register.inclusion_tag('core/components/statistics-card.html')
def statistics_card(title, amount=0, icon=None, badge_amount=None, badge_text=None, badge_icon=None, badge_type='brand', delay='0s', redirect_link=None):
    # خريطة الألوان بناءً على ملف الـ CSS المدمج
    color_map = {
        'brand': {
            'icon_bg': 'bg-brand-light',
            'icon_text': 'text-brand',
            'badge': 'bg-brand-light text-brand'
        },
        'amber': {
            'icon_bg': 'bg-amber-light',
            'icon_text': 'text-amber',
            'badge': 'bg-amber-light text-amber'
        },
        'coral': {
            'icon_bg': 'bg-coral-light',
            'icon_text': 'text-coral',
            'badge': 'bg-coral-light text-coral'
        }
    }

    # اختيار التنسيق أو العودة للافتراضي (brand)
    style = color_map.get(badge_type, color_map['brand'])

    return {
        'title': title,
        'amount': amount,
        'icon': icon or 'fa-chart-line',
        'badge_amount': badge_amount,
        'badge_text': badge_text,
        'badge_icon': badge_icon,
        'delay': delay,
        'redirect_link': redirect_link,
        # تمرير الكلاسات الجاهزة للقالب
        'icon_bg': style['icon_bg'],
        'icon_text': style['icon_text'],
        'badge_class': style['badge'],
    }


@register.inclusion_tag('core/components/weekly-data-chart.html')
def weekly_data_chart(title,data_dict):

    return {
        'title': title,
        'weekly_data_json': data_dict
    }
@register.inclusion_tag('core/components/candidate-row.html')
def candidate_row(candidate, is_last=False,redirect_link=None):
    return {
        'c': candidate,
        'is_last': is_last,
        'redirect_link': redirect_link,
    }

@register.inclusion_tag('core/components/tag-card.html')
def tag_card(label):
    return {
        'label': label,
    }

@register.inclusion_tag('core/components/job_applicant_detail.html')
def job_applicant_detail(job_app):
    return {
        'job_app': job_app,
        # 'redirect_link': redirect_link,
    }
@register.inclusion_tag('core/components/link-button.html',name='link-button', takes_context=True)
def link_button(context,url,label="",title="",icon=None,extra_classes=None):

    return {
        'url': url,
        'label': label,
        'title': title,
        'icon': icon ,
        'extra_classes': extra_classes ,
        'LANGUAGE_BIDI': context.get('LANGUAGE_BIDI'),
    }


@register.inclusion_tag('core/components/delete-button.html', takes_context=True)
def delete_button(context, action_url, label=None, message=None, extra_classes=""):
    return {
        'url': action_url,
        'label': label or '',
        'message': message or _("هل أنت متأكد من رغبتك في حذف هذا العنصر؟"),
        'extra_classes': extra_classes,
        'LANGUAGE_BIDI': context.get('LANGUAGE_BIDI', False), # مهم لترتيب الأزرار
    }

@register.inclusion_tag('core/components/show-messages.html', takes_context=True)
def show_messages(context, messages=[]):
    return {
        'messages': messages,
    }



@register.inclusion_tag('core/components/job-card.html')
def job_card(job, redirect_link=None,is_manager=False):
    # حساب نسبة التحويل مع التأكد من عدم القسمة على صفر
    conversion_rate = 0
    # if job.get('views', 0) > 0:
    #     conversion_rate = (job.get('apps', 0) / job.get('views')) * 100

    # تحديد ما إذا كانت الوظيفة نشطة (بناءً على حالة معينة)
    # is_active = job.get('status') == 'نشط' or job.get('status') == 'Active'

    return {
        'j': job,
        'redirect_link': redirect_link,
        'conversion_rate': round(conversion_rate, 1),
        'is_active': job.is_active,
        'is_manager': is_manager,
    }

@register.inclusion_tag('core/components/job_search_item.html')
def job_search_item(job, redirect_link=None,is_manager=False):

    conversion_rate = 0

    return {
        'j': job,
        'redirect_link': redirect_link,
        'conversion_rate': round(conversion_rate, 1),
        'is_active': job.is_active,
        'is_manager': is_manager,
    }
# @register.inclusion_tag('core/components/job-post-card.html')
# def job_card(job, redirect_link=None):
#     # حساب نسبة التحويل مع التأكد من عدم القسمة على صفر
#     conversion_rate = 0
#     if job.get('views', 0) > 0:
#         conversion_rate = (job.get('apps', 0) / job.get('views')) * 100
#
#     # تحديد ما إذا كانت الوظيفة نشطة (بناءً على حالة معينة)
#     is_active = job.get('status') == 'نشط' or job.get('status') == 'Active'
#
#     return {
#         'j': job,
#         'redirect_link': redirect_link,
#         'conversion_rate': round(conversion_rate, 1),
#         'is_active': is_active
#     }


@register.inclusion_tag('core/components/interview-card.html')
def interview_card(iv, is_last=False):
    # خريطة الألوان بناءً على نوع المقابلة
    color_map = {
        'sky': 'bg-sky-light text-sky',
        'brand': 'bg-brand-light text-brand',
        'amber': 'bg-amber-light text-amber',
    }

    return {
        'iv': iv,
        'color_class': color_map.get(iv.get('typeColor'), 'bg-raised text-fg-muted'),
        'is_last': is_last
    }
@register.inclusion_tag('core/components/funnel-step.html')
def funnel_step(label, count, percentage, index=0):
    # مصفوفة الألوان مرتبة حسب مراحل القمع
    palette = [
        '#0d7c5f',  # Brand / Emerald
        '#2a8fc7',  # Sky Blue
        '#c48a0a',  # Amber
        '#e06040',  # Coral
        '#7c5cbf',  # Purple
        '#0d7c5f',  # التعيين (عودة للون البراند)
    ]

    # اختيار اللون بناءً على رقم الخطوة (Index)
    # إذا تجاوزت الخطوات عدد الألوان، سيعود للون الأول باستخدام %
    selected_color = palette[index % len(palette)]

    return {
        'label': label,
        'count': count,
        'percentage': percentage+10,
        'color': selected_color,
    }

@register.inclusion_tag('core/components/plan-card.html', takes_context=True)
def plan_card(context, title, price, features=[], is_popular=False, button_text="Subscribe"):
    return {
        'title': title,
        'price': price,
        'features': features, # مصفوفة من المميزات
        'is_popular': is_popular,
        'button_text': button_text,
        'LANGUAGE_BIDI': context.get('LANGUAGE_BIDI'),
    }
@register.inclusion_tag('core/components/submit-button.html',name='submit-button', takes_context=True)
def submit_button(context,label, content_color=None,icon=None,bg_color=None):

    return {
        'label': label,
        'icon': icon ,
        'content_color': content_color ,
        'bg_color': bg_color ,
        'LANGUAGE_BIDI': context.get('LANGUAGE_BIDI'),
    }


@register.inclusion_tag('core/components/input-text.html',name='input-text', takes_context=True)
def input_text(context, label, name, type='text', id=None, value=None, error=None,
               content_color='text-content', icon=None, bg_color='bg-field-base',
               placeholder='', help_text=None,required=False):


    """
    مكون إدخال نصي احترافي يدعم الثيمات التلقائية (Dark/Light) عبر Tailwind 4.
    """
    formatted_error = None
    if error:
        if isinstance(error, (list, tuple)):
            formatted_error = error[0]  # نأخذ أول رسالة خطأ فقط لجمالية التصميم
        else:
            formatted_error = str(error)

    return {
        'label': label,
        'type': type,
        'name': name,
        'id': id if id else f"id_{name}",  # توليد ID تلقائي في حال عدم وجوده لضمان ربط الـ Label
        'value': value if value else '',
        'error': formatted_error,
        'icon': icon,
        'placeholder': placeholder,
        'help_text': help_text,
        'required': required,
        # ألوان تعتمد على متغيراتك الثابتة
        'bg_color': bg_color,
        'content_color': content_color,
        'request': context.get('request'), # لتمرير السياق إذا احتجت له مستقبلاً
    }



@register.inclusion_tag('core/components/input-checkbox.html', name='input-checkbox')
def input_checkbox(label, name, checked=False, required=False, id=None, error=None):
    return {
        'label': label,
        'name': name,
        'checked': checked,
        'required': required,
        'id': id if id else f"id_{name}",
        'error': error,
    }