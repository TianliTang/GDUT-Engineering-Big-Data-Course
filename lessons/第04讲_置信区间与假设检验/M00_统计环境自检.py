import json
import sys

result = {'python': sys.version.split()[0], 'packages': {}}
for name in ['numpy', 'pandas', 'matplotlib', 'scipy']:
    module = __import__(name)
    result['packages'][name] = getattr(module, '__version__', 'unknown')
result['status'] = 'CHECK_PASS'
print(json.dumps(result, ensure_ascii=False, indent=2))
