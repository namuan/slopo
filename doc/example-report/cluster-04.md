## (4) score 0.94-1.00

Hash: `a3e5a5a93c89`

---

- `slopo/indexing/parsing/lang/javascript.py` lines 53-66
- `slopo/indexing/parsing/lang/typescript.py` lines 53-66

```python
def _binding_name_node(node: Node) -> Node | None:
    parent = node.parent
    if parent is None:
        return None
    if parent.type == "variable_declarator":  
        return parent.child_by_field_name("name")
    if parent.type == "pair":  
        return parent.child_by_field_name("key")
    if parent.type == "assignment_expression":  
        left = parent.child_by_field_name("left")
        if left is not None and left.type == "member_expression":
            return left.child_by_field_name("property")
        return left
    return None
```

---

- `slopo/indexing/parsing/lang/csharp.py` lines 56-67

```python
def _binding_name_node(node: Node) -> Node | None:
    parent = node.parent
    if parent is None:
        return None
    if parent.type == "variable_declarator":  
        return parent.child_by_field_name("name")
    if parent.type == "assignment_expression":  
        left = parent.child_by_field_name("left")
        if left is not None and left.type == "member_access_expression":
            return left.child_by_field_name("name")
        return left
    return None
```

---

- `slopo/indexing/parsing/lang/java.py` lines 48-59

```python
def _binding_name_node(node: Node) -> Node | None:
    parent = node.parent
    if parent is None:
        return None
    if parent.type == "variable_declarator":  
        return parent.child_by_field_name("name")
    if parent.type == "assignment_expression":  
        left = parent.child_by_field_name("left")
        if left is not None and left.type == "field_access":
            return left.child_by_field_name("field")
        return left
    return None
```

---

- `slopo/indexing/parsing/lang/rust.py` lines 48-59

```python
def _binding_name_node(node: Node) -> Node | None:
    parent = node.parent
    if parent is None:
        return None
    if parent.type == "let_declaration":  
        return parent.child_by_field_name("pattern")
    if parent.type == "assignment_expression":  
        left = parent.child_by_field_name("left")
        if left is not None and left.type == "field_expression":
            return left.child_by_field_name("field")
        return left
    return None
```

---

- `slopo/indexing/parsing/lang/kotlin.py` lines 49-61

```python
def _binding_name_node(node: Node) -> Node | None:
    parent = node.parent
    if parent is None:
        return None
    if parent.type == "property_declaration":  
        declaration = next(
            (c for c in parent.children if c.type == "variable_declaration"), None
        )
        return _last_identifier(declaration) if declaration else None
    if parent.type == "assignment":  
        target = parent.children[0] if parent.children else None
        return _last_identifier(target) if target else None
    return None
```

---

- `slopo/indexing/parsing/lang/go.py` lines 48-63

```python
def _binding_name_node(node: Node) -> Node | None:
    parent = node.parent  
    if parent is None or parent.type != "expression_list":
        return None
    binding = parent.parent
    if binding is None:
        return None
    if binding.type == "var_spec":  
        return binding.child_by_field_name("name")
    if binding.type in ("short_var_declaration", "assignment_statement"):
        
        
        left = binding.children[0] if binding.children else None
        target = left.children[0] if (left and left.children) else None
        return _target_name_node(target) if target else None
    return None
```
