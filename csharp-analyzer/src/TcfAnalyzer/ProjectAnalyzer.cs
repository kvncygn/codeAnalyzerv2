using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;

namespace TcfAnalyzer;

/// <summary>
/// Builds one ad-hoc compilation from the request's files + BCL references, then analyzes
/// each file. A failure on one file never aborts the others.
/// </summary>
public static class ProjectAnalyzer
{
    public static AnalyzeResponse Analyze(AnalyzeRequest request)
    {
        var prefix = request.TcfPrefix ?? string.Empty;

        var parsed = new List<(RequestFile File, SyntaxTree Tree)>();
        foreach (var file in request.Files ?? new List<RequestFile>())
        {
            // ParseText never throws on syntax errors; it produces a tree with error nodes.
            var tree = CSharpSyntaxTree.ParseText(file.Text ?? string.Empty, path: file.Path);
            parsed.Add((file, tree));
        }

        var compilation = CSharpCompilation.Create(
            assemblyName: "analysis",
            syntaxTrees: parsed.Select(p => p.Tree),
            references: ReferenceLoader.BclReferences(),
            options: new CSharpCompilationOptions(OutputKind.DynamicallyLinkedLibrary));

        var usedSymbols = new HashSet<ISymbol>(SymbolEqualityComparer.Default);
        foreach (var (file, tree) in parsed)
        {
            var model = compilation.GetSemanticModel(tree);
            var root = tree.GetCompilationUnitRoot();
            foreach (var node in root.DescendantNodes())
            {
                var symbolInfo = model.GetSymbolInfo(node);
                var candidates = symbolInfo.Symbol != null
                    ? new[] { symbolInfo.Symbol }
                    : symbolInfo.CandidateSymbols.ToArray();

                foreach (var sym in candidates)
                {
                    usedSymbols.Add(sym.OriginalDefinition);
                    if (sym.ContainingType != null)
                    {
                        usedSymbols.Add(sym.ContainingType.OriginalDefinition);
                    }
                }

                var declaredSymbol = model.GetDeclaredSymbol(node);
                if (declaredSymbol is INamedTypeSymbol namedType)
                {
                    if (namedType.BaseType != null) usedSymbols.Add(namedType.BaseType.OriginalDefinition);
                    foreach (var iface in namedType.Interfaces) usedSymbols.Add(iface.OriginalDefinition);
                }
            }
        }

        var results = new List<FileResult>(parsed.Count);
        foreach (var (file, tree) in parsed)
        {
            try
            {
                results.Add(FileAnalyzer.Analyze(compilation, tree, file.Path, prefix, usedSymbols));
            }
            catch (Exception ex)
            {
                Console.Error.WriteLine($"[analyzer] error analyzing {file.Path}: {ex.Message}");
                results.Add(new FileResult(
                    file.Path, false, new Diagnostics(true, 1),
                    new List<CommentSpan>(), new List<MethodResult>(), new List<UnusedDefinition>()));
            }
        }

        return new AnalyzeResponse(results);
    }
}
