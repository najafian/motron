import os
import importlib.util
import importlib

def scan_and_import_modules(base_dir="src/main", base_package="motron"):
    """
    Recursively scan all Python files in base_dir and import them as modules,
    assuming they follow the base_package structure.
    """
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                # Get full path
                full_path = os.path.join(root, file)
                # Convert path to importable module path
                rel_path = os.path.relpath(full_path, base_dir)  # e.g., 'domain/usecase/foo.py'
                module_path = rel_path.replace(os.sep, ".").replace(".py", "")  # 'domain.usecase.foo'
                full_module_name = f"{base_package}.{module_path}"  # e.g., 'motron.domain.usecase.foo'

                try:
                    importlib.import_module(full_module_name)
                    print(f"[Motron] Imported module: {full_module_name}")
                except Exception as e:
                    print(f"[Motron] Failed to import {full_module_name}: {e}")
