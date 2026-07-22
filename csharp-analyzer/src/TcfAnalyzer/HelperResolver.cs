using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp.Syntax;

namespace TcfAnalyzer;

/// <summary>
/// Resolves the helper functions an TCF method calls. A helper is a source-defined,
/// non-TCF, ordinary method (resolved semantically). Library/unresolved calls and
/// TCF-to-TCF calls are ignored.
/// </summary>
public static class HelperResolver
{
    public static List<HelperRef> Resolve(SemanticModel model, MethodDeclarationSyntax method, string prefix)
    {
        var found = new Dictionary<(string Name, string File), HelperRef>();

        foreach (var invocation in method.DescendantNodes().OfType<InvocationExpressionSyntax>())
        {
            var info = model.GetSymbolInfo(invocation);

            // Symbol is null when overload resolution fails -- which happens for otherwise
            // valid calls whenever an *argument* expression doesn't fully bind (e.g. string
            // concatenation "a" + b, or x.ToString(), under the ad-hoc compilation). The
            // intended target is still reported in CandidateSymbols. We only need to know
            // *which* method is invoked, not whether its arguments type-check, so fall back
            // to the candidates. The in-source / ordinary / non-TCF filters below keep this
            // safe: library or TCF candidates are still excluded.
            var candidates = info.Symbol is not null
                ? new[] { info.Symbol }
                : info.CandidateSymbols.ToArray();

            foreach (var candidate in candidates)
            {
                if (candidate is not IMethodSymbol symbol)
                    continue; // not a method -> ignore

                var def = symbol.OriginalDefinition;

                if (def.MethodKind != MethodKind.Ordinary)
                    continue; // constructor / accessor / operator -> not a helper

                var sourceLocation = def.Locations.FirstOrDefault(l => l.IsInSource);
                if (sourceLocation is null)
                    continue; // metadata (BCL / third-party) -> library, ignore

                if (def.Name.StartsWith(prefix, StringComparison.Ordinal))
                    continue; // TCF-to-TCF -> ignore

                var file = sourceLocation.SourceTree?.FilePath ?? string.Empty;
                found.TryAdd((def.Name, file), new HelperRef(def.Name, file));
            }
        }

        return found.Values
            .OrderBy(h => h.Name, StringComparer.Ordinal)
            .ThenBy(h => h.File, StringComparer.Ordinal)
            .ToList();
    }
}
