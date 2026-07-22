# Requirements

## Project

Build a local-only static code analyzer application.

The application runs on localhost and analyzes source code files under a folder selected by the user.

The application must not send source code or analysis data outside the local machine.

## Core Goal

The user provides a folder path.

The analyzer recursively scans supported source files under that folder and produces static analysis reports.

Supported file extensions:

```text
.cs
.c
.h
.cpp
.hpp
.cc
.cxx
.hh
```

## Local-Only Constraints

The application must not:

```text
make internet requests
send source code outside the machine
use cloud or AI APIs
use telemetry
use remote logging
```

All analysis must happen locally.

## Platform and Delivery

The application targets Windows and is delivered as a single local executable.

The local-only constraints above apply to every component, including any bundled
analysis engine. No component may make network requests at runtime.

## UI Requirements

The application must have a localhost UI.

The UI must allow the user to:

```text
enter a folder path
enter or change the TCF prefix
start analysis
view results
```

Default TCF prefix:

```text
TCF
```

The folder path is the analysis target.

The TCF prefix is an analysis configuration value.

## C# Analysis

For C# files, analyze methods whose names start with the configured TCF prefix.

For each TCF method, extract:

```text
method name
file path
start line
end line
total line count
code line count
comment line count
inline comment line count
blank line count
comment ratio
cyclomatic complexity
used helper functions
```

## Helper Function Rules

Helper functions are determined automatically by semantic analysis. They are not
inferred from naming conventions and are not manually configured.

A helper function is:

```text
a C# method
defined in a file under the analyzed folder
whose name does NOT start with the TCF prefix (non-TCF)
called by at least one TCF method
```

Call targets are resolved semantically (by the C# compiler engine), so a project method
is correctly distinguished from a same-named library method
(for example a project Add() versus List<T>.Add()).

The analyzer must not:

```text
infer helpers from names (a method or file containing "helper" means nothing)
treat every non-TCF method as a helper (only those called by an TCF method)
treat library or framework calls as helpers
```

A non-TCF method that no TCF method calls is not a helper.

## TCF Call Rules

Do not analyze TCF-to-TCF calls as a separate report category.

The reports must not include:

```text
TCF calls
TCF-to-TCF dependency edges
```

If an TCF method calls another TCF method, do not report it as a separate dependency category.

## C/C++ Analysis

C and C++ files do not use TCF logic.

C and C++ files do not use helper logic.

For C/C++ files, only file-level metrics are required:

```text
file path
file type
total line count
code line count
comment line count
inline comment line count
blank line count
```

For C/C++ files:

```text
TCF method count = 0
helper method count = 0
```

## Line Counting Rules

Line counting must follow these rules exactly.

Blank line:

```text
blank_lines +1
```

Code-only line:

```text
code_lines +1
```

Comment-only line:

```text
comment_lines +1
```

Code line with inline comment:

```text
code_lines +1
comment_lines +1
inline_comment_lines +1
```

Example:

```csharp
int x = 5; // comment
```

This line counts as both code and comment.

It must increment:

```text
code_lines
comment_lines
inline_comment_lines
```

## Project Summary

At the beginning of the result, show a project summary containing:

```text
total source file count
total line count
total code line count
total comment line count
total inline comment line count
total blank line count
total C# file count
total C# method count
total TCF method count
total helper method count
```

## File Summary

For every analyzed file, show:

```text
file path
file type
total lines
code lines
comment lines
inline comment lines
blank lines
TCF method count
helper method count
```

For C/C++ files, TCF and helper counts must be zero.

## Source Tree

Before TCF method details, show a source tree.

The tree must show each analyzed file and the TCF methods under that file.

Example format:

```text
[ROOT]
+-- Program.cs (500 lines, TCF=5, Helpers=0)
    +-- TCF_Init
    +-- TCF_Process
+-- HelperFunctions.cs (120 lines, TCF=0, Helpers=8)
+-- utils.c (80 lines, TCF=0, Helpers=0)
```

## Output Order

The analysis result must be shown in this exact order:

```text
1. Project Summary
2. File Summary
3. Source Tree
4. TCF Method Details
5. Helper Usage Summary
```

## Helper Usage Summary

Show which helper functions are used by TCF methods.

For each helper, list the TCF methods that call it.

## Error Handling

The application must not crash in these cases:

```text
invalid folder path
empty folder
no supported source files found
file encoding errors
source files with syntax errors
```

The user must see understandable error or warning messages.

Syntax errors in one file must not stop the whole analysis if other files can still be analyzed.

Encoding errors in one file must not crash the application.

## Important Behavior Rules

Do not add unsupported file types unless explicitly requested.

Do not add cloud-based analysis.

Do not add AI-based code analysis.

Do not add telemetry.

Do not treat every non-TCF method as a helper (only methods an TCF method calls).

Do not treat file or method names containing "helper" as helper indicators.

Do not report TCF-to-TCF dependency edges.

Do not require source code to be uploaded anywhere.

## Expected Development Approach

Implement the application according to the requirements above.

When a requirement is ambiguous, prefer the stricter and more conservative interpretation.

Do not introduce extra features that change the scope of the analyzer unless explicitly requested.

The final application should be usable from a localhost UI and should analyze a user-selected local folder according to these rules.

