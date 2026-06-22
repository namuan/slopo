## (9) score 0.93-0.97

Hash: `38abfbd70dde`

---

- `slopo/indexing/parsing/lang/python.py` lines 61-65

```python
def _count_body_nodes(function_definition: Node) -> int:
    body = function_definition.child_by_field_name("body")
    if body is None:
        return 0
    return _count_named_nodes(body)
```

---

- `slopo/indexing/parsing/lang/kotlin.py` lines 91-97

```python
def _count_body_nodes(function_declaration: Node) -> int:
    body = next(
        (c for c in function_declaration.children if c.type == "function_body"), None
    )
    if body is None:
        return 0
    return _count_named_nodes(body)
```

---

- `slopo/indexing/parsing/lang/java.py` lines 83-87

```python
def _count_body_nodes(method_declaration: Node) -> int:
    body = method_declaration.child_by_field_name("body")
    if body is None:
        return 0
    return _count_named_nodes(body)
```
