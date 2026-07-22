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

        var results = new List<FileResult>(parsed.Count);
        foreach (var (file, tree) in parsed)
        {
            try
            {
                results.Add(FileAnalyzer.Analyze(compilation, tree, file.Path, prefix));
            }
            catch (Exception ex)
            {
                Console.Error.WriteLine($"[analyzer] error analyzing {file.Path}: {ex.Message}");
                results.Add(new FileResult(
                    file.Path, false, new Diagnostics(true, 1),
                    new List<CommentSpan>(), new List<MethodResult>()));
            }
        }

        return new AnalyzeResponse(results);
    }
}
