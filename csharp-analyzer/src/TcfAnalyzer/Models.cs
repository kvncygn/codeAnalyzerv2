namespace TcfAnalyzer;

// ---- Request (read from stdin) ----

/// <summary>The analysis request: the TCF prefix and the decoded C# source files.</summary>
public sealed record AnalyzeRequest(string TcfPrefix, List<RequestFile> Files);

/// <summary>One C# file: absolute path + already-decoded text (Python owns encoding).</summary>
public sealed record RequestFile(string Path, string Text);

// ---- Response (written to stdout) ----

public sealed record AnalyzeResponse(List<FileResult> Files);

public sealed record FileResult(
    string Path,
    bool Ok,
    Diagnostics Diagnostics,
    List<CommentSpan> Comments,
    List<MethodResult> Methods,
    List<UnusedDefinition> UnusedDefinitions);

public sealed record Diagnostics(bool HasErrors, int ErrorCount);

/// <summary>0-based line, 0-based character (UTF-16 code unit) coordinates, end exclusive.</summary>
public sealed record CommentSpan(int StartLine, int StartCol, int EndLine, int EndCol);

public sealed record MethodResult(
    string Name,
    bool IsTcf,
    int StartLine,
    int EndLine,
    int CyclomaticComplexity,
    string TimeComplexity,
    int TimeComplexityLine,
    List<HelperRef> UsedHelpers);

/// <summary>A helper used by an TCF method: its simple name and defining file.</summary>
public sealed record HelperRef(string Name, string File);

/// <summary>An unused variable, enum, constant, class, property, or field.</summary>
public sealed record UnusedDefinition(string Name, string Type, int Line);
