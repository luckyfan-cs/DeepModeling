from .registry import Registry

# Expose a default registry instance similar to mlebench
registry = Registry()

__all__ = [
    "registry",
    "Registry",
]
