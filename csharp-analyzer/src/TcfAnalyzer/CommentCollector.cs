using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;

namespace TcfAnalyzer;

/// <summary>
/// Collects comment trivia spans (line, block, and documentation comments) so the Python
/// side can apply the exact line-counting rules. Comment markers inside string/char
/// literals are not trivia, so they are correctly excluded.
/// </summary>
public static class CommentCollector
{
    public static List<CommentSpan> Collect(SyntaxNode root)
    {
        var spans = new List<CommentSpan>();
        foreach (var trivia in root.DescendantTrivia())
        {
            switch (trivia.Kind())
            {
                case SyntaxKind.SingleLineCommentTrivia:
                case SyntaxKind.MultiLineCommentTrivia:
                case SyntaxKind.SingleLineDocumentationCommentTrivia:
                case SyntaxKind.MultiLineDocumentationCommentTrivia:
                    var span = trivia.GetLocation().GetLineSpan();
                    spans.Add(new CommentSpan(
                        span.StartLinePosition.Line, span.StartLinePosition.Character,
                        span.EndLinePosition.Line, span.EndLinePosition.Character));
                    break;
            }
        }
        return spans;
    }
}
