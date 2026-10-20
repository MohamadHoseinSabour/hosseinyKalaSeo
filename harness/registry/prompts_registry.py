"""Prompts registry and template interpolation manager (سیستم پرامپت‌ها)."""

import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from harness.core.config import PROMPTS_DIR

class PromptTemplate:
    """Represents a structured prompt template."""
    
    def __init__(
        self,
        name: str,
        path: Path,
        title: str = "",
        description: str = "",
        content: str = "",
        variables: Optional[List[str]] = None,
    ):
        self.name = name
        self.path = path
        self.title = title or name.replace("_", " ").title()
        self.description = description
        self.content = content
        self.variables = variables or []

    def render(self, context: Dict[str, Any]) -> str:
        """Interpolate variable placeholders like {var_name}."""
        rendered = self.content
        for k, v in context.items():
            rendered = rendered.replace(f"{{{k}}}", str(v))
        return rendered

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "title": self.title,
            "description": self.description,
            "path": str(self.path),
            "variables": self.variables,
        }

class PromptsRegistry:
    """Manages loading, parsing, and rendering prompt templates."""
    
    @classmethod
    def list_prompts(cls) -> List[PromptTemplate]:
        prompts = []
        if not PROMPTS_DIR.exists():
            return prompts

        for f in sorted(PROMPTS_DIR.glob("*.md")):
            name = f.stem
            try:
                raw = f.read_text(encoding="utf-8")
                # Parse title and description if available
                title = name
                desc = ""
                for line in raw.splitlines()[:5]:
                    if line.startswith("# "):
                        title = line[2:].strip()
                    elif line.startswith("> ") and not desc:
                        desc = line[2:].strip()

                import re
                vars_found = sorted(list(set(re.findall(r'\{([a-zA-Z0-9_]+)\}', raw))))

                prompts.append(PromptTemplate(
                    name=name,
                    path=f,
                    title=title,
                    description=desc,
                    content=raw,
                    variables=vars_found,
                ))
            except Exception:
                pass

        return prompts

    @classmethod
    def get_prompt(cls, name: str) -> Optional[PromptTemplate]:
        for p in cls.list_prompts():
            if p.name.lower() == name.lower():
                return p
        return None

    @classmethod
    def render(cls, name: str, variables: Dict[str, Any]) -> Optional[str]:
        prompt = cls.get_prompt(name)
        if not prompt:
            return None
        return prompt.render(variables)
