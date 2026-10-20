"""Registry and scanner for all agent skills."""

import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from harness.core.config import SKILLS_DIR

class SkillInfo:
    """Represents a discovered agent skill."""
    
    def __init__(
        self,
        name: str,
        path: Path,
        description: str = "",
        category: str = "General",
    ):
        self.name = name
        self.path = path
        self.description = description
        self.category = category

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "path": str(self.path),
        }

class SkillsRegistry:
    """Discovers, parses, and searches all installed skills."""
    
    _CORE_HOSSEINY_SKILLS = {
        "seo-optimization": "Core Hosseiny SEO",
        "content-writing": "Core Hosseiny Content",
        "content-humanizer": "Core Hosseiny Tone",
        "ecommerce-seo": "Core Hosseiny Store",
        "technical-seo": "Core Hosseiny Technical",
        "wordpress-content-agent-api": "Core Hosseiny API",
    }
    
    _CATEGORY_MAPPINGS = {
        "copywriting": "Copywriting & CRO",
        "copy-editing": "Copywriting & CRO",
        "cro": "Copywriting & CRO",
        "signup": "Copywriting & CRO",
        "onboarding": "Copywriting & CRO",
        "paywalls": "Copywriting & CRO",
        "popups": "Copywriting & CRO",
        "offers": "Copywriting & CRO",
        "schema": "Technical & SEO",
        "seo-audit": "Technical & SEO",
        "site-architecture": "Technical & SEO",
        "programmatic-seo": "Technical & SEO",
        "ai-seo": "Technical & SEO",
        "analytics": "Analytics & Attribution",
        "attribution": "Analytics & Attribution",
        "ab-testing": "Analytics & Attribution",
        "image": "Multimedia & Creative",
        "video": "Multimedia & Creative",
        "ad-creative": "Multimedia & Creative",
        "ads": "Paid Acquisition",
        "social": "Growth & Distribution",
        "cold-email": "Outreach & Sales",
        "emails": "Lifecycle Marketing",
        "content-strategy": "Strategy & Planning",
        "marketing-council": "Strategy & Planning",
        "marketing-ideas": "Strategy & Planning",
        "marketing-plan": "Strategy & Planning",
    }

    @staticmethod
    def _parse_frontmatter(content: str) -> Dict[str, str]:
        """Extract yaml-like frontmatter metadata from SKILL.md."""
        meta = {}
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                for line in frontmatter.strip().splitlines():
                    if ":" in line:
                        k, v = line.split(":", 1)
                        meta[k.strip()] = v.strip().strip('"').strip("'")
        return meta

    @classmethod
    def discover_all(cls) -> Dict[str, SkillInfo]:
        """Scan SKILLS_DIR and return all registered skills."""
        skills: Dict[str, SkillInfo] = {}
        if not SKILLS_DIR.exists():
            return skills

        for skill_folder in sorted(SKILLS_DIR.iterdir()):
            if not skill_folder.is_dir():
                continue
                
            skill_md = skill_folder / "SKILL.md"
            if not skill_md.exists():
                continue

            name = skill_folder.name
            desc = ""
            try:
                content = skill_md.read_text(encoding="utf-8")
                meta = cls._parse_frontmatter(content)
                desc = meta.get("description", "")
                if not desc:
                    # fallback to first markdown paragraph
                    lines = [l.strip() for l in content.splitlines() if l.strip() and not l.startswith("#") and not l.startswith("---")]
                    if lines:
                        desc = lines[0][:150]
            except Exception:
                desc = "Registered skill"

            # Determine category
            category = cls._CORE_HOSSEINY_SKILLS.get(name)
            if not category:
                category = cls._CATEGORY_MAPPINGS.get(name, "Marketing & Execution")

            skills[name] = SkillInfo(
                name=name,
                path=skill_md,
                description=desc,
                category=category,
            )

        return skills

    @classmethod
    def list_skills(cls, category: Optional[str] = None) -> List[SkillInfo]:
        all_skills = list(cls.discover_all().values())
        if category:
            all_skills = [s for s in all_skills if s.category.lower() == category.lower()]
        return all_skills

    @classmethod
    def get_skill(cls, name: str) -> Optional[SkillInfo]:
        return cls.discover_all().get(name)

    @classmethod
    def search_skills(cls, query: str) -> List[SkillInfo]:
        q = query.lower()
        results = []
        for s in cls.discover_all().values():
            if q in s.name.lower() or q in s.description.lower() or q in s.category.lower():
                results.append(s)
        return results
