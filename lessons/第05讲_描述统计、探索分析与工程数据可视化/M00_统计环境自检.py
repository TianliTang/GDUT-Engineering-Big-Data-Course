import json
import sys

result = {'python': sys.version.split()[0], 'packages': {}}
for package_name in ['numpy', 'pandas', 'matplotlib']:
    module = __import__(package_name)
    result['packages'][package_name] = getattr(module, '__version__', 'unknown')
result['status'] = 'CHECK_PASS'
print(json.dumps(result, ensure_ascii=False, indent=2))
