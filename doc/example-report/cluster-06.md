## (6) score 0.93-1.00

Hash: `fc46752d2ce6`

---

- `slopo/indexing/parsing/lang/javascript.py` lines 44-50
- `slopo/indexing/parsing/lang/typescript.py` lines 44-50

```python
def _unit_name(node: Node) -> str:
    
    
    name_node = node.child_by_field_name("name")
    if name_node is None and node.type in {"arrow_function", "function_expression"}:
        name_node = _binding_name_node(node)
    return name_node.text.decode() if (name_node and name_node.text) else "<unknown>"
```

---

- `slopo/indexing/parsing/lang/kotlin.py` lines 38-46

```python
def _unit_name(node: Node) -> str:
    
    
    
    
    name_node = node.child_by_field_name("name")
    if name_node is None and node.type == "anonymous_function":
        name_node = _binding_name_node(node)
    return name_node.text.decode() if (name_node and name_node.text) else "<unknown>"
```

---

- `slopo/indexing/parsing/lang/go.py` lines 38-45

```python
def _unit_name(node: Node) -> str:
    
    
    
    name_node = node.child_by_field_name("name")
    if name_node is None and node.type == "func_literal":
        name_node = _binding_name_node(node)
    return name_node.text.decode() if (name_node and name_node.text) else "<unknown>"
```

---

- `slopo/indexing/parsing/lang/rust.py` lines 38-45

```python
def _unit_name(node: Node) -> str:
    
    
    
    name_node = node.child_by_field_name("name")
    if name_node is None and node.type == "closure_expression":
        name_node = _binding_name_node(node)
    return name_node.text.decode() if (name_node and name_node.text) else "<unknown>"
```

---

- `slopo/indexing/parsing/lang/java.py` lines 38-45

```python
def _unit_name(node: Node) -> str:
    
    
    
    name_node = node.child_by_field_name("name")
    if name_node is None and node.type == "lambda_expression":
        name_node = _binding_name_node(node)
    return name_node.text.decode() if (name_node and name_node.text) else "<unknown>"
```

---

- `slopo/indexing/parsing/lang/csharp.py` lines 46-53

```python
def _unit_name(node: Node) -> str:
    
    
    
    name_node = node.child_by_field_name("name")
    if name_node is None and node.type in _ANONYMOUS_TYPES:
        name_node = _binding_name_node(node)
    return name_node.text.decode() if (name_node and name_node.text) else "<unknown>"
```
