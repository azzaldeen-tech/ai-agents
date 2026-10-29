<div align="center">

# 📊 Job Market Trend Analysis System

**A Django-powered analytics platform that transforms raw job-market data into actionable labor-market intelligence.**

*Visualize trends · Track in-demand skills · Forecast career paths*

<img src="static/img/solider.png" alt="Labor Market Analytics Home" width="800"/>

*Labor Market Analytics*
<img src="static/img/img2.png" alt="Labor Market Analytics " width="800"/>

</div>

![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-v4-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)
![daisyUI](https://img.shields.io/badge/daisyUI-5-5C016E?style=for-the-badge&logo=daisyui&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Chart.js](https://img.shields.io/badge/Chart.js-4.x-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)
![HTMX](https://img.shields.io/badge/AJAX-HTMX-34D0B1?style=for-the-badge&logo=htmx&logoColor=white)

---

## 🎯 Overview

The **Job Market Trend Analysis System** is a full-stack web platform built on Django's **MVT (Model–View–Template)** pattern with a **modular app architecture**. It aggregates and analyzes job postings across companies, sectors, cities, and experience levels — then turns that data into live, interactive intelligence.

### The Problem It Solves

Job seekers, students, and career planners make decisions blind: *Which skills are actually in demand? Which sector pays best? Where is the market heading in the next quarter?* Meanwhile, employers lack visibility into hiring funnels and market benchmarks.

This system closes that gap by providing:

| Audience | Value Delivered |
|---|---|
| 🧑‍💻 **Members / Students** | Explore live jobs, discover trending skills, view predictive career-path analytics |
| 🏢 **Companies** | Post jobs, manage applicants through a hiring funnel, benchmark salaries by category |
| 🛡️ **Admins** | Approve companies, govern accounts, oversee platform-wide statistics |

---

## ✨ Key Features

### 📈 Graphical Labor-Market Visualization
Interactive **Chart.js** dashboards rendering jobs-over-time timelines, top-skill rankings, salary-by-category comparisons, experience-level distributions, and sector breakdowns — all fed by optimized Django ORM aggregation pipelines.

### 🔮 Skills-Demand Prediction Algorithms
A dedicated statistical engine (`core/Utils`) powered by **pandas / NumPy / SciPy / statsmodels**:
- **ARIMA time-series forecasting** (`ai_statistical_analysis.py`) projects job demand for the next three months.
- Trending-skills scoring, monthly aggregation via `TruncMonth`, and weighted category analytics.

### 🛡️ Role-Based Access Control (RBAC)
Precise, decorator-driven authorization built on a custom `CustomUser` model:
- `@member_required` → guards the talent side (`members/decorators.py`)
- `@company_required` → guards the employer side (`companies/decorators.py`)
- `ApprovalCompanyMiddleware` → blocks unapproved companies until admin review
- Centralized route registry (`core/app_links.py`) for safe, consistent redirects

### 🎛️ Advanced Dynamic Filters
Composable query-builder (`build_job_filters`) driving HTMX-powered partial re-rendering — filter jobs by skill, category, city, experience level, and salary range **without a single page reload**.

### ⚙️ Engineering Extras
- 🌍 Bilingual UI (Arabic/English) via `django-modeltranslation` + `locale/ar`
- 🎨 Custom **Tailwind CSS v4 + daisyUI** theme app with a component library of reusable template tags
- 🤖 `AutoGenerator` CLI that scaffolds standardized new Django apps with zero boilerplate
- 🌱 Deterministic database seeders (`Seeds/`) for accounts, companies, jobs, regions, and skills

---

## 🏗️ Application Architecture & Folder Structure

### MVT + Modular App Architecture

The project follows Django's **MVT** pattern, elevated by a **separation-of-concerns discipline** inside every app:

```
┌─────────────────────────────────────────────────────────────────┐
│                        config (Project)                         │
│         settings.py · urls.py · WSGI/ASGI · management          │
└──────────────┬───────────────────────────────────────────────────┘
               │
   ┌───────────┼────────────┬──────────────┬──────────────┐
   ▼           ▼            ▼              ▼              ▼
┌───────┐ ┌─────────┐ ┌───────────┐ ┌─────────┐ ┌───────────┐
│ core  │ │accounts │ │ companies │ │ members │ │   theme   │
│ (hub) │ │ (auth)  │ │(employer) │ │(talent) │ │(tailwind) │
└───┬───┘ └─────────┘ └─────┬─────┘ └────┬────┘ └───────────┘
    │                       │            │
    ▼                       ▼            ▼
 Utils/                decorators.py  decorators.py
 ├ statistical_analysis     @company_required @member_required
 ├ ai_statistical_analysis
 └ services layer
```

**Concern separation per module:**

| Module | Responsibility |
|---|---|
| `decorators.py` | Declarative RBAC view guards (`@member_required`, `@company_required`) |
| `Utils/services.py` | Business logic isolated from views — thin views, testable services |
| `app_links.py` | Single source of truth for named routes & redirects |
| `context_processors.py` | Per-app global template context injection |
| `middleware.py` | Cross-cutting policies (e.g., company approval gating) |
| `templatetags/` | Reusable UI component tags (cards, buttons, charts) |

### Folder Tree

```text
Labor-Market-Trends-Analysis-Platform/
├── config/                          # ⚙️ Project configuration
│   ├── settings.py                  #    Settings (allauth, crispy, tailwind, i18n)
│   ├── urls.py                      #    Root URL router
│   └── management/
│       └── commands/
│           └── generate_apps.py     #    App scaffolding command
│
├── core/                            # 🧠 Central hub — shared logic & analytics engine
│   ├── Utils/
│   │   ├── statistical_analysis.py  #    ORM aggregations: KPIs, filters, timelines
│   │   ├── ai_statistical_analysis.py #  ARIMA forecasting (statsmodels)
│   │   ├── JobServices.py           #    Job-domain service layer
│   │   ├── services.py              #    Shared service utilities
│   │   └── AutoGenerator/
│   │       └── generator.py         #    Automated app scaffolder
│   ├── templatetags/
│   │   └── ui_components.py         #    Reusable UI template tags
│   ├── middleware.py                #    ApprovalCompanyMiddleware
│   ├── context_processors.py        #    Global context injection
│   ├── app_links.py                 #    Centralized route registry
│   └── templates/core/
│       ├── base.html                #    Master layout (Chart.js + HTMX)
│       ├── dashboard.html           #    Admin dashboard
│       ├── labor_market_trends.html #    Trends visualization suite
│       ├── predictive_analytics.html#    Forecasting dashboards
│       ├── jobs_explore.html        #    Public job explorer
│       ├── components/              #    20+ reusable UI components
│       └── partials/                #    HTMX partial responses
│
├── accounts/                        # 🔐 Identity & authentication
│   ├── models.py                    #    CustomUser (role flags)
│   ├── signals.py                   #    Profile auto-creation hooks
│   └── templates/account/           #    Login / signup / password flows
│
├── companies/                       # 🏢 Employer module
│   ├── models.py                    #    CompanyProfile, Job, JobApplication
│   ├── decorators.py                #    @company_required (RBAC)
│   ├── Utils/companyServices.py     #    Employer business logic
│   └── templates/companies/         #    Dashboard, job CRUD, applicant funnel
│
├── members/                         # 👤 Talent module
│   ├── models.py                    #    MemberProfile, applications
│   ├── decorators.py                #    @member_required (RBAC)
│   ├── Utils/services.py            #    Member business logic
│   └── templates/members/           #    Dashboard, applied/advertised jobs
│
├── theme/                           # 🎨 Tailwind CSS app (django-tailwind)
│   ├── static_src/
│   │   ├── src/styles.css           #    Tailwind v4 entrypoint
│   │   └── tailwind.config.js       #    Design tokens & plugins
│   └── templates/base.html          #    Theme base template
│
├── Seeds/                           # 🌱 Database seeders
│   ├── seed_accounts.py             #    Demo users & roles
│   ├── seed_companies.py            #    Company profiles
│   ├── seed_jobs.py                 #    Job postings dataset
│   ├── seed_region.py               #    Saudi geographic data
│   └── seed_skills.py               #    Skill taxonomy
│
├── locale/ar/                       # 🌍 Arabic translations
├── static/                          # 📦 Global assets (js/app.js, css, img)
├── db.sqlite3                       # 🗄️ SQLite database
├── requirements.txt                 # 📋 Python dependencies
└── manage.py                        # 🚀 Django entrypoint
```

---

## 🛠️ Technologies Used

| Category | Technology | Purpose |
|---|---|---|
| **Backend** | Python 3.14 · Django 6.0 | Core framework (MVT) |
| | django-allauth | Authentication & account management |
| | django-crispy-forms + crispy-tailwind | Tailwind-styled form rendering |
| | django-modeltranslation | Arabic/English content i18n |
| | django-environ | 12-factor environment configuration |
| **Frontend** | Tailwind CSS v4 + daisyUI 5 | Utility-first design system |
| | HTMX (django-htmx) | AJAX partial page updates |
| | Chart.js 4 | Interactive data visualization |
| | Vanilla JavaScript (ES6) | Client-side interactivity & theming |
| **Data & Analytics** | pandas · NumPy · SciPy | Data manipulation & computation |
| | statsmodels (ARIMA) | Time-series demand forecasting |
| **Database** | SQLite 3 | Zero-config relational storage |
| **Architecture** | MVT + Modular Apps | Separation of concerns per domain |
| | Service Layer Pattern | Business logic in `Utils/services.py` |
| | Decorator-based RBAC | Declarative role authorization |

---

## 🚀 Setup & Installation

### Prerequisites

| Tool | Version |
|---|---|
| Python | ≥ 3.12 (tested on 3.14) |
| Node.js + npm | ≥ 18 (for Tailwind build) |
| Git | Latest |

### 1️⃣ Clone & Create Virtual Environment

```bash
git clone https://github.com/azzaldeen-tech/Labor-Market-Trends-Analysis-Platform.git
cd Labor-Market-Trends-Analysis-Platform

# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
npm install --prefix theme/static_src   # Tailwind toolchain
```

### 3️⃣ Configure Environment Variables

Create a `.env` file in the project root:

```env
APP_NAME=LaborMarketAnalytics
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
EMAIL_SERVICE=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
```

### 4️⃣ Apply Migrations

```bash
python manage.py migrate
```

### 5️⃣ Create the Master (Admin) User

```bash
python manage.py createsuperuser
```

### 6️⃣ Seed Demo Data *(optional)*

Populate the database with realistic demo datasets:

```bash
python Seeds\seed_accounts.py
python Seeds\seed_companies.py
python Seeds\seed_skills.py
python Seeds\seed_region.py
python Seeds\seed_jobs.py
```

### 7️⃣ Build Styles & Run the Server
Development — watch & compile Tailwind (separate terminal)
```bash
python manage.py tailwind start
```
Production build
```bash
python manage.py tailwind build
```
Launch Django
```bash
python manage.py runserver
```

| Endpoint | URL |
|---|---|
| 🌐 Platform | `http://127.0.0.1:8000` |
| 🛡️ Admin panel | `http://127.0.0.1:8000/admin` |

---

## 👤 Author & Contact

<table>
<tr>
<td align="center" width="50%">

### Azzaldeen Al-Qashaei
*Python / Django Architect*

**GitHub:** [azzaldeen-tech](https://github.com/azzaldeen-tech)
**LinkedIn:** [azzaldeen-al-qashaei](https://www.linkedin.com/in/azzaldeen-al-qashaei-0a6928206)


</tr>
</table>

<div align="center">

⭐ **If this project helped you, consider giving it a star!** ⭐

</div>
