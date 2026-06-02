namespace Text;

public class Formatter
{
    public string Indent(string[] lines, int spaces)
    {
        string Pad(string line) => new string(' ', spaces) + line;

        var result = new List<string>();
        foreach (var line in lines)
        {
            result.Add(Pad(line));
        }
        return string.Join("\n", result);
    }
}
