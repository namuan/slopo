## (8) score 0.99-1.00

Hash: `e1c991a348b6`

---

- `slopo/indexing/parsing/lang/go.py` lines 97-101
- `slopo/indexing/parsing/lang/javascript.py` lines 90-94
- `slopo/indexing/parsing/lang/rust.py` lines 83-87
- `slopo/indexing/parsing/lang/typescript.py` lines 90-94

```python
def _count_body_nodes(unit: Node) -> int:
    body = unit.child_by_field_name("body")
    if body is None:
        return 0
    return _count_named_nodes(body)
```

---

- `slopo/indexing/parsing/lang/csharp.py` lines 91-95

```python
def _count_body_nodes(unit: Node) -> int:
    body = _body_node(unit)
    if body is None:
        return 0
    return _count_named_nodes(body)
```
