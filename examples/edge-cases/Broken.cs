using System;

// This file has a deliberate SYNTAX ERROR (missing closing brace).
// Analysis must NOT crash; other files should still be analyzed.
public class Broken
{
    public void TCF_Oops()
    {
        Console.WriteLine("missing brace below");
    // <-- closing brace of method intentionally omitted
}
