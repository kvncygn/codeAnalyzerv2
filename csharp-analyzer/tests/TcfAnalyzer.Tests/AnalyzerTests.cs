using TcfAnalyzer;
using Xunit;

namespace TcfAnalyzer.Tests;

public class AnalyzerTests
{
    private static AnalyzeResponse Run(string prefix, params (string Path, string Text)[] files)
        => ProjectAnalyzer.Analyze(new AnalyzeRequest(
            prefix,
            files.Select(f => new RequestFile(f.Path, f.Text)).ToList()));

    private static MethodResult Method(AnalyzeResponse r, string name)
        => r.Files.SelectMany(f => f.Methods).Single(m => m.Name == name);

    [Fact]
    public void Distinguishes_project_method_from_same_named_bcl_method()
    {
        const string src = @"
using System.Collections.Generic;
namespace D {
  class S {
    int Add(int a, int b) { return a + b; }
    public int TCF_M(int n) { var l = new List<int>(); l.Add(n); return Add(n, 1); }
  }
}";
        var helpers = Method(Run("TCF", ("S.cs", src)), "TCF_M").UsedHelpers;
        // The project Add() is a helper; List<int>.Add() is a library call and must be ignored.
        Assert.Equal(new[] { "Add" }, helpers.Select(h => h.Name).ToArray());
    }

    [Fact]
    public void Resolves_helper_defined_in_another_file()
    {
        const string util = @"namespace D { static class Util { public static int Sq(int v) => v * v; } }";
        const string svc = @"namespace D { class S { public int TCF_M(int n) { return Util.Sq(n); } } }";
        var helpers = Method(Run("TCF", ("Util.cs", util), ("S.cs", svc)), "TCF_M").UsedHelpers;
        Assert.Equal("Sq", Assert.Single(helpers).Name);
    }

    [Fact]
    public void Ignores_tcf_to_tcf_calls()
    {
        const string src = @"namespace D { class S {
            public int TCF_A(int n) { return TCF_B(n); }
            public int TCF_B(int n) { return n; }
        } }";
        Assert.Empty(Method(Run("TCF", ("S.cs", src)), "TCF_A").UsedHelpers);
    }

    [Fact]
    public void Computes_cyclomatic_complexity()
    {
        // base 1 + if + && + for + case + ?:  = 6
        const string src = @"namespace D { class S {
            public int TCF_M(int n) {
                int t = 0;
                if (n > 0 && n < 10) { t = 1; }
                for (int i = 0; i < n; i++) { t += i; }
                switch (n) { case 1: t = 1; break; default: break; }
                return n > 0 ? t : -t;
            }
        } }";
        Assert.Equal(6, Method(Run("TCF", ("S.cs", src)), "TCF_M").CyclomaticComplexity);
    }

    [Fact]
    public void Syntax_error_in_one_file_does_not_stop_others()
    {
        const string bad = "namespace D { class S { public int TCF_M( { return ; } }";
        const string good = "namespace D { class S2 { public int TCF_OK() { return 1; } } }";
        var r = Run("TCF", ("bad.cs", bad), ("good.cs", good));

        Assert.Equal(2, r.Files.Count);
        Assert.Contains(r.Files, f => f.Diagnostics.HasErrors);                       // bad flagged
        Assert.Contains(r.Files.SelectMany(f => f.Methods), m => m.Name == "TCF_OK"); // good analyzed
    }

    [Fact]
    public void Collects_line_and_block_comments()
    {
        const string src = "namespace D { class S { // c\n int TCF_M() { int x = 5; /* b */ return x; } } }";
        Assert.NotEmpty(Run("TCF", ("S.cs", src)).Files.Single().Comments);
    }

    [Fact]
    public void Resolves_helper_called_with_concatenated_or_member_arguments()
    {
        // Regression: under the ad-hoc compilation, an argument like "x" + n or n.ToString()
        // can leave the call's Symbol null (OverloadResolutionFailure). The helper must still
        // be detected via the candidate symbols, otherwise common logging/message calls vanish.
        const string src = @"namespace D { class S {
            public void TCF_M(int n) {
                Log(""line "" + n);
                Log(n.ToString());
            }
            void Log(string m) { }
        } }";
        var helpers = Method(Run("TCF", ("S.cs", src)), "TCF_M").UsedHelpers;
        Assert.Equal(new[] { "Log" }, helpers.Select(h => h.Name).ToArray());
    }

    [Fact]
    public void Concatenated_arguments_do_not_make_library_calls_into_helpers()
    {
        // The candidate fallback must not turn a same-named BCL call into a helper, even when
        // overload resolution fails on a concatenated argument.
        const string src = @"
using System.Collections.Generic;
namespace D { class S {
    public void TCF_M() {
        var items = new List<string>();
        items.Add(""a"" + ""b"");  // library List<string>.Add -> not a helper
        Add(""x"" + ""y"");        // project Add -> helper
    }
    void Add(string s) { }
} }";
        var helpers = Method(Run("TCF", ("S.cs", src)), "TCF_M").UsedHelpers;
        Assert.Equal(new[] { "Add" }, helpers.Select(h => h.Name).ToArray());
    }

    [Fact]
    public void Non_tcf_method_is_not_treated_as_helper_on_its_own()
    {
        // A non-TCF method that no TCF calls must produce no helpers anywhere.
        const string src = @"namespace D { class S { int Lonely() => 1; } }";
        var r = Run("TCF", ("S.cs", src));
        Assert.Empty(r.Files.SelectMany(f => f.Methods).SelectMany(m => m.UsedHelpers));
    }
}
