from __future__ import annotations

import re
from pathlib import Path

from .models import HtmlTestReport, HtmlSubFolder, HtmlVirtualFolder, HtmlAnalysisResult

_TOTAL_RE = re.compile(r"<th>\s*Number of Total Steps\s*</th>\s*<td>\s*(?:<[^>]+>)*\s*(\d+)\s*(?:</[^>]+>)*\s*</td>", re.IGNORECASE)
_PASSED_RE = re.compile(r"<th>\s*Number of Passed Steps\s*</th>\s*<td>\s*(?:<[^>]+>)*\s*(\d+)\s*(?:</[^>]+>)*\s*</td>", re.IGNORECASE)
_FAILED_RE = re.compile(r"<th>\s*Number of Failed Steps\s*</th>\s*<td>\s*(?:<[^>]+>)*\s*(\d+)\s*(?:</[^>]+>)*\s*</td>", re.IGNORECASE)
_NA_RE = re.compile(r"<th>\s*Number of N/A Steps\s*</th>\s*<td>\s*(?:<[^>]+>)*\s*(\d+)\s*(?:</[^>]+>)*\s*</td>", re.IGNORECASE)
_IDX_TOTAL_RE = re.compile(r"<th>\s*NR TOTAL TEST CASES\s*</th>\s*<td>\s*(?:<[^>]+>)*\s*(\d+)\s*(?:</[^>]+>)*\s*</td>", re.IGNORECASE)
_IDX_PASSED_RE = re.compile(r"<th>\s*NR PASSED TEST CASES\s*</th>\s*<td>\s*(?:<[^>]+>)*\s*(\d+)(.*?)\s*(?:</[^>]+>)*\s*</td>", re.IGNORECASE)
_IDX_FAILED_RE = re.compile(r"<th>\s*NR FAILED TEST CASES\s*</th>\s*<td>\s*(?:<[^>]+>)*\s*(\d+)(.*?)\s*(?:</[^>]+>)*\s*</td>", re.IGNORECASE)
_FAILED_STEP_RE = re.compile(r'<tr>\s*<td[^>]*>\s*(\d+)\s*</td>(?:(?!<tr>).)*?<td class="error">\s*FAILED\s*</td>', re.DOTALL | re.IGNORECASE)
_FAILED_INC_RE = re.compile(r'<td[^>]*>(?:(?!</td>).)*?FAILED\s*\(?\s*INCOMPLETE\s*\)?(?:(?!</td>).)*?</td>', re.IGNORECASE | re.DOTALL)


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
    all_reports: list[tuple[HtmlTestReport, str, str]] = []
    index_report = None
    TAGS = ["SCN", "SCA_WINDOWS", "MANUAL", "SCA_MANUAL"]
    
    for file_path in folder.rglob("*.html"):
        name = file_path.name
        
        # Only process index.html and files starting with TC
        if name.lower() != "index.html" and not name.startswith("TC"):
            continue
            
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            
            if name.lower() == "index.html":
                m_total = _IDX_TOTAL_RE.search(content)
                total = int(m_total.group(1)) if m_total else 0
                
                m_passed = _IDX_PASSED_RE.search(content)
                passed = int(m_passed.group(1)) if m_passed else 0
                passed_pct = m_passed.group(2).strip() if m_passed else ""
                
                m_failed = _IDX_FAILED_RE.search(content)
                failed = int(m_failed.group(1)) if m_failed else 0
                failed_pct = m_failed.group(2).strip() if m_failed else ""
                
                na = 0
                failed_inc = 0
            else:
                total = extract_metric(_TOTAL_RE, content)
                passed = extract_metric(_PASSED_RE, content)
                failed = extract_metric(_FAILED_RE, content)
                na = extract_metric(_NA_RE, content)
                failed_inc = len(_FAILED_INC_RE.findall(content))
                passed_pct = ""
                failed_pct = ""
            
            failed_step_ids: tuple[int, ...] = ()
            if failed > 0:
                matches = _FAILED_STEP_RE.findall(content)
                try:
                    failed_step_ids = tuple(int(x) for x in matches)
                except ValueError:
                    pass
            
            report = HtmlTestReport(
                file_name=name,
                absolute_path=str(file_path.absolute()),
                total_steps=total,
                passed_steps=passed,
                failed_steps=failed,
                na_steps=na,
                failed_incomplete_steps=failed_inc,
                failed_step_ids=failed_step_ids,
                passed_pct=passed_pct,
                failed_pct=failed_pct
            )
            
            if name.lower() == "index.html":
                index_report = report
            else:
                # Find the first occurring tag
                tag_positions = {}
                for tag in TAGS:
                    idx = name.find(tag)
                    if idx != -1:
                        tag_positions[tag] = idx
                if not tag_positions:
                    continue
                first_tag = min(tag_positions.keys(), key=lambda k: tag_positions[k])
                
                # Extract TCF...RC1 base folder name
                idx_tcf = name.find("TCF")
                idx_rc1 = name.find("RC1")
                if idx_tcf != -1 and idx_rc1 != -1 and idx_rc1 > idx_tcf:
                    base_folder = name[idx_tcf:idx_rc1 + 3]
                    all_reports.append((report, base_folder, first_tag))
                
        except Exception:
            continue
            
    # Grouping logic
    # folders_map[base_folder][tag] = [reports...]
    folders_map: dict[str, dict[str, list[HtmlTestReport]]] = {}
    
    for report, base_folder, tag in all_reports:
        if base_folder not in folders_map:
            folders_map[base_folder] = {t: [] for t in TAGS}
        folders_map[base_folder][tag].append(report)
        
    virtual_folders: list[HtmlVirtualFolder] = []
    
    for bf_name, tag_map in folders_map.items():
        subfolders = []
        # Create subfolders for all tags even if empty, as requested
        for tag in TAGS:
            sorted_reports = sorted(tag_map[tag], key=lambda r: r.file_name)
            display_name = "WINDOWS" if tag == "SCN" else tag
            subfolders.append(HtmlSubFolder(name=display_name, reports=sorted_reports))
        virtual_folders.append(HtmlVirtualFolder(name=bf_name, subfolders=subfolders))
            
    return HtmlAnalysisResult(
        folder=str(folder),
        virtual_folders=sorted(virtual_folders, key=lambda v: v.name),
        index_report=index_report
    )
