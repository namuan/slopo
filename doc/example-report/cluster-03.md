## (3) score 1.00-1.00

Hash: `e6c369338dc2`

---

- `slopo/indexing/parsing/lang/csharp.py` lines 22-26
- `slopo/indexing/parsing/lang/go.py` lines 14-18
- `slopo/indexing/parsing/lang/java.py` lines 14-18
- `slopo/indexing/parsing/lang/javascript.py` lines 20-24
- `slopo/indexing/parsing/lang/kotlin.py` lines 14-18
- `slopo/indexing/parsing/lang/python.py` lines 12-16
- `slopo/indexing/parsing/lang/rust.py` lines 14-18
- `slopo/indexing/parsing/lang/typescript.py` lines 20-24

```python
def parse(source: bytes) -> list[CodeUnit]:
    tree = _PARSER.parse(source)
    units: list[CodeUnit] = []
    _collect_units(tree.root_node, source, units)
    return units
```
