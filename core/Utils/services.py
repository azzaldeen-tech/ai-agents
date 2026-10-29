import asyncio
import re

import playwright_stealth
from playwright.async_api import async_playwright
from django.utils.translation import gettext_lazy as _
# from core.tests import JobAdvertisement

#
# async def run_professional_scraper(search_query):
#     async with async_playwright() as p:
#         # 1. إعداد المتصفح بوضع التخفي
#         browser = await p.chromium.launch(headless=True)
#         context = await browser.new_context(
#             user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
#         )
#         page = await context.new_page()
#         try:
#             await playwright_stealth.stealth_async(page)
#         except:
#             pass
#
#
#         # 2. بناء الرابط والتوجه للموقع (مثال: LinkedIn)
#         url = f"https://www.linkedin.com/jobs/search/?keywords={search_query}&location=Yemen"
#         await page.goto(url, wait_until="networkidle")
#
#         # 3. جلب البيانات المرجعية من قاعدة البيانات لتحسين الأداء
#         all_standard_titles = list(StandardTitle.objects.all())
#         all_standard_skills = list(StandardSkill.objects.all())
#
#         # 4. تحديد كروت الوظائف في الصفحة
#         job_cards = await page.query_selector_all('.job-search-card')
#
#         count = 0
#         for card in job_cards:
#             try:
#                 # استخراج النصوص الأساسية
#                 raw_title = (await (await card.query_selector('.base-search-card__title')).inner_text()).strip()
#                 company = (await (await card.query_selector('.base-search-card__subtitle')).inner_text()).strip()
#                 link_element = await card.query_selector('a.base-card__full-link')
#                 link = await link_element.get_attribute('href') if link_element else ""
#
#                 # --- ذكاء الربط: تحديد المسمى الموحد ---
#                 matched_title = None
#                 for st in all_standard_titles:
#                     # نتحقق إذا كان الـ Slug الخاص بنا موجوداً داخل العنوان المسحوب
#                     if st.slug.replace('-', ' ') in raw_title.lower():
#                         matched_title = st
#                         break
#
#                 # --- إنشاء الإعلان في قاعدة البيانات ---
#                 # نستخدم update_or_create لمنع التكرار بناءً على الرابط
#                 job_ad, created = JobAdvertisement.objects.update_or_create(
#                     source_url=link,
#                     defaults={
#                         'title_ref': matched_title,
#                         'raw_title': raw_title,
#                         'company_name': company,
#                         'source_type': 'scraped',
#                         'location': "Yemen",
#                         'description': f"Automated scrape for {raw_title} at {company}"
#                     }
#                 )
#
#                 # --- ذكاء الاستخلاص: تحديد المهارات المطلوبة ---
#                 if created:
#                     found_skills = []
#                     for skill in all_standard_skills:
#                         # نبحث عن الكلمات المفتاحية للمهارة داخل عنوان الوظيفة
#                         # ملاحظة: يمكنك تطوير هذا ليشمل الوصف الكامل لاحقاً
#                         pattern = rf"\b{re.escape(skill.search_keywords.lower())}\b"
#                         if re.search(pattern, raw_title.lower()):
#                             found_skills.append(skill)
#
#                     if found_skills:
#                         job_ad.skills.add(*found_skills)
#
#                     count += 1
#                     print(f"✅ تم حفظ: {raw_title}")
#
#             except Exception as e:
#                 print(f"⚠️ خطأ في معالجة كرت وظيفي: {e}")
#                 continue
#
#         await browser.close()
#         return count
#
#
# async def run_live_search_scraper(search_query):
#     job_results = []  # قائمة لتخزين النتائج وعرضها فوراً
#
#     async with async_playwright() as p:
#         # 1. إعداد المتصفح بوضع التخفي
#         browser = await p.chromium.launch(headless=True)
#         context = await browser.new_context(
#             user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
#         )
#         page = await context.new_page()
#         # await stealth_page(page)
#         try:
#             await playwright_stealth.stealth_async(page)
#         except:
#             pass
#         # 2. بناء الرابط والتوجه للموقع (LinkedIn كمثال)
#         # ملاحظة: تم تعديل الرابط ليشمل الدولة والبحث
#         url = f"https://www.linkedin.com/jobs/search/?keywords={search_query}"
#         await page.goto(url, wait_until="networkidle")
#
#         # 3. تحديد كروت الوظائف في الصفحة
#         job_cards = await page.query_selector_all('.job-search-card')
#
#         for card in job_cards:
#             try:
#                 # استخراج النصوص الأساسية
#                 title_el = await card.query_selector('.base-search-card__title')
#                 company_el = await card.query_selector('.base-search-card__subtitle')
#                 link_el = await card.selector('a.base-card__full-link') or await card.query_selector('a')
#
#                 title_text = (await title_el.inner_text()).strip() if title_el else "عنوان غير متوفر"
#                 company_text = (await company_el.inner_text()).strip() if company_el else "شركة غير معروفة"
#                 link_url = await link_el.get_attribute('href') if link_el else "#"
#
#                 # إضافة النتيجة إلى القائمة بدلاً من حفظها في قاعدة البيانات
#                 job_results.append({
#                     'title': title_text,
#                     'company': company_text,
#                     'link': link_url,
#                     'source': 'LinkedIn'
#                 })
#
#             except Exception as e:
#                 print(f"⚠️ خطأ أثناء قراءة بيانات الوظيفة: {e}")
#                 continue
#
#         await browser.close()
#         return job_results  # نعود بالنتائج لكي تعرضها في المتصفح
# # دالة وسيطة للتشغيل من الـ View (تتعامل مع الـ Async)
# def start_sync_scraper(query):
#     return asyncio.run(run_live_search_scraper(query))
#     # return asyncio.run(run_professional_scraper(query))