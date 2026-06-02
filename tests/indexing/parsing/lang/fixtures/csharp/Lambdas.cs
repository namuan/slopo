using System;
using System.Linq;

namespace Pipeline;

public class Processor
{
    public int[] Transform(int[] values)
    {
        Func<int, int> doubler = x => x * 2;
        return values
            .Where(v => v > 0)
            .Select(v =>
            {
                int scaled = doubler(v);
                return scaled + 1;
            })
            .ToArray();
    }

    public void Configure()
    {
        OnError = delegate(Exception ex)
        {
            Console.WriteLine(ex.Message);
        };
    }
}
