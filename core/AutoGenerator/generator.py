import os
from django.conf import settings
from django.core.management import call_command
class AutoGenerator:
    """
    A professional automation tool for Django to generate
    standardized application structures with zero manual boilerplate.
    """

    def __init__(self):
        # Professional CLI Colors
        self.SUCCESS = '\033[92m'
        self.WARNING = '\033[93m'
        self.INFO = '\033[96m'
        self.BOLD = '\033[1m'
        self.RESET = '\033[0m'
        self.BORDER = f"{self.INFO}{'=' * 70}{self.RESET}"

    def generate(self, app_name):
        """The main execution thread for generating an app."""
        app_name = app_name.lower().strip()

        print(f"\n{self.INFO}🔧 Initializing AutoGenerator for: {self.BOLD}{app_name}{self.RESET}...")

        # 1. Start App
        if not self._create_django_app(app_name):
            return

        # 2. Build Internal Logic
        self._build_templates(app_name)
        self._build_urls(app_name)
        self._build_views(app_name)
        # 3. Register Routing
        routing_status = self._register_urls(app_name)
        # 4. Final Report
        self._print_report(app_name, routing_status)

    def _create_django_app(self, app_name):
        app_path = os.path.join(settings.BASE_DIR, app_name)
        if os.path.exists(app_path):
            print(f"{self.WARNING}⚠️  Skip: Directory '{app_name}' already exists.{self.RESET}")
            return True
        try:
            call_command('startapp', app_name)
            return True
        except Exception as e:
            print(f"\033[91m❌ Error creating app: {e}{self.RESET}")
            return False

    def _build_templates(self, app_name):
        path = os.path.join(settings.BASE_DIR, app_name, 'templates', app_name)
        os.makedirs(path, exist_ok=True)
        file_path = os.path.join(path, 'dashboard.html')

        content = (
            "{% extends 'core/base.html' %}\n"
            "{% block content %}\n"
            "<div class='p-8 bg-white shadow rounded-lg'>\n"
            f"    <h1 class='text-3xl font-bold text-indigo-600'>{app_name.capitalize()} Dashboard</h1>\n"
            "    <p class='text-gray-500 mt-2'>Automated interface for Labor-Market-Trend-Anyalysis Platform.</p>\n"
            "</div>\n"
            "{% endblock %}"
        )
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def _build_views(self, app_name):
        path = os.path.join(settings.BASE_DIR, app_name, 'views.py')
        content = (
            "from django.shortcuts import render\n\n"
            f"app_name = '{app_name}'\n\n"
            "def dashboard_view(request):\n"
            f"    return render(request, '{app_name}/dashboard.html')\n"
        )
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

    def _build_urls(self, app_name):
        path = os.path.join(settings.BASE_DIR, app_name, 'urls.py')
        content = (
            "from django.urls import path\n"
            "from . import views\n\n"
            f"app_name = '{app_name}'\n\n"
            "urlpatterns = [\n"
            "    path('dashboard/', views.dashboard_view, name='dashboard'),\n"
            "]\n"
        )
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

    def _register_urls(self, app_name):
        urls_path = os.path.join(settings.BASE_DIR, 'config', 'urls.py')
        marker = "# === [AUTO_GENERATED_URLS_END] ==="

        with open(urls_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if any(f"'{app_name}.urls'" in line for line in lines):
            return "ALREADY_REGISTERED"

        new_lines = []
        found = False
        for line in lines:
            if marker in line:
                new_lines.append(f"    path('{app_name}/', include('{app_name}.urls')),\n")
                found = True
            new_lines.append(line)

        if found:
            with open(urls_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            return "SUCCESS"
        return "MARKER_NOT_FOUND"

    def _print_report(self, app_name, routing_status):
        print(f"\n{self.BORDER}")
        print(f"{self.SUCCESS}{self.BOLD}🚀 GENERATION COMPLETE!{self.RESET}")
        print(f"{self.BORDER}\n")

        print(f"{self.INFO}{self.BOLD}Module:{self.RESET} {app_name}")
        print(f"{self.INFO}{self.BOLD}URL Status:{self.RESET} {routing_status}")

        print(f"\n{self.WARNING}{self.BOLD}⚠️  REQUIRED ACTION:{self.RESET}")
        print(f"To finalize, update {self.BOLD}config/settings.py{self.RESET}:")
        print(f"   {self.SUCCESS}INSTALLED_APPS = [{self.RESET}")
        print(f"   {self.SUCCESS}    ...{self.RESET}")
        print(f"   {self.SUCCESS}    '{app_name}',{self.RESET}")
        print(f"   {self.SUCCESS}]{self.RESET}")

        print(f"\n{self.BORDER}")