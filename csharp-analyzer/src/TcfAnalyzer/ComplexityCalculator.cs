using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;

namespace TcfAnalyzer;

/// <summary>
/// McCabe cyclomatic complexity = 1 + number of decision points in the method body.
/// Decision points: if, for, foreach (incl. deconstruction), while, do, case labels
/// (default excluded), switch-expression arms, catch, the ?: operator, and the binary
/// &amp;&amp;, ||, ?? operators.
/// </summary>
public static class ComplexityCalculator
{
    public static int Compute(MethodDeclarationSyntax method)
    {
        var count = 1;
        foreach (var node in method.DescendantNodes())
        {
            switch (node.Kind())
            {
                case SyntaxKind.IfStatement:
                case SyntaxKind.ForStatement:
                case SyntaxKind.ForEachStatement:
                case SyntaxKind.ForEachVariableStatement:
                case SyntaxKind.WhileStatement:
                case SyntaxKind.DoStatement:
                case SyntaxKind.CaseSwitchLabel:
                case SyntaxKind.CasePatternSwitchLabel:
                case SyntaxKind.SwitchExpressionArm:
                case SyntaxKind.CatchClause:
                case SyntaxKind.ConditionalExpression:
                case SyntaxKind.LogicalAndExpression:
                case SyntaxKind.LogicalOrExpression:
                case SyntaxKind.CoalesceExpression:
                case SyntaxKind.CoalesceAssignmentExpression: // ??=
                case SyntaxKind.ConditionalAccessExpression:  // ?.
                case SyntaxKind.OrPattern:                    // is A or B
                case SyntaxKind.AndPattern:                   // is A and B
                    count++;
                    break;
            }
        }
        return count;
    }
}
