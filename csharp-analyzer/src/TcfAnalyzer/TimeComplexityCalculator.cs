using System;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;

namespace TcfAnalyzer;

public static class TimeComplexityCalculator
{
    public sealed record TimeComplexityResult(string Complexity, int LineNumber);

    public static TimeComplexityResult Compute(MethodDeclarationSyntax method)
    {
        int maxDepth = 0;
        int maxDepthLine = 0;

        void Visit(SyntaxNode node, int currentDepth)
        {
            int nextDepth = currentDepth;
            bool isLoop = node is ForStatementSyntax || 
                          node is ForEachStatementSyntax || 
                          node is WhileStatementSyntax || 
                          node is DoStatementSyntax;

            if (isLoop)
            {
                nextDepth++;
                if (nextDepth > maxDepth)
                {
                    maxDepth = nextDepth;
                    maxDepthLine = node.GetLocation().GetLineSpan().StartLinePosition.Line + 1; // 1-indexed
                }
            }

            foreach (var child in node.ChildNodes())
            {
                Visit(child, nextDepth);
            }
        }

        if (method.Body != null)
        {
            Visit(method.Body, 0);
        }
        else if (method.ExpressionBody != null)
        {
            Visit(method.ExpressionBody, 0);
        }

        string complexityStr = maxDepth switch
        {
            0 => "O(1)",
            1 => "O(N)",
            2 => "O(N^2)",
            _ => $"O(N^{maxDepth})"
        };

        // If O(1), there's no loop, so line number can just be the method's start line.
        if (maxDepth == 0)
        {
            maxDepthLine = method.GetLocation().GetLineSpan().StartLinePosition.Line + 1;
        }

        return new TimeComplexityResult(complexityStr, maxDepthLine);
    }
}
