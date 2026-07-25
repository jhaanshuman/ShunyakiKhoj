# -*- coding: utf-8 -*-
"""
Module Registry v5.0.
Plugin-style architecture for registering and dynamically loading calculation modules.
Every subsystem is an independent module registered here.
"""

from typing import Dict, Any, List, Callable, Optional

class ModuleRegistry:
    """Central registry for v5.0 calculation modules."""

    _registry: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def register(cls, module_id: str, name: str, description: str, handler: Callable, default_enabled: bool = True, dependencies: Optional[List[str]] = None):
        """Register a new calculation module."""
        cls._registry[module_id] = {
            "id": module_id,
            "name": name,
            "description": description,
            "handler": handler,
            "default_enabled": default_enabled,
            "dependencies": dependencies or []
        }

    @classmethod
    def get_registered_modules(cls) -> List[str]:
        """Get list of all registered module IDs."""
        return list(cls._registry.keys())

    @classmethod
    def resolve_requested_modules(cls, requested: List[str]) -> List[str]:
        """Resolve requested module IDs, expanding 'ALL' or empty requests."""
        if not requested or "ALL" in [r.upper() for r in requested]:
            return cls.get_registered_modules()

        resolved = set()
        for req in requested:
            req_clean = req.strip()
            if req_clean in cls._registry:
                resolved.add(req_clean)
                # Auto-resolve dependencies
                for dep in cls._registry[req_clean]["dependencies"]:
                    if dep in cls._registry:
                        resolved.add(dep)
        return list(resolved)

    @classmethod
    def execute_module(cls, module_id: str, context: Dict[str, Any]) -> Any:
        """Execute a single module handler safely."""
        if module_id not in cls._registry:
            return {"error": f"Module '{module_id}' not registered."}
        try:
            return cls._registry[module_id]["handler"](context)
        except Exception as e:
            return {
                "status": "error",
                "module_id": module_id,
                "message": str(e)
            }
