using System;

namespace Shapes;

public interface IShape
{
    double Area();
}

public class Circle : IShape
{
    public void Reset()
    {
    }

    public double Radius()
    {
        return _radius * _radius;
    }

    [Obsolete("Use Area instead")]
    public double Diameter()
    {
        double radius = 2.0;
        double diameter = radius * 2;
        if (diameter < 0)
        {
            throw new InvalidOperationException("negative diameter");
        }
        return diameter;
    }
}
