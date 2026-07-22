using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;

namespace TcfAnalyzer;

/// <summary>Analyzes a single C# syntax tree against the shared compilation.</summary>
public static class FileAnalyzer
{
    public static FileResult Analyze(CSharpCompilation compilation, SyntaxTree tree, string path, string prefix)
    {
        var root = tree.GetCompilationUnitRoot();
        var model = compilation.GetSemanticModel(tree);

        var errorCount = tree.GetDiagnostics().Count(d => d.Severity == DiagnosticSeverity.Error);
        var comments = CommentCollector.Collect(root);

        var methods = new List<MethodResult>();
        foreach (var decl in root.DescendantNodes().OfType<MethodDeclarationSyntax>())
        {
            var name = decl.Identifier.ValueText;
            var isTcf = name.StartsWith(prefix, StringComparison.Ordinal);
            var lineSpan = tree.GetLineSpan(decl.Span);
            var helpers = isTcf
                ? HelperResolver.Resolve(model, decl, prefix)
                : new List<HelperRef>();

            methods.Add(new MethodResult(
                name,
                isTcf,
                lineSpan.StartLinePosition.Line,
                lineSpan.EndLinePosition.Line,
                ComplexityCalculator.Compute(decl),
                helpers));
        }

        return new FileResult(path, true, new Diagnostics(errorCount > 0, errorCount), comments, methods);
    }
}
