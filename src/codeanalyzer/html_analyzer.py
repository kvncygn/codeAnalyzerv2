from __future__ import annotations

import re
from pathlib import Path

from .models import HtmlTestReport, HtmlVirtualFolder, HtmlAnalysisResult

_TOTAL_RE = re.compile(r"<th>\s*Number of Total Steps\s*</th>\s*<td>\s*<b>\s*(\d+)\s*</b>\s*</td>", re.IGNORECASE)
_PASSED_RE = re.compile(r"<th>\s*Number of Passed Steps\s*</th>\s*<td>\s*<b>\s*(\d+)\s*</b>\s*</td>", re.IGNORECASE)
_FAILED_RE = re.compile(r"<th>\s*Number of Failed Steps\s*</th>\s*<td>\s*<b>\s*(\d+)\s*</b>\s*</td>", re.IGNORECASE)
_NA_RE = re.compile(r"<th>\s*Number of N/A Steps\s*</th>\s*<td>\s*<b>\s*(\d+)\s*</b>\s*</td>", re.IGNORECASE)
_FAILED_STEP_RE = re.compile(r'<tr>\s*<td[^>]*>\s*(\d+)\s*</td>(?:(?!<tr>).)*?<td class="error">\s*FAILED\s*</td>', re.DOTALL | re.IGNORECASE)


def extract_metric(pattern: re.Pattern[str], text: str) -> int:
    match = pattern.search(text)
    if match:
        try:
            return int(match.group(1))
        except ValueError:
            return 0
    return 0


def analyze_html_reports(folder: Path) -> HtmlAnalysisResult:
    """Scan the given folder for .html files and group them into virtual folders."""
    all_reports: list[HtmlTestReport] = []
    
    for file_path in folder.rglob("*.html"):
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            
            total = extract_metric(_TOTAL_RE, content)
            passed = extract_metric(_PASSED_RE, content)
            failed = extract_metric(_FAILED_RE, content)
            na = extract_metric(_NA_RE, content)
            
            failed_step_ids: tuple[int, ...] = ()
            if failed > 0:
                matches = _FAILED_STEP_RE.findall(content)
                try:
                    failed_step_ids = tuple(int(x) for x in matches)
                except ValueError:
                    pass
            
            all_reports.append(
                HtmlTestReport(
                    file_name=file_path.name,
                    total_steps=total,
                    passed_steps=passed,
                    failed_steps=failed,
                    na_steps=na,
                    failed_step_ids=failed_step_ids
                )
            )
        except Exception:
            continue
            
    # Grouping logic
    # Find prefixes like TCF_..._RC1
    prefix_map: dict[str, list[HtmlTestReport]] = {}
    single_files: list[HtmlTestReport] = []
    
    for report in all_reports:
        name = report.file_name
        if name.startswith("TCF") and "RC1" in name:
            idx = name.find("RC1")
            prefix = name[:idx + 3] # Include "RC1"
            prefix_map.setdefault(prefix, []).append(report)
        else:
            single_files.append(report)
            
    virtual_folders: list[HtmlVirtualFolder] = []
    
    for prefix, reports in prefix_map.items():
        if len(reports) >= 2:
            virtual_folders.append(
                HtmlVirtualFolder(
                    name=prefix,
                    reports=sorted(reports, key=lambda r: r.file_name)
                )
            )
        else:
            # If only 1 file, it doesn't get a virtual folder
            single_files.extend(reports)
            
    return HtmlAnalysisResult(
        folder=str(folder),
        virtual_folders=sorted(virtual_folders, key=lambda v: v.name),
        single_files=sorted(single_files, key=lambda r: r.file_name)
    )
