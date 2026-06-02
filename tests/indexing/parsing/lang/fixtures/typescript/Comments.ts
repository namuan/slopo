/**
 * Computes the total price including tax.
 * @param amount the pre-tax amount
 */
function totalWithTax(amount: number): number {
  // apply the standard rate
  const rate = 0.2; /* twenty percent */
  const docsUrl = "https://example.com/* not a comment */";
  return amount * (1 + rate);
}
