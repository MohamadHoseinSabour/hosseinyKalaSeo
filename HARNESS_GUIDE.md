# راهنمای جامع سیستم هارنس توزیع‌شده حسینی کالا (Hosseiny Kala Advanced Harness System)

این سند مرجع رسمی و مستندات عملیاتی **سیستم هارنس پیشرفته (Advanced Harness System)** برای پروژه سئو و محتوای فروشگاه اینترنتی **حسینی کالا (hosseinykala.ir)** است. این سیستم به گونه‌ای طراحی شده است که چندین سیستم و مجری هوش مصنوعی بتوانند به صورت **موازی و توزیع‌شده (Distributed & Parallel)** بدون تداخل یا دوباره‌کاری روی پروژه کار کنند، تسک‌ها را مدیریت نمایند، و در صورت توقف ناگهانی یک نشست روی یک سیستم، ادامه کار از همان گام دقیق روی سیستم دیگر از سر گرفته شود.

---

## 🎯 ۱. اهداف و قابلیت‌های محوری سیستم هارنس

1. **مدیریت موازی چند سیستمی (Multi-System Execution):**
   - پشتیبانی از اجرای همزمان روی لپ‌تاپ، سرور و کامپیوترهای مختلف.
   - شناسه اختصاصی نود بر اساس نام سیستم و کاربر (`Node ID`).
   - سازوکار قفل اجاره‌ای موقت (`Lease Lock`) جهت جلوگیری از کار همزمان دو سیستم روی یک تسک.

2. **ذخیره نشست و بازیابی از نقطه توقف (Session Checkpointing & Resume):**
   - ذخیره ریز به ریز وضعیت اجرای گام‌ها (Step Index, Progress %, Intermediate Data).
   - انتقال خودکار تسک نیمه‌کاره به سیستم دیگر با دستور `harness resume`.
   - عدم هدررفت پیش‌نویس‌ها و محاسبات انجام‌شده در صورت قطعی اینترنت، بسته‌شدن پنجره یا تغییر سیستم.

3. **سیستم تذکرات و قوانین بحرانی (Critical Reminders Engine):**
   - پایش و اعتبارسنجی خودکار کلیه قوانین ثابت پروژه (لینک‌های کاننیکال، منع `?product_cat=ID`، عدم وجود متن روی تصویر شاخص، ابعاد ۱۵۹۹ در ۹۰۰، وضعیت الزاماً زمان‌بندی‌شده، املای هاورسن و فرمول‌های کاتالوگ).

4. **فهرست اسکیل‌های نصب‌شده (Skills Registry):**
   - اسکن و شناسایی ۵۶ اسکیل تخصصی موجود در مسیر `.agent/skills/`.
   - امکان جستجو و بررسی پیش‌نیازهای هر اسکیل برای اجرای تسک‌ها.

5. **سیستم پرامپت‌ها و الگوهای آماده (Prompts Registry):**
   - پرامپت‌های استاندارد مقاله‌نویسی پیلار، غنی‌سازی صفحه محصول، سئو دسته‌بندی و همگام‌سازی کاتالوگ با قابلیت تزریق متغیرها (`Variables Interpolation`).

6. **شفافیت کامل تاریخچه و صف کارها (Task Lifecycle & Audit Log):**
   - تفکیک دقیق: کارهای پایان‌یافته (`tasks_history.json`)، کارهای در جریان (`tasks_active.json`) و کارهای در صف انتظار (`tasks_queue.json`).

---

## 🏗️ ۲. معماری فایل‌ها و دایرکتوری‌ها

