using System.Text.Json;

namespace TcfAnalyzer;

/// <summary>Shared JSON options: camelCase property names, case-insensitive reads.</summary>
public static class Json
{
    public static readonly JsonSerializerOptions Options = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
        PropertyNameCaseInsensitive = true,
    };
}
