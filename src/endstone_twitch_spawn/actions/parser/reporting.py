from pathlib import Path

from rich.text import Text
from rich.console import Console

from ..models import Issue, Severity
from endstone import Logger, ColorFormat


def _source_line(file: Path, line_no: int) -> str | None:
    try:
        lines = file.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return None
    if 1 <= line_no <= len(lines):
        return lines[line_no - 1]
    return None


def format_issue(issue: Issue) -> Text:
    is_error = issue.severity == Severity.ERROR
    sev_style = "bold red" if is_error else "bold yellow"
    label = "error" if is_error else "warning"
    blue_bold = "bold blue"
    bold = "bold"

    header_code = f"[{issue.code}]" if issue.code else ""
    title = issue.name or label

    text = Text()
    text.append(f"{label}{header_code}", style=sev_style)
    text.append(f": {title}\n", style=bold)

    text.append(" --> ", style=blue_bold)
    text.append(f"workflows/{issue.file.name}:{issue.source_line}\n")

    gutter_w = len(str(issue.source_line))
    pad = " " * gutter_w

    src = _source_line(issue.file, issue.source_line)

    if src is not None:
        stripped = src.rstrip("\n")
        text.append(f"{issue.source_line} | ", style=blue_bold)
        text.append(f"{stripped}\n")

        underline_len = max(len(stripped.strip()), 1)
        leading_ws = len(stripped) - len(stripped.lstrip())
        caret = "^" * underline_len

        text.append(f"{pad} | ", style=blue_bold)
        text.append(" " * leading_ws)
        text.append(caret, style=sev_style)
        if issue.help:
            text.append(f" {issue.help}")
        text.append("\n")
    else:
        text.append(f"{pad} | ", style=blue_bold)
        text.append("^", style=sev_style)
        text.append(" (source unavailable)")
        if issue.help:
            text.append(f" — {issue.help}")
        text.append("\n")

    return text


def _render(text: Text) -> str:
    """Render Text to a plain-16-color ANSI string, independent of the
    destination stream (which is usually not a real tty)."""
    console = Console(
        force_terminal=True,
        color_system="standard",
        no_color=False,
        width=120,
        soft_wrap=True,
    )
    with console.capture() as capture:
        console.print(text, end="")
    return capture.get()


def print_issues(issues: list[Issue], logger: Logger) -> None:
    """
    Log each issue through the logger method matching its own severity,
    so a warning never gets painted red just because some other issue in
    the batch was an error.
    """
    if not issues:
        return

    for issue in issues:
        rendered = _render(format_issue(issue))
        if issue.severity == Severity.ERROR:
            logger.error(rendered)
        else:
            logger.warning(rendered)

    errors = sum(1 for i in issues if i.severity == Severity.ERROR)
    warnings = sum(1 for i in issues if i.severity == Severity.WARNING)
    parts = []
    if errors:
        parts.append(f"{errors} error{'s' if errors != 1 else ''}")
    if warnings:
        parts.append(f"{warnings} warning{'s' if warnings != 1 else ''}")

    summary = _render(Text(f"{', '.join(parts)} emitted", style="bold"))
    if errors:
        logger.error(summary)
    else:
        logger.warning(summary)


def format_issue_mc(issue: Issue) -> str:
    is_error = issue.severity == Severity.ERROR
    sev_color = ColorFormat.RED if is_error else ColorFormat.YELLOW
    label = "Error" if is_error else "Warning"

    header_code = f"[{issue.code}] " if issue.code else ""
    title = issue.name or label

    lines = []
    lines.append(
        f"{sev_color}{ColorFormat.BOLD}{label} {header_code}{ColorFormat.RESET}"
        f"{ColorFormat.BOLD}{title}{ColorFormat.RESET}"
    )
    lines.append(
        f"{ColorFormat.GRAY}in {ColorFormat.RESET}{ColorFormat.BOLD}"
        f"workflows/{issue.file.name}{ColorFormat.RESET}"
        f"{ColorFormat.GRAY}, line {issue.source_line}{ColorFormat.RESET}"
    )

    src = _source_line(issue.file, issue.source_line)
    if src is not None:
        stripped = src.strip()
        lines.append(f"  {ColorFormat.ITALIC}\u201c{stripped}\u201d{ColorFormat.RESET}")

    if issue.help:
        lines.append(f"  {sev_color}-> {ColorFormat.RESET}{issue.help}")

    return "\n".join(lines)


def format_issues_mc(issues: list[Issue]) -> str:
    """
    Same content as print_issues_mc, but returns a single formatted
    string instead of logging — caller decides what to do with it.
    """
    if not issues:
        return ""

    blocks = [format_issue_mc(issue) for issue in issues]

    errors = sum(1 for i in issues if i.severity == Severity.ERROR)
    warnings = sum(1 for i in issues if i.severity == Severity.WARNING)
    parts = []
    if errors:
        parts.append(f"{errors} error{'s' if errors != 1 else ''}")
    if warnings:
        parts.append(f"{warnings} warning{'s' if warnings != 1 else ''}")

    summary = f"{ColorFormat.BOLD}{', '.join(parts)} emitted{ColorFormat.RESET}"
    blocks.append(summary)

    return "\n\n".join(blocks)
