## (2) score 0.95-1.00

Hash: `dcd405ffdfbc`

---

- `slopo/indexing/parsing/lang/kotlin.py` lines 70-80
- `slopo/indexing/parsing/lang/python.py` lines 40-50

```python
def _body_without_comments(function: Node, source: bytes) -> str:
    comment_spans: list[tuple[int, int]] = []
    _collect_comment_spans(function, comment_spans)

    pieces: list[bytes] = []
    cursor = function.start_byte
    for start, end in sorted(comment_spans):
        pieces.append(source[cursor:start])
        cursor = end
    pieces.append(source[cursor : function.end_byte])
    return b"".join(pieces).decode()
```

---

- `slopo/indexing/parsing/lang/java.py` lines 62-72

```python
def _body_without_comments(method: Node, source: bytes) -> str:
    comment_spans: list[tuple[int, int]] = []
    _collect_comment_spans(method, comment_spans)

    pieces: list[bytes] = []
    cursor = method.start_byte
    for start, end in sorted(comment_spans):
        pieces.append(source[cursor:start])
        cursor = end
    pieces.append(source[cursor : method.end_byte])
    return b"".join(pieces).decode()
```

---

- `slopo/indexing/parsing/lang/csharp.py` lines 70-80
- `slopo/indexing/parsing/lang/go.py` lines 76-86
- `slopo/indexing/parsing/lang/javascript.py` lines 69-79
- `slopo/indexing/parsing/lang/rust.py` lines 62-72
- `slopo/indexing/parsing/lang/typescript.py` lines 69-79

```python
def _body_without_comments(unit: Node, source: bytes) -> str:
    comment_spans: list[tuple[int, int]] = []
    _collect_comment_spans(unit, comment_spans)

    pieces: list[bytes] = []
    cursor = unit.start_byte
    for start, end in sorted(comment_spans):
        pieces.append(source[cursor:start])
        cursor = end
    pieces.append(source[cursor : unit.end_byte])
    return b"".join(pieces).decode()
```
