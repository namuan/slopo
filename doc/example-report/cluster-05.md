## (5) score 0.96-1.00

Hash: `05d70662b75d`

---

- `slopo/indexing/parsing/lang/csharp.py` lines 29-43
- `slopo/indexing/parsing/lang/go.py` lines 21-35
- `slopo/indexing/parsing/lang/java.py` lines 21-35
- `slopo/indexing/parsing/lang/javascript.py` lines 27-41
- `slopo/indexing/parsing/lang/kotlin.py` lines 21-35
- `slopo/indexing/parsing/lang/rust.py` lines 21-35
- `slopo/indexing/parsing/lang/typescript.py` lines 27-41

```python
def _collect_units(node: Node, source: bytes, units: list[CodeUnit]) -> None:
    if node.type in _UNIT_TYPES:
        body = _body_without_comments(node, source)
        units.append(
            CodeUnit(
                name=_unit_name(node),
                body=body,
                start_line=node.start_point[0] + 1,
                end_line=node.end_point[0] + 1,
                body_node_count=_count_body_nodes(node),
                body_hash=hash_body(body),
            )
        )
    for child in node.children:
        _collect_units(child, source, units)
```

---

- `slopo/indexing/parsing/lang/python.py` lines 19-37

```python
def _collect_units(node: Node, source: bytes, units: list[CodeUnit]) -> None:
    if node.type == "function_definition":
        name_node = node.child_by_field_name("name")
        name = (
            name_node.text.decode() if (name_node and name_node.text) else "<unknown>"
        )
        body = _body_without_comments(node, source)
        units.append(
            CodeUnit(
                name=name,
                body=body,
                start_line=node.start_point[0] + 1,
                end_line=node.end_point[0] + 1,
                body_node_count=_count_body_nodes(node),
                body_hash=hash_body(body),
            )
        )
    for child in node.children:
        _collect_units(child, source, units)
```