```text
hosseinyKalaSeo/
│
├── harness.py                    # لانچر اصلی پایتون
├── harness.bat                   # فایل اجرایی سریع در خط فرمان ویندوز
├── harness.ps1                   # اسکریپت پاورشل با پشتیبانی از UTF-8
├── HARNESS_GUIDE.md              # راهنمای کامل سیستم (همین فایل)
│
├── harness/
│   ├── __init__.py               # اکسپورت‌های ماژول و تابع get_harness()
│   ├── cli.py                    # رابط کاربری کنسولی و داشبورد ترمینال
│   │
│   ├── core/
│   │   ├── config.py             # مسیرها، شناسه‌های پیش‌فرض و تنظیمات قفل
│   │   ├── node.py               # شناسایی مشخصات سخت‌افزاری و ثبت ضربان قلب نودها
│   │   ├── task.py               # مدل داده تسک و چرخه حیات گام‌ها
│   │   ├── session.py            # مدیریت نشست اجرایی، چک‌پوینت‌ها و Context Manager
│   │   ├── engine.py             # هسته هماهنگ‌کننده صف، دریافت، بازیابی و آزادسازی
│   │   └── git_sync.py           # ابزار همگام‌سازی خودکار وضعیت با Git
│   │
│   ├── storage/
│   │   └── state_store.py        # ذخیره‌سازی اتمیک JSON و مدیریت فایل‌های دیسک
│   │
│   ├── registry/
│   │   ├── skills_registry.py    # اسکنر و دسته‌بندی ۵۶ اسکیل ایجنت
│   │   ├── reminders_registry.py # سیستم تذکرات و ولیدیتور قوانین طلایی
│   │   └── prompts_registry.py   # لودر و رندرر قالب‌های پرامپت
│   │
│   ├── prompts/                  # قالب‌های پرامپت با فرمت Markdown
│   │   ├── master_system_prompt.md
│   │   ├── buying_guide_article_prompt.md
│   │   ├── product_enrichment_prompt.md
│   │   ├── category_seo_pillar_prompt.md
│   │   ├── technical_seo_audit_prompt.md
│   │   └── excel_catalog_sync_prompt.md
│   │
│   ├── templates/                # پایپ‌لاین‌های آماده گردش کار (Pipeline Templates)
│   │   ├── content_pipeline_template.json
│   │   ├── product_sync_template.json
│   │   └── seo_audit_template.json
│   │
│   └── state/                    # دیتابیس وضعیت هماهنگ‌شده با گیت (Git-Tracked State)
│       ├── tasks_queue.json      # صف کارهای آینده (Backlog)
│       ├── tasks_active.json     # تسک‌های در حال اجرا در سیستم‌ها
│       ├── tasks_history.json    # سوابق کارهای تکمیل‌شده
│       ├── workers_registry.json # رجیستری ماشین‌ها و آخرین ضربان قلب
│       └── checkpoints/          # فایل‌های چک‌پوینت ریز برای هر تسک
```

---

## ⚡ ۳. راهنمای دستورات خط فرمان (CLI Reference)

برای اجرای فرامین، می‌توانید از `python harness.py` یا در ویندوز مستقیماً از `harness` استفاده نمایید:

### ۳.۱. مشاهده داشبورد جامع و وضعیت نودها (`status`)
نمایش مشخصات نود فعلی، تسک‌های در حال اجرا در تمامی سیستم‌ها، تسک‌های نیمه‌کاره، صف آینده و خلاصه تاریخچه:
```bash
python harness.py status
```

### ۳.۲. بازیابی تسک نیمه‌کاره روی یک سیستم دیگر (`resume`)
اگر تسکی روی کامپیوتر محل کار نصفه مانده یا فرآیند قطع شده است، با اجرای این دستور در لپ‌تاپ یا سیستم دوم، قفل به ماشین جدید منتقل شده و از آخرین گام ادامه می‌یابد:
```bash
# بازیابی خودکار اولین تسک متوقف‌شده:
python harness.py resume

# یا بازیابی تسک مشخص با شناسه:
python harness.py resume TASK-QUEUE-001
```

### ۳.۳. مدیریت تسک‌ها (`task`)

#### الف) دریافت و قفل تسک از صف (`claim`):
```bash
# دریافت تسک با اولویت بالاتر:
python harness.py task claim

# دریافت تسک بر اساس دسته‌بندی خاص (content / catalog / audit):
python harness.py task claim --category content

# دریافت یک تسک مشخص با شناسه:
python harness.py task claim TASK-QUEUE-002
```

#### ب) ثبت چک‌پوینت میانی در حین کار (`checkpoint`):
در پایان هر مرحله (مثلاً پس از تولید متن اولیه یا تولید تصویر)، این دستور را اجرا کنید تا وضعیت و داده‌های میانی ذخیره شوند:
```bash
python harness.py task checkpoint TASK-QUEUE-001 --step 2 --name "نگارش متن پیش‌نویس" --data '{"draft_words": 2100, "status": "draft_complete"}' --message "متن اولیه آماده شد"
```

#### ج) تکمیل نهایی تسک (`complete`):
تسک از حالت فعال خارج شده، چک‌پوینت آن پاک و به عنوان سابقه موفق ثبت می‌گردد:
```bash
python harness.py task complete TASK-QUEUE-001 --result "مقاله با موفقیت زمان‌بندی شد" --artifacts "pipeline/draft.md,data/posts.json"
```

#### د) گزارش خطا و توقف تسک (`fail`):
```bash
python harness.py task fail TASK-QUEUE-001 --error "خطای عدم برقراری ارتباط با وردپرس (۴۰۳)"
```

#### ه) آزادسازی تسک و بازگرداندن به صف (`release`):
اگر سیستمی بخواهد بدون اتمام کار، تسک را برای سایر سیستم‌ها آزاد کند:
```bash
python harness.py task release TASK-QUEUE-001
```

#### و) افزودن تسک جدید با الگو (`add`):
```bash
python harness.py task add --title "نگارش راهنمای خرید مایکروویو" --category content --priority HIGH --template content_pipeline
```

---

