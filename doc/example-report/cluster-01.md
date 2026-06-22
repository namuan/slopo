## (1) score 0.96-1.00

Hash: `344750d2372b`

---

- `slopo/indexing/parsing/lang/csharp.py` lines 108-112
- `slopo/indexing/parsing/lang/go.py` lines 104-108
- `slopo/indexing/parsing/lang/java.py` lines 90-94
- `slopo/indexing/parsing/lang/javascript.py` lines 97-101
- `slopo/indexing/parsing/lang/kotlin.py` lines 100-104
- `slopo/indexing/parsing/lang/rust.py` lines 90-94
- `slopo/indexing/parsing/lang/typescript.py` lines 97-101

```python
def _count_named_nodes(node: Node) -> int:
    count = 1 if node.is_named else 0
    for child in node.children:
        count += _count_named_nodes(child)
    return count
```

---

- `slopo/indexing/parsing/lang/python.py` lines 68-74

```python
def _count_named_nodes(node: Node) -> int:
    if _is_docstring(node):
        return 0
    count = 1 if node.is_named else 0
    for child in node.children:
        count += _count_named_nodes(child)
    return count
```
