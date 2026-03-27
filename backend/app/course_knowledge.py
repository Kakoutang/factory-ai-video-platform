from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DOCS_ROOT = PROJECT_ROOT / "docs"
OPERATIONS_MANUAL_PATH = DOCS_ROOT / "operations-manual.md"
COURSE_CORPUS_ROOT = DOCS_ROOT / "course-corpus" / "raw"


def read_operations_manual() -> str:
    if not OPERATIONS_MANUAL_PATH.exists():
        return ""
    return OPERATIONS_MANUAL_PATH.read_text(encoding="utf-8")


def parse_manual_sections() -> list[dict[str, str]]:
    text = read_operations_manual()
    if not text:
        return []

    sections: list[dict[str, str]] = []
    current_title: str | None = None
    current_lines: list[str] = []

    for line in text.splitlines():
        if line.startswith("## "):
            if current_title:
                body = "\n".join(current_lines).strip()
                sections.append(
                    {
                        "title": current_title,
                        "body": body,
                        "summary": summarize_section(body),
                    }
                )
            current_title = line[3:].strip()
            current_lines = []
            continue
        current_lines.append(line)

    if current_title:
        body = "\n".join(current_lines).strip()
        sections.append(
            {
                "title": current_title,
                "body": body,
                "summary": summarize_section(body),
            }
        )

    return sections


def summarize_section(body: str) -> str:
    bullets = []
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            bullets.append(stripped[2:])
        elif stripped:
            bullets.append(stripped)
        if len(bullets) >= 2:
            break
    return " ".join(bullets[:2])


def section_map() -> dict[str, dict[str, str]]:
    return {section["title"]: section for section in parse_manual_sections()}


def manual_bundle(section_titles: list[str]) -> list[dict[str, str]]:
    sections = section_map()
    return [sections[title] for title in section_titles if title in sections]


def list_course_sources() -> list[dict[str, str]]:
    sources: list[dict[str, str]] = []
    if not COURSE_CORPUS_ROOT.exists():
        return sources

    for path in sorted(COURSE_CORPUS_ROOT.glob("*.txt")):
        stem = path.stem
        if "：" in stem:
            source_type, title = stem.split("：", 1)
        else:
            source_type, title = "课程文本", stem

        sources.append(
            {
                "filename": path.name,
                "source_type": source_type,
                "title": title,
                "path": str(path),
            }
        )

    return sources


def unique_course_titles() -> list[str]:
    titles = []
    seen = set()
    for source in list_course_sources():
        title = source["title"]
        if title in seen:
            continue
        seen.add(title)
        titles.append(title)
    return titles
