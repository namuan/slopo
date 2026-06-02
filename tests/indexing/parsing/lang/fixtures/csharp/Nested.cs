namespace Orders;

public class OrderService
{
    public decimal Total(decimal[] amounts)
    {
        decimal sum = 0;
        foreach (var amount in amounts)
        {
            sum += amount;
        }
        return sum;
    }

    private class Validator
    {
        public bool IsValid(decimal amount)
        {
            return amount >= 0;
        }
    }
}
