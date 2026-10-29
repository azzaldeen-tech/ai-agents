from django.shortcuts import render
from django.contrib.auth import login

from core.app_links import AppLinks
from .forms import  CompanySignupForm, MemberSignupForm

from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .models import Role


@login_required
def redirect_by_role(request):

    dashboards = getattr(settings, 'ROLE_DASHBOARDS', {})
    default_home = getattr(settings, 'DEFAULT_HOME_URL', '/')

    identity = getattr(request.user, 'identity', None)
    # 3. الحصول على كود الدور
    role_code = getattr(identity, 'code', None) if identity else None

    # 4. محاولة التوجيه بناءً على الدور
    target_url = dashboards.get(role_code)
    # # TODO: The right moveit to method running when system start build
    # app_name=get_identity_app_name(role_code)
    # if app_name and not app_is_exists(app_name):
    #     gen = AppGenerator()
    #     gen.generate(app_name)

    print(f"DEBUG: User Role Code: {role_code} -> Target URL: {target_url}")

    return redirect(target_url if target_url else default_home)

def error_404(request, exception):
    return render(request, '404.html', status=404)

def error_500(request):
    return render(request, '500.html', status=500)

def select_account_type(request):

    identity_roles=[]
    if request.method == 'GET':
        identity_roles = Role.objects.filter(view_in_register=True, is_identity=True)

    return render(request, 'account/select_account_type.html', {'identity_roles': identity_roles})

# def signup(request):
#     if request.method == 'POST':
#         # هنا نستقبل البيانات المدخلة والوسائط من واجهة المستخدم
#         form = CustomSignupForm(request.POST, request.FILES)
#         #يتأكد من أن البريد الإلكتروني صحيح، كلمة المرور مطابقة للشروط، وأن المستخدم غير موجود مسبقاً.
#         if form.is_valid():
#             user = form.save() # تحويل كائن البيانات المدخلة الى استعلام قابل لتنفيذ في قاعدة البيانات
#             login(request, user) # تسجيل دخول تلقائي بعد التسجيل
#             return redirect('core:home') # الانتقال لصفحة الرئيسية
#     else:
#         form = CustomSignupForm()
#     return render(request, 'account/signup.html', {'form': form})


def signup_company(request):
    if request.method == 'POST':
        form = CompanySignupForm(request.POST, request.FILES)
        print("Register::")
        if form.is_valid():
            print("Register2::")
            user = form.save(request)
            login(request, user)
            return redirect(AppLinks.Dashboards.COMPANY)
    else:
        form = CompanySignupForm()
    return render(request, 'account/signup.html', {'form': form})


def signup_member(request):
    if request.method == 'POST':
        form = MemberSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(request)
            login(request, user)
            return redirect(AppLinks.Dashboards.MEMBER)
    else:
        form = MemberSignupForm()
    return render(request, 'account/signup.html', {'form': form})

# دالة تسجيل حساب وضيفتها:
# التحقق من نوع دالة الارسال  post | get  او غيرها
# إلتقاط البيانات من الطلب والمدخله في النموذج من قبل المستخدم
# def register(request):
#     if request.method == 'POST':
#         # هنا نستقبل البيانات المدخلة والوسائط من واجهة المستخدم
#         form = CustomSignupForm(request.POST, request.FILES)
#         #يتأكد من أن البريد الإلكتروني صحيح، كلمة المرور مطابقة للشروط، وأن المستخدم غير موجود مسبقاً.
#         if form.is_valid():
#             user = form.save() # تحويل كائن البيانات المدخلة الى استعلام قابل لتنفيذ في قاعدة البيانات
#             login(request, user) # تسجيل دخول تلقائي بعد التسجيل
#             return redirect('core:home') # الانتقال لصفحة الرئيسية
#     else:
#         form = CustomSignupForm()
#     return render(request, 'account/register.html', {'form': form})



# def search_users(request):
#     query = request.GET.get('search', '')
#     if query:
#         users = CustomUser.objects.filter(username__icontains=query)
#     else:
#         users = []
#
#     # نرسل ملف HTML صغير جداً يحتوي فقط على القائمة
#     return render(request, 'core/home.html', {'users': users})
#