## 🔍 ۴. سیستم تذکرات و بررسی قوانین بحرانی (`reminders`)

این بخش تضمین می‌کند که هیچ تولید محتوا یا تنظیمی برخلاف قوانین سئو حسینی کالا صورت نگیرد.

### ۴.۱. مشاهده لیست ۱۰ تذکر حیاتی:
```bash
python harness.py reminders
```

### ۴.۲. آزمون و اعتبارسنجی خودکار متن یا فایل:
تست هوشمند برای بررسی خطای `?product_cat=ID`، اسلاگ‌های فارسی، املای هاورسن و وضعیت زمان‌بندی:
```bash
python harness.py reminders --check --file path/to/article.html --slug "samsung-rt50-fridge" --status "future"
```

---

## 🧠 ۵. کار با اسکیل‌ها و پرامپت‌ها (`skills` & `prompts`)

### ۵.۱. جستجو و مشاهده اسکیل‌ها:
```bash
# لیست کلیه اسکیل‌ها:
python harness.py skills

# جستجوی اسکیل بر اساس کلیدواژه:
python harness.py skills --search "seo"

# مشاهده توضیحات کامل یک اسکیل:
python harness.py skills --show "content-humanizer"
```

### ۵.۲. فراخوانی و رندر قالب‌های پرامپت:
```bash
# لیست الگوهای پرامپت موجود:
python harness.py prompts

# رندر پرامپت با متغیرهای دلخواه:
python harness.py prompts --render buying_guide_article_prompt \
  --var topic_title="راهنمای خرید ماشین ظرفشویی" \
  --var focus_keyword="خرید ماشین ظرفشویی در اهواز" \
  --var category_name="ماشین ظرفشویی" \
  --var category_canonical_url="https://hosseinykala.ir/product-category/dishwasher/"
```

---

## 🔄 ۶. پروتکل همگام‌سازی چند سیستمی با گیت (`sync`)

برای انتقال آخرین وضعیت بین سیستم‌ها (مثلاً انتقال از کامپیوتر دفتر به سیستم منزل):

```bash
# دریافت آخرین تسک‌ها و تغییرات از گیت:
python harness.py sync --pull

# ارسال آخرین چک‌پوینت‌ها و وضعیت تسک‌ها به گیت:
python harness.py sync --push --message "chore(harness): update active checkpoint"

# انجام همزمان دریافت و ارسال:
python harness.py sync
```

---

## 💻 ۷. استفاده از هارنس درون اسکریپت‌های پایتون (Python SDK)

توسعه‌دهندگان و اسکریپت‌های اتوماسیون می‌توانند مستقیماً از هارنس استفاده کنند:

```python
from harness import get_harness

# ۱. دریافت نمونه موتور هارنس
engine = get_harness()

# ۲. ادعای بالاترین تسک در صف
ctx = engine.claim_next_task(category="content")

if ctx:
    with ctx:
        print(f"شروع اجرای تسک: {ctx.task.title}")
        
        # گام اول
        ctx.checkpoint(
            step_index=0,
            step_name="تحقیق کلمات کلیدی",
            data={"keywords": ["یخچال دیپوینت اهواز", "قیمت یخچال"]}
        )
        
        # انجام پردازش و ثبت گام دوم
        ctx.checkpoint(
            step_index=1,
            step_name="تولید پیش‌نویس",
            data={"draft_file": "pipeline/draft.md"}
        )
        
        # در صورت بروز استثنا یا قطع برنامه، وضعیت تا همین گام ذخیره شده
        # و سیستم دیگر می‌تواند با ctx.resume_task آن را ادامه دهد.
        
        # اتمام کار
        ctx.complete(result_summary="مقاله با موفقیت تدوین و زمان‌بندی شد.")
```

---

## 🛡️ ۸. اصول ایمنی و استانداردهای تضمین‌شده

1. **انحصاری بودن قفل (Single Ownership):** هر تسک در یک زمان فقط متعلق به یک سیستم است (`claimed_by`).
2. **انقضای خودکار قفل رهاشده (Lease Expiry):** در صورتی که سیستمی دچار قطعی برق یا آسیب شود، پس از اتمام مدت زمان لیس (پیش‌فرض ۴۵ دقیقه)، تسک به عنوان «آماده بازیابی» علامت‌گذاری می‌شود تا سایر سیستم‌ها بتوانند آن را بردارند.
3. **نگهداری اتمیک داده‌ها (Atomic Writes):** کلیه ذخیره‌سازی‌ها با ایجاد فایل موقت و انتقال امن انجام می‌شوند تا در صورت قطع برق، فایل دیتابیس دچار خرابی (Corruption) نشود.
4. **رعایت قوانین سئو (SEO Compliance):** تمام الگوها و ولیدیتورهای داخلی، استانداردهای اختصاصی حسینی کالا را به طور کامل پوشش می‌دهند.
