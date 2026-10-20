"""Reminders and critical rule enforcement engine (سیستم تذکرات و قوانین بحرانی)."""

import re
from typing import Dict, Any, List, Optional, Tuple

class ReminderRule:
    """Definition of a critical rule or guideline for Hosseiny Kala."""
    
    def __init__(
        self,
        rule_id: str,
        title: str,
        severity: str,
        category: str,
        description: str,
        recommendation: str,
    ):
        self.rule_id = rule_id
        self.title = title
        self.severity = severity  # "CRITICAL", "HIGH", "STANDARD"
        self.category = category
        self.description = description
        self.recommendation = recommendation

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.rule_id,
            "title": self.title,
            "severity": self.severity,
            "category": self.category,
            "description": self.description,
            "recommendation": self.recommendation,
        }

class RemindersRegistry:
    """Main repository and validator for critical project reminders and rules."""
    
    RULES: List[ReminderRule] = [
        ReminderRule(
            rule_id="RULE-01",
            title="الزام قطعی لینک‌های کاننیکال و منع شناسه عددی (Canonical URLs Only)",
            severity="CRITICAL",
            category="Internal Linking",
            description="در ووکامرس، پارامتر به فرمت ?product_cat=ID یا ?p=ID به خطای ۴۰۴ قطعی یا ریدایرکت اضافی منجر می‌شود.",
            recommendation="تمامی دسته‌بندی‌ها الزاماً با آدرس کاننیکال /product-category/{slug}/ و محصولات با /product/{slug}/ مستقیماً از data/categories.json و data/products.json درج شوند.",
        ),
        ReminderRule(
            rule_id="RULE-02",
            title="عدم درج هرگونه متن روی تصاویر کاور و شاخص (No Text on Images)",
            severity="CRITICAL",
            category="Media",
            description="تصاویر کاور و شاخص وبلاگ باید کاملاً خالص، طبیعی و فاقد هرگونه متن، عنوان، فونت یا واترمارک باشند.",
            recommendation="از پرامپت‌های کاملاً تمیز و خالص بدون نوشته متنی استفاده شده و خروجی قبل از آپلود بررسی شود.",
        ),
        ReminderRule(
            rule_id="RULE-03",
            title="مشخصات ابعاد و حجم تصویر شاخص (1599x900px, ~100KB)",
            severity="CRITICAL",
            category="Media",
            description="ابعاد تصویر شاخص باید افقی 1599 در 900 پیکسل و حجم فشرده‌شده بین 80 تا 120 کیلوبایت باشد.",
            recommendation="در صورت وجود محصول، تصویر واقعی از سایت به عنوان رفرنس تولید تصویر استفاده شود.",
        ),
        ReminderRule(
            rule_id="RULE-04",
            title="منع انتشار مستقیم و الزام زمان‌بندی (Scheduled Only)",
            severity="CRITICAL",
            category="WordPress Publishing",
            description="ایجنت به هیچ عنوان حق انتشار مستقیم (status: publish) مقالات را ندارد.",
            recommendation="تمام مقالات جدید الزاماً با وضعیت زمان‌بندی (status: future) در روزهای یک‌شنبه، سه‌شنبه و پنج‌شنبه ساعت ۱۹:۳۰ یا پیش‌نویس (draft) ثبت شوند.",
        ),
        ReminderRule(
            rule_id="RULE-05",
            title="ساختار اسلاگ (Slug) انگلیسی کوتاه و مفهومی",
            severity="HIGH",
            category="SEO URLs",
            description="اسلاگ محصولات و مقالات باید کاملاً انگلیسی، معنادار، کوتاه و با فرمت brand-model-category-spec باشد.",
            recommendation="از ایجاد Slugهای فارسی بریده‌شده یا تکراری اکیداً پرهیز شود (مثال: clover-frnt-70-glory-plus).",
        ),
        ReminderRule(
            rule_id="RULE-06",
            title="مدیریت کاتالوگ، فرمول درصد تغییر و رنگ‌بندی پویا",
            severity="CRITICAL",
            category="Catalog & Pricing",
            description="کاتالوگ دارای ۱۸ ستون است. ستون E دارای فرمول خودکار =(B-D)/D است و تغییرات بالای ۵۰٪ نارنجی هشدار (#FCE4D6) می‌شوند. در محصولات متغیر، والد نباید قیمت داشته باشد.",
            recommendation="قیمت فقط به تنوع‌ها (فرزندان) داده شود و وضعیت در سایت (ستون R) بر اساس موجودی و قوانین فروشگاه رعایت گردد.",
        ),
        ReminderRule(
            rule_id="RULE-07",
            title="املای صحیح و یکپارچه برند «هاورسن»",
            severity="HIGH",
            category="Branding",
            description="نام برند هاورسن باید در کل سایت، کاتالوگ اکسل و دیتابیس دقیقاً با املای فارسی «هاورسن» نوشته شود.",
            recommendation="از نگارش‌های اشتباه مانند «آورسون» یا «هاورسون» خودداری شود.",
        ),
        ReminderRule(
            rule_id="RULE-08",
            title="انکر تکست صفحه اصلی و موقعیت جغرافیایی فروشگاه",
            severity="HIGH",
            category="SEO On-Page",
            description="هنگام لینک دادن به صفحه اصلی (hosseinykala.ir)، انکر تکست باید «فروشگاه لوازم خانگی حسینی» باشد.",
            recommendation="در محتوا به استقرار و شعب حضوری فروشگاه در اهواز اشاره شود.",
        ),
        ReminderRule(
            rule_id="RULE-09",
            title="ارتباط استاندارد با REST API رسمی وردپرس با نقش ویرایشگر (Editor)",
            severity="CRITICAL",
            category="Technical API",
            description="کلیه تعاملات باید از طریق اندپوینتهای استاندارد /wp-json/wp/v2/ با دسترسی کاربر agent انجام پذیرد.",
            recommendation="هیچ کد یا اندپوینت غیراستانداردی صدا زده نشود و خطاهای ۴۰۱ یا ۴۰۳ سریعاً گزارش شوند.",
        ),
        ReminderRule(
            rule_id="RULE-10",
            title="ثبت کامل فوکوس کیورد و برچسب‌های سئو در متادیتا",
            severity="HIGH",
            category="SEO Metadata",
            description="هنگام ارسال مقاله، کلمه کلیدی اصلی (Focus Keyword) در فیلدهای Rank Math / Yoast و برچسب‌های هدفمند ثبت گردند.",
            recommendation="از تنظیم صحیح meta description و rank_math_focus_keyword اطمینان حاصل شود.",
        ),
    ]

    @classmethod
    def list_all(cls) -> List[ReminderRule]:
        return cls.RULES

    @classmethod
    def get_rule(cls, rule_id: str) -> Optional[ReminderRule]:
        for r in cls.RULES:
            if r.rule_id.lower() == rule_id.lower():
                return r
        return None

    @classmethod
    def validate_content(
        cls,
        html_content: str,
        slug: str = "",
        status: str = "future",
    ) -> List[Dict[str, Any]]:
        """Run automated heuristic validation against critical rules."""
        violations = []
        
        # Check Rule 1: No query param IDs
        if "?product_cat=" in html_content:
            violations.append({
                "rule_id": "RULE-01",
                "severity": "CRITICAL",
                "message": "استفاده غیرمجاز از ?product_cat=ID یافت شد! این لینک به خطای ۴۰۴ منتهی می‌شود.",
            })
        if re.search(r'\?p=\d+', html_content):
            violations.append({
                "rule_id": "RULE-01",
                "severity": "CRITICAL",
                "message": "استفاده از شناسه عددی ?p=ID در لینک‌ها مشاهده شد. باید به آدرس دائمی کاننیکال تبدیل شود.",
            })

        # Check Rule 4: No direct publish
        if status.lower() == "publish":
            violations.append({
                "rule_id": "RULE-04",
                "severity": "CRITICAL",
                "message": "وضعیت انتشار مستقیم (publish) مجاز نیست! باید future یا draft باشد.",
            })

        # Check Rule 5: Slug english only
        if slug and re.search(r'[\u0600-\u06FF]', slug):
            violations.append({
                "rule_id": "RULE-05",
                "severity": "HIGH",
                "message": f"اسلاگ شامل حروف فارسی است ('{slug}'). اسلاگ باید انگلیسی کوتاه و معنادار باشد.",
            })

        # Check Rule 7: Haversen spelling
        if "آورسون" in html_content or "هاورسون" in html_content:
            violations.append({
                "rule_id": "RULE-07",
                "severity": "HIGH",
                "message": "املای اشتباه برای برند هاورسن یافت شد. املای صحیح «هاورسن» است.",
            })

        return violations
