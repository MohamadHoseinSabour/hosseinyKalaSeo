"""Command Line Interface for Hosseiny Kala Advanced Harness System."""

import argparse
import datetime
import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Any

from harness.core.config import get_node_id, PROJECT_ROOT
from harness.core.engine import HarnessEngine
from harness.core.task import Task
from harness.core.git_sync import GitSync
from harness.storage.state_store import StateStore
from harness.registry.skills_registry import SkillsRegistry
from harness.registry.reminders_registry import RemindersRegistry
from harness.registry.prompts_registry import PromptsRegistry

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Terminal ANSI colors
class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[95m"
    BLUE = "\033[94m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"

def c(text: str, color: str) -> str:
    return f"{color}{text}{Colors.RESET}"

def print_banner():
    banner = f"""
{Colors.CYAN}{Colors.BOLD}================================================================================
  🚀 HOSSEINY KALA - ADVANCED DISTRIBUTED HARNESS SYSTEM (سیستم هارنس حسینی کالا)
  Multi-System Parallel Execution & Distributed State Orchestrator
================================================================================{Colors.RESET}
"""
    print(banner)

def format_progress_bar(percent: int, width: int = 20) -> str:
    filled = int(width * (percent / 100))
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {percent}%"

def cmd_status(engine: HarnessEngine, args):
    """Render comprehensive multi-system status dashboard."""
    print_banner()
    dash = engine.get_dashboard_summary()
    node_id = dash["current_node"]
    
    print(f"{c('📌 مشخصات نود فعلی (Current Worker Node):', Colors.BOLD)}")
    print(f"   • شناسه سیستم: {c(node_id, Colors.CYAN)}")
    print(f"   • تعداد ماشین‌های ثبت‌شده: {c(str(dash['total_workers']), Colors.GREEN)}")
    print(f"   • زمان جاری سیستم: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Active / In-progress tasks
    active = dash["active_tasks"]
    print(f"{c('⚡ تسک‌های فعال در حال اجرا (Active Tasks Across Machines):', Colors.BOLD)} ({len(active)})")
    if not active:
        print(f"   {c('(هیچ تسکی در حال حاضر در حال اجرا نیست)', Colors.DIM)}")
    else:
        for t in active:
            claimed_by = t.get("claimed_by", "Unknown")
            is_mine = claimed_by == node_id
            node_tag = c(f"[{claimed_by}] (همین سیستم)", Colors.GREEN) if is_mine else c(f"[{claimed_by}]", Colors.YELLOW)
            progress = t.get("progress_percent", 0)
            bar = format_progress_bar(progress)
            step_name = t.get("current_step_name", "")
            step_idx = t.get("current_step_index", 0)
            total = len(t.get("steps", []))
            
            print(f"   • {c(t['id'], Colors.BOLD)}: {t['title']}")
            print(f"     مجری: {node_tag} | پیشرفت: {bar} (گام {step_idx + 1}/{total}: {step_name})")
            if t.get("lease_expires_at"):
                print(f"     انقضای قفل: {t['lease_expires_at']}")
    print()

    # Resumable tasks
    resumable = dash["resumable_tasks"]
    if resumable:
        print(f"{c('⚠️ تسک‌های نیمه‌کاره قابل بازیابی (Resumable / Interrupted Tasks):', Colors.YELLOW + Colors.BOLD)} ({len(resumable)})")
        print(f"   {c('این تسک‌ها به علت توقف نشست یا اتمام مهلت سیستم قبلی، آماده ادامه از گام متوقف‌شده هستند:', Colors.DIM)}")
        for r in resumable:
            print(f"   👉 {c(r['id'], Colors.BOLD)}: {r['title']}")
            print(f"      گام فعلی: {r.get('current_step_name')} (پیشرفت: {r.get('progress_percent')}%)")
            print(f"      دستور ادامه: {c(f'python harness.py resume {r["id"]}', Colors.CYAN)}")
        print()

    # Backlog queue
    queue = dash["next_queued_tasks"]
    print(f"{c('📋 صف کارهای بعدی در صف انتظار (Backlog Queue):', Colors.BOLD)} (کل: {dash['queue_count']})")
    if not queue:
        print(f"   {c('(صف انتظار خالی است)', Colors.DIM)}")
    else:
        for q in queue:
            prio_color = Colors.RED if q.get("priority") == "CRITICAL" else Colors.YELLOW
            print(f"   • [{c(q.get('priority', 'MEDIUM'), prio_color)}] {c(q['id'], Colors.BOLD)}: {q['title']}")
            print(f"     دسته‌بندی: {q.get('category')} | برچسب‌ها: {', '.join(q.get('tags', []))}")
    print()

    # Recent history
    history = dash["recent_completed"]
    print(f"{c('✅ تاریخچه کارهای اخیر انجام‌شده (Completed Tasks History):', Colors.BOLD)} (کل سابقه: {dash['completed_history_count']})")
    if not history:
        print(f"   {c('(هنوز تسکی تکمیل نشده است)', Colors.DIM)}")
    else:
        for h in history:
            print(f"   ✔ {c(h.get('id', ''), Colors.GREEN)}: {h.get('title')}")
            print(f"     تکمیل توسط: {h.get('completed_by_node', 'N/A')} در {h.get('completed_at', 'N/A')}")
            if h.get("result_summary"):
                print(f"     نتیجه: {h.get('result_summary')}")
    print()

    # Quick summary of skills, prompts, and reminders
    skills_count = len(SkillsRegistry.discover_all())
    prompts_count = len(PromptsRegistry.list_prompts())
    rules_count = len(RemindersRegistry.list_all())
    print(f"{c('⚙️ منابع و ماژول‌های فعال ایجنت:', Colors.BOLD)}")
    print(f"   • اسکیل‌های ثبت‌شده (.agent/skills): {c(str(skills_count), Colors.CYAN)} عدد")
    print(f"   • الگوهای پرامپت (harness/prompts): {c(str(prompts_count), Colors.CYAN)} عدد")
    print(f"   • تذکرات و قوانین بحرانی سئو: {c(str(rules_count), Colors.CYAN)} قاعده")
    print(f"   • چک‌پوینت‌های ذخیره‌شده روی دیسک: {c(str(dash['checkpoints_count']), Colors.CYAN)} عدد")
    print(f"{Colors.CYAN}================================================================================{Colors.RESET}")

def cmd_resume(engine: HarnessEngine, args):
    """Resume an interrupted or orphaned task."""
    task_id = args.task_id
    if not task_id:
        # Find first resumable task
        resumable = engine.find_resumable_tasks()
        if not resumable:
            print(f"{c('هیچ تسک نیمه‌کاره یا بازیابی‌پذیری یافت نشد.', Colors.YELLOW)}")
            return
        task_id = resumable[0].id

    print(f"در حال بازیابی تسک {c(task_id, Colors.CYAN)} بر روی سیستم {c(engine.node_id, Colors.BOLD)}...")
    ctx = engine.resume_task(task_id)
    if not ctx:
        print(f"{c('خطا: امکان بازیابی تسک وجود ندارد یا تسک یافت نشد.', Colors.RED)}")
        return

    task = ctx.task
    print(f"{c('تسک با موفقیت بازیابی و قفل اختصاصی به این ماشین منتقل شد!', Colors.GREEN)}")
    print(f"عنوان: {task.title}")
    print(f"گام فعلی: {task.current_step_index + 1} از {task.total_steps} ({task.current_step_name})")
    print(f"درصد پیشرفت قبلی: {task.progress_percentage}%")
    
    if ctx.checkpoint_data:
        print(f"{c('داده‌های متنی و محاسبات میانی ذخیره‌شده:', Colors.BOLD)}")
        for k, v in ctx.checkpoint_data.items():
            preview = str(v)[:100] + "..." if len(str(v)) > 100 else str(v)
            print(f"   • {k}: {preview}")

    print(f"\n{c('می‌توانید اجرای این تسک را مستقیماً ادامه دهید یا گام‌ها را با دستور زیر ثبت کنید:', Colors.CYAN)}")
    print(f"python harness.py task checkpoint {task.id} --step {task.current_step_index + 1} --name \"گام بعدی\"")

def cmd_task_claim(engine: HarnessEngine, args):
    """Claim a pending task or the next highest priority task."""
    if args.task_id:
        ctx = engine.claim_task(args.task_id)
    else:
        ctx = engine.claim_next_task(category=args.category)

    if not ctx:
        print(f"{c('هیچ تسک واجد شرایطی برای دریافت یافت نشد.', Colors.YELLOW)}")
        return

    print(f"{c('تسک با موفقیت دریافت و قفل شد:', Colors.GREEN)}")
    print(f"شناسه: {ctx.task.id}")
    print(f"عنوان: {ctx.task.title}")
    print(f"اولویت: {ctx.task.priority}")
    print(f"گام ۱: {ctx.task.current_step_name}")

def cmd_task_checkpoint(engine: HarnessEngine, args):
    """Save an intermediate execution checkpoint for a task."""
    active = StateStore.get_active()
    if args.task_id not in active:
        print(f"{c(f'خطا: تسک {args.task_id} در میان تسک‌های فعال یافت نشد.', Colors.RED)}")
        return

    task = Task.from_dict(active[args.task_id])
    ctx = engine.resume_task(args.task_id)
    if not ctx:
        print(f"{c('خطا در باز کردن نشست تسک.', Colors.RED)}")
        return

    payload = {}
    if args.data:
        try:
            payload = json.loads(args.data)
        except Exception:
            payload = {"raw_note": args.data}

    ctx.checkpoint(
        step_index=args.step,
        step_name=args.name,
        data=payload,
        message=args.message or "",
    )
    print(f"{c('چک‌پوینت با موفقیت در دیسک ذخیره شد!', Colors.GREEN)}")
    print(f"تسک: {args.task_id} | گام: {args.step} ({args.name}) | پیشرفت: {ctx.task.progress_percentage}%")

def cmd_task_complete(engine: HarnessEngine, args):
    """Mark a task as completed."""
    active = StateStore.get_active()
    if args.task_id not in active:
        print(f"{c(f'خطا: تسک {args.task_id} در میان تسک‌های فعال یافت نشد.', Colors.RED)}")
        return

    ctx = engine.resume_task(args.task_id)
    if not ctx:
        print(f"{c('خطا در بارگذاری تسک.', Colors.RED)}")
        return

    artifacts = [a.strip() for a in args.artifacts.split(",")] if args.artifacts else []
    ctx.complete(result_summary=args.result or "با موفقیت تکمیل شد.", artifacts=artifacts)
    print(f"{c(f'تسک {args.task_id} با موفقیت به پایان رسید و به تاریخچه منتقل شد.', Colors.GREEN)}")

def cmd_task_fail(engine: HarnessEngine, args):
    """Mark a task as failed with error context."""
    active = StateStore.get_active()
    if args.task_id not in active:
        print(f"{c(f'تسک {args.task_id} فعال نیست.', Colors.RED)}")
        return

    ctx = engine.resume_task(args.task_id)
    if not ctx:
        return
    ctx.fail(args.error)
    print(f"{c(f'وضعیت تسک {args.task_id} به FAILED تغییر یافت و جزئیات خطا ذخیره شد.', Colors.YELLOW)}")

def cmd_task_release(engine: HarnessEngine, args):
    """Release a claimed task back into pending queue."""
    ok = engine.release_task(args.task_id)
    if ok:
        print(f"{c(f'تسک {args.task_id} با موفقیت آزاد شد و به صف بازگشت.', Colors.GREEN)}")
    else:
        print(f"{c(f'خطا: تسک {args.task_id} در میان تسک‌های فعال یافت نشد.', Colors.RED)}")

def cmd_task_add(engine: HarnessEngine, args):
    """Add a new task into the queue."""
    template_data = {}
    if args.template:
        tpl_path = PROJECT_ROOT / "harness" / "templates" / f"{args.template}.json"
        if not tpl_path.exists():
            tpl_path = PROJECT_ROOT / "harness" / "templates" / f"{args.template}_template.json"
        if tpl_path.exists():
            try:
                template_data = json.loads(tpl_path.read_text(encoding="utf-8"))
            except Exception as e:
                print(f"خطا در خواندن الگو: {e}")

    steps = template_data.get("steps", [])
    if not steps and args.steps:
        steps = [{"step_index": i, "name": s.strip(), "status": "pending"} for i, s in enumerate(args.steps.split(","))]

    task = Task(
        task_id=args.id,
        title=args.title,
        category=args.category or template_data.get("category", "general"),
        priority=args.priority or template_data.get("priority", "MEDIUM"),
        tags=[t.strip() for t in args.tags.split(",")] if args.tags else [],
        required_skills=template_data.get("required_skills", []),
        steps=steps,
        metadata={"created_via": "cli"},
    )
    task_id = engine.add_task(task)
    print(f"{c('تسک جدید با موفقیت به صف افزوده شد:', Colors.GREEN)}")
    print(f"شناسه: {task_id}")
    print(f"عنوان: {task.title}")
    print(f"تعداد گام‌ها: {len(task.steps)}")

def cmd_skills(engine: HarnessEngine, args):
    """Inspect and search installed skills."""
    if args.search:
        results = SkillsRegistry.search_skills(args.search)
        print(f"{c(f'نتایج جستجوی اسکیل برای \"{args.search}\":', Colors.BOLD)} ({len(results)} مورد)")
        for s in results:
            print(f" • {c(s.name, Colors.CYAN)} [{s.category}]: {s.description[:90]}...")
    elif args.show:
        skill = SkillsRegistry.get_skill(args.show)
        if not skill:
            print(f"{c(f'اسکیل \"{args.show}\" یافت نشد.', Colors.RED)}")
            return
        print(f"{c('نام اسکیل:', Colors.BOLD)} {skill.name}")
        print(f"{c('دسته‌بندی:', Colors.BOLD)} {skill.category}")
        print(f"{c('مسیر فایل:', Colors.BOLD)} {skill.path}")
        print(f"{c('توضیحات:', Colors.BOLD)}\n{skill.description}")
    else:
        all_skills = SkillsRegistry.list_skills(category=args.category)
        print(f"{c('لیست اسکیل‌های نصب‌شده (.agent/skills):', Colors.BOLD)} ({len(all_skills)} مورد)")
        by_cat = {}
        for s in all_skills:
            by_cat.setdefault(s.category, []).append(s)
        for cat, items in sorted(by_cat.items()):
            print(f"\n{c(f'[{cat}]', Colors.YELLOW)}")
            for item in items:
                print(f"   • {c(item.name, Colors.CYAN)}: {item.description[:75]}...")

def cmd_reminders(engine: HarnessEngine, args):
    """View and validate project reminders and critical rules."""
    if args.check:
        content = ""
        if args.file and Path(args.file).exists():
            content = Path(args.file).read_text(encoding="utf-8")
        elif args.content:
            content = args.content

        violations = RemindersRegistry.validate_content(
            html_content=content,
            slug=args.slug or "",
            status=args.status or "future",
        )
        if not violations:
            print(f"{c('✔ تمام بررسی‌های سئو و تذکرات با موفقیت پاس شدند!', Colors.GREEN)}")
        else:
            print(f"{c(f'⚠️ تعداد {len(violations)} نقض قاعده یا اخطار سئو یافت شد:', Colors.RED + Colors.BOLD)}")
            for v in violations:
                print(f"   • [{c(v['severity'], Colors.RED)}] ({v['rule_id']}): {v['message']}")
    else:
        rules = RemindersRegistry.list_all()
        print(f"{c('قوانین و تذکرات بحرانی پروژه حسینی کالا (Critical Project Reminders):', Colors.BOLD)} ({len(rules)} قاعده)")
        for r in rules:
            sev_color = Colors.RED if r.severity == "CRITICAL" else Colors.YELLOW
            print(f"\n[{c(r.rule_id, Colors.BOLD)}] [{c(r.severity, sev_color)}] {c(r.title, Colors.CYAN)}")
            print(f"   توضیح: {r.description}")
            print(f"   دستورالعمل: {c(r.recommendation, Colors.GREEN)}")

def cmd_prompts(engine: HarnessEngine, args):
    """Inspect and render system and task prompts."""
    if args.show:
        prompt = PromptsRegistry.get_prompt(args.show)
        if not prompt:
            print(f"{c(f'الگوی پرامپت \"{args.show}\" یافت نشد.', Colors.RED)}")
            return
        print(f"{c('عنوان:', Colors.BOLD)} {prompt.title}")
        print(f"{c('متغیرها:', Colors.BOLD)} {', '.join(prompt.variables) or 'None'}")
        print(f"\n{prompt.content}")
    elif args.render:
        vars_dict = {}
        if args.var:
            for item in args.var:
                if "=" in item:
                    k, v = item.split("=", 1)
                    vars_dict[k.strip()] = v.strip()
        rendered = PromptsRegistry.render(args.render, vars_dict)
        if not rendered:
            print(f"{c(f'الگوی پرامپت \"{args.render}\" یافت نشد.', Colors.RED)}")
            return
        print(rendered)
    else:
        prompts = PromptsRegistry.list_prompts()
        print(f"{c('الگوهای پرامپت ثبت‌شده (harness/prompts):', Colors.BOLD)} ({len(prompts)} مورد)")
        for p in prompts:
            print(f"   • {c(p.name, Colors.CYAN)}: {p.title}")
            if p.variables:
                print(f"     متغیرها: {', '.join(p.variables)}")

def cmd_sync(engine: HarnessEngine, args):
    """Synchronize distributed state via Git."""
    if args.pull or not args.push:
        print("در حال دریافت آخرین وضعیت از گیت (git pull --rebase)...")
        ok, msg = GitSync.pull()
        color = Colors.GREEN if ok else Colors.RED
        print(c(msg, color))

    if args.push or not args.pull:
        print("در حال همگام‌سازی و ارسال وضعیت به گیت (git push)...")
        ok, msg = GitSync.push_state(args.message or "chore(harness): sync multi-machine state")
        color = Colors.GREEN if ok else Colors.RED
        print(c(msg, color))

def main():
    parser = argparse.ArgumentParser(
        prog="harness",
        description="Hosseiny Kala Advanced Distributed Harness System",
    )
    parser.add_argument("--node-id", help="Override worker node identifier")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # status
    p_status = subparsers.add_parser("status", help="Show system dashboard and active tasks")

    # resume
    p_resume = subparsers.add_parser("resume", help="Resume interrupted task on this machine")
    p_resume.add_argument("task_id", nargs="?", help="Specific Task ID to resume")

    # task
    p_task = subparsers.add_parser("task", help="Manage individual tasks")
    task_subs = p_task.add_subparsers(dest="task_command")
    
    # task claim
    p_claim = task_subs.add_parser("claim", help="Claim next or specific task")
    p_claim.add_argument("task_id", nargs="?", help="Task ID to claim")
    p_claim.add_argument("--category", help="Filter by category")

    # task checkpoint
    p_cp = task_subs.add_parser("checkpoint", help="Save intermediate step checkpoint")
    p_cp.add_argument("task_id", help="Active Task ID")
    p_cp.add_argument("--step", type=int, required=True, help="Step index")
    p_cp.add_argument("--name", required=True, help="Step name")
    p_cp.add_argument("--data", help="JSON data string or note")
    p_cp.add_argument("--message", help="Log message")

    # task complete
    p_comp = task_subs.add_parser("complete", help="Complete a task")
    p_comp.add_argument("task_id", help="Active Task ID")
    p_comp.add_argument("--result", help="Result summary")
    p_comp.add_argument("--artifacts", help="Comma-separated artifact paths")

    # task fail
    p_fail = task_subs.add_parser("fail", help="Mark a task as failed")
    p_fail.add_argument("task_id", help="Active Task ID")
    p_fail.add_argument("--error", required=True, help="Error message")

    # task release
    p_rel = task_subs.add_parser("release", help="Release task back to pending queue")
    p_rel.add_argument("task_id", help="Active Task ID")

    # task add
    p_add = task_subs.add_parser("add", help="Add new task to queue")
    p_add.add_argument("--id", help="Custom task ID")
    p_add.add_argument("--title", required=True, help="Task title")
    p_add.add_argument("--category", help="Category")
    p_add.add_argument("--priority", choices=["CRITICAL", "HIGH", "MEDIUM", "LOW"], default="MEDIUM")
    p_add.add_argument("--tags", help="Comma-separated tags")
    p_add.add_argument("--template", help="Template name (e.g. content_pipeline)")
    p_add.add_argument("--steps", help="Comma-separated step names")

    # skills
    p_skills = subparsers.add_parser("skills", help="Explore agent skills")
    p_skills.add_argument("--category", help="Filter by category")
    p_skills.add_argument("--search", help="Search query")
    p_skills.add_argument("--show", help="Show details for skill name")

    # reminders
    p_reminders = subparsers.add_parser("reminders", help="Rules and warnings")
    p_reminders.add_argument("--check", action="store_true", help="Run validation check")
    p_reminders.add_argument("--content", help="Content string to check")
    p_reminders.add_argument("--file", help="File path to check")
    p_reminders.add_argument("--slug", help="Slug to check")
    p_reminders.add_argument("--status", help="Publish status to check")

    # prompts
    p_prompts = subparsers.add_parser("prompts", help="Prompts registry")
    p_prompts.add_argument("--show", help="Show prompt content")
    p_prompts.add_argument("--render", help="Render prompt with vars")
    p_prompts.add_argument("--var", action="append", help="Variable as key=val")

    # sync
    p_sync = subparsers.add_parser("sync", help="Synchronize distributed state with Git")
    p_sync.add_argument("--pull", action="store_true", help="Pull only")
    p_sync.add_argument("--push", action="store_true", help="Push only")
    p_sync.add_argument("--message", help="Commit message")

    args = parser.parse_args()
    engine = HarnessEngine(node_id=args.node_id)

    if args.command == "status" or not args.command:
        cmd_status(engine, args)
    elif args.command == "resume":
        cmd_resume(engine, args)
    elif args.command == "task":
        if args.task_command == "claim":
            cmd_task_claim(engine, args)
        elif args.task_command == "checkpoint":
            cmd_task_checkpoint(engine, args)
        elif args.task_command == "complete":
            cmd_task_complete(engine, args)
        elif args.task_command == "fail":
            cmd_task_fail(engine, args)
        elif args.task_command == "release":
            cmd_task_release(engine, args)
        elif args.task_command == "add":
            cmd_task_add(engine, args)
        else:
            cmd_status(engine, args)
    elif args.command == "skills":
        cmd_skills(engine, args)
    elif args.command == "reminders":
        cmd_reminders(engine, args)
    elif args.command == "prompts":
        cmd_prompts(engine, args)
    elif args.command == "sync":
        cmd_sync(engine, args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
