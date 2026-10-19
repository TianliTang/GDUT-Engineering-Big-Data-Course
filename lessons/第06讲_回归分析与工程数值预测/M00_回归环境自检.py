from importlib import import_module
import json, sys
packages = {}
for name in ['numpy', 'pandas', 'matplotlib', 'sklearn']:
    module = import_module(name)
    packages[name] = getattr(module, '__version__', 'unknown')
print(json.dumps({'python': sys.version.split()[0], 'packages': packages, 'status': 'CHECK_PASS'}, ensure_ascii=False, indent=2))
