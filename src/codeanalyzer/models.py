"""Typed result model produced by the orchestrator and consumed by the report layer."""

from __future__ import annotations

from dataclasses import dataclass, field

from .filetypes import Language
from .line_metrics import LineCounts


@dataclass(frozen=True)
class HelperRef:
    """A helper function identified by its simple name and defining file (relative)."""

    name: str
    file: str


@dataclass(frozen=True)
class UnusedMethod:
    """A non-TCF method that is not called by any TCF method."""

    name: str
    file: str
    start_line: int
    end_line: int
    cyclomatic_complexity: int
    time_complexity: str
    tc_line: int


@dataclass(frozen=True)
class UnusedDefinition:
    """An unused variable, enum, constant, class, property, or field."""

    name: str
    type: str
    line: int
    file: str


@dataclass(frozen=True)
class TcfMethod:
    """Full per-method report for one TCF method. Line numbers are 1-based for display."""

    name: str
    file: str
    start_line: int
    end_line: int
    counts: LineCounts
    cyclomatic_complexity: int
    time_complexity: str
    tc_line: int
    used_helpers: tuple[HelperRef, ...]


@dataclass(frozen=True)
class DevMethod:
    """Method data specifically for Developer Analysis (shows all methods)."""
    name: str
    file: str
    start_line: int
    end_line: int
    cyclomatic_complexity: int
    time_complexity: str
    tc_line: int


@dataclass(frozen=True)
class FileReport:
    """Per-file summary row."""

    rel_path: str
    file_type: str
    language: Language
    counts: LineCounts
    tcf_method_count: int
    helper_method_count: int
    tcf_method_names: tuple[str, ...]


@dataclass(frozen=True)
class HelperUsage:
    """A helper and the sorted names of the TCF methods that call it."""

    helper: HelperRef
    callers: tuple[str, ...]
    helper_callers: tuple[str, ...] = ()


@dataclass(frozen=True)
class ProjectSummary:
    file_count: int
    counts: LineCounts
    csharp_file_count: int
    csharp_method_count: int
    tcf_method_count: int
    helper_method_count: int
    unused_method_count: int
    unused_definition_count: int


@dataclass(frozen=True)
class AnalysisResult:
    """The complete analysis, ready for rendering in the required output order."""

    folder: str
    summary: ProjectSummary
    files: tuple[FileReport, ...]
    tcf_methods: tuple[TcfMethod, ...]
    helper_usage: tuple[HelperUsage, ...]
    unused_methods: tuple[UnusedMethod, ...]
    unused_definitions: tuple[UnusedDefinition, ...]
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class DevAnalysisResult:
    """The complete result of a Dev Analysis (C/C++) run."""
    folder: str
    methods: tuple[DevMethod, ...]


@dataclass(frozen=True)
class HtmlTestReport:
    """Represents a parsed HTML test report file and its metrics."""
    file_name: str
    absolute_path: str
    total_steps: int
    passed_steps: int
    failed_steps: int
    na_steps: int
    failed_incomplete_steps: int = 0
    failed_step_ids: tuple[int, ...] = field(default_factory=tuple)
    passed_pct: str = ""
    failed_pct: str = ""


@dataclass(frozen=True)
class HtmlSubFolder:
    """A sub-folder categorization based on specific tags."""
    name: str
    reports: list[HtmlTestReport]

    @property
    def total_steps(self) -> int:
        return sum(r.total_steps for r in self.reports)

    @property
    def passed_steps(self) -> int:
        return sum(r.passed_steps for r in self.reports)

    @property
    def failed_steps(self) -> int:
        return sum(r.failed_steps for r in self.reports)

    @property
    def na_steps(self) -> int:
        return sum(r.na_steps for r in self.reports)

    @property
    def failed_incomplete_steps(self) -> int:
        return sum(r.failed_incomplete_steps for r in self.reports)


@dataclass(frozen=True)
class HtmlVirtualFolder:
    """A virtual grouping of HTML test reports based on their common prefix."""
    name: str
    subfolders: list[HtmlSubFolder]

    @property
    def total_steps(self) -> int:
        return sum(s.total_steps for s in self.subfolders)

    @property
    def passed_steps(self) -> int:
        return sum(s.passed_steps for s in self.subfolders)

    @property
    def failed_steps(self) -> int:
        return sum(s.failed_steps for s in self.subfolders)

    @property
    def na_steps(self) -> int:
        return sum(s.na_steps for s in self.subfolders)

    @property
    def failed_incomplete_steps(self) -> int:
        return sum(s.failed_incomplete_steps for s in self.subfolders)


@dataclass(frozen=True)
class HtmlAnalysisResult:
    """The result of the HTML test report analysis."""
    folder: str
    virtual_folders: list[HtmlVirtualFolder]
    index_report: HtmlTestReport | None = None

    @property
    def total_steps(self) -> int:
        return sum(vf.total_steps for vf in self.virtual_folders)

    @property
    def passed_steps(self) -> int:
        return sum(vf.passed_steps for vf in self.virtual_folders)

    @property
    def failed_steps(self) -> int:
        return sum(vf.failed_steps for vf in self.virtual_folders)

    @property
    def na_steps(self) -> int:
        return sum(vf.na_steps for vf in self.virtual_folders)

    @property
    def failed_incomplete_steps(self) -> int:
        return sum(vf.failed_incomplete_steps for vf in self.virtual_folders)
