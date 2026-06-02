/**
 * Combines two values.
 * @param {number} a
 * @param {number} b
 */
function withComments(a, b) {
  // a leading line comment
  const sum = a + b; // a trailing line comment
  /* a block comment
     spanning lines */
  const url = "https://not-a-comment";
  return sum;
}
