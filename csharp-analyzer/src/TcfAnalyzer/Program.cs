using System.Text.Json;
using TcfAnalyzer;

// Local-only C# analyzer. Reads an AnalyzeRequest as JSON from stdin and writes an
// AnalyzeResponse as JSON to stdout. No network, no telemetry, no file output.
try
{
    using var input = Console.OpenStandardInput();
    var request = JsonSerializer.Deserialize<AnalyzeRequest>(input, Json.Options)
                  ?? throw new InvalidDataException("Empty or invalid request on stdin.");

    var response = ProjectAnalyzer.Analyze(request);

    using var output = Console.OpenStandardOutput();
    JsonSerializer.Serialize(output, response, Json.Options);
    return 0;
}
catch (Exception ex)
{
    Console.Error.WriteLine("[analyzer] fatal: " + ex.Message);
    return 1;
}
