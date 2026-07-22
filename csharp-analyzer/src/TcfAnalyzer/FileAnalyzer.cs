using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;

namespace TcfAnalyzer;

/// <summary>Analyzes a single C# syntax tree against the shared compilation.</summary>
public static class FileAnalyzer
{
    public static FileResult Analyze(CSharpCompilation compilation, SyntaxTree tree, string path, string prefix, HashSet<ISymbol> usedSymbols)
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

        var unusedDefinitions = new List<UnusedDefinition>();
        foreach (var node in root.DescendantNodes())
        {
            var declaredSymbol = model.GetDeclaredSymbol(node);
            if (declaredSymbol == null) continue;

            if (declaredSymbol.IsImplicitlyDeclared || declaredSymbol.IsOverride) continue;
            if (declaredSymbol.Name == "Main") continue;
            if (declaredSymbol is IMethodSymbol) continue; // Methods are handled separately

            if (!usedSymbols.Contains(declaredSymbol.OriginalDefinition))
            {
                var typeStr = declaredSymbol switch
                {
                    IFieldSymbol f when f.IsConst => "Constant",
                    IFieldSymbol f when f.ContainingType?.TypeKind == TypeKind.Enum => "Enum Member",
                    IFieldSymbol => "Field",
                    IPropertySymbol => "Property",
                    ILocalSymbol => "Variable",
                    INamedTypeSymbol n when n.TypeKind == TypeKind.Enum => "Enum",
                    INamedTypeSymbol n when n.TypeKind == TypeKind.Class => "Class",
                    INamedTypeSymbol n when n.TypeKind == TypeKind.Struct => "Struct",
                    INamedTypeSymbol n when n.TypeKind == TypeKind.Interface => "Interface",
                    IEventSymbol => "Event",
                    _ => null
                };

                if (typeStr != null)
                {
                    var lineSpan = tree.GetLineSpan(node.Span);
                    unusedDefinitions.Add(new UnusedDefinition(declaredSymbol.Name, typeStr, lineSpan.StartLinePosition.Line + 1));
                }
            }
        }

        return new FileResult(path, true, new Diagnostics(errorCount > 0, errorCount), comments, methods, unusedDefinitions);
    }
}
