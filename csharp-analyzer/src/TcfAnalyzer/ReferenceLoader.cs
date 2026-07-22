using Microsoft.CodeAnalysis;

namespace TcfAnalyzer;

/// <summary>
/// Loads BCL metadata references from the running runtime's trusted platform assemblies,
/// so the ad-hoc compilation can bind framework calls (e.g. List&lt;T&gt;.Add, Console.WriteLine)
/// without needing a .csproj or NuGet restore.
/// </summary>
public static class ReferenceLoader
{
    public static List<MetadataReference> BclReferences()
    {
        var refs = new List<MetadataReference>();
        var tpa = AppContext.GetData("TRUSTED_PLATFORM_ASSEMBLIES") as string ?? string.Empty;
        foreach (var path in tpa.Split(Path.PathSeparator))
        {
            if (path.EndsWith(".dll", StringComparison.OrdinalIgnoreCase) && File.Exists(path))
                refs.Add(MetadataReference.CreateFromFile(path));
        }
        return refs;
    }
}
