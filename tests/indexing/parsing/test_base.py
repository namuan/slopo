from slopo.indexing.parsing.base import hash_body


def test_identical_code_hashes_equal():
    assert hash_body("int sum = a + b;") == hash_body("int sum = a + b;")


def test_whitespace_differences_hash_equal():
    assert hash_body("int sum = a + b;") == hash_body("int  sum =\n\ta +  b;")


def test_minimal_code_difference_hashes_differently():
    assert hash_body("int sum = a + b;") != hash_body("int sum = a - b;")
