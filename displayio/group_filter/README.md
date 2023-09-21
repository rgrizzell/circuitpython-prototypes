# Group Filter
Iterates through the layer structure and returns a list of objects. Accepts an optional filter function. Useful for
interacting with dynamic UI elements.
```python
print("Unfiltered")
print(filter_group(screen))
print("Filtered: Rect")
print(filter_group(screen, filter_func=lambda x: isinstance(x, Rect)))
print("Filtered: Circle")
print(filter_group(screen, filter_func=lambda x: isinstance(x, Circle)))
```

```text
Unfiltered
[[<Rect object at 0x2000b560>, <Rect object at 0x20010420>, <Circle object at 0x20010ae0>], [<Rect object at 0x20010bb0>, <Circle object at 0x200139d0>]]
Filtered: Rect
[[<Rect object at 0x2000b560>, <Rect object at 0x20010420>], [<Rect object at 0x20010bb0>]]
Filtered: Circle
[[<Circle object at 0x20010ae0>], [<Circle object at 0x200139d0>]]
```
