## (7) score 0.98-1.00

Hash: `60849c6d52f1`

---

- `slopo/indexing/parsing/lang/csharp.py` lines 83-88
- `slopo/indexing/parsing/lang/go.py` lines 89-94
- `slopo/indexing/parsing/lang/java.py` lines 75-80
- `slopo/indexing/parsing/lang/javascript.py` lines 82-87
- `slopo/indexing/parsing/lang/kotlin.py` lines 83-88
- `slopo/indexing/parsing/lang/rust.py` lines 75-80
- `slopo/indexing/parsing/lang/typescript.py` lines 82-87

```python
def _collect_comment_spans(node: Node, spans: list[tuple[int, int]]) -> None:
    if node.type in _COMMENT_TYPES:
        spans.append((node.start_byte, node.end_byte))
        return
    for child in node.children:
        _collect_comment_spans(child, spans)
```

---

- `slopo/indexing/parsing/lang/python.py` lines 53-58

```python
def _collect_comment_spans(node: Node, spans: list[tuple[int, int]]) -> None:
    if node.type in _COMMENT_TYPES or _is_docstring(node):
        spans.append((node.start_byte, node.end_byte))
        return
    for child in node.children:
        _collect_comment_spans(child, spans)
```
