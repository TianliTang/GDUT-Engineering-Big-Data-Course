from importlib import import_module
import json,sys
packages={}
for name in ['numpy','pandas','matplotlib','sklearn']:
    m=import_module(name); packages[name]=getattr(m,'__version__','unknown')
print(json.dumps({'python':sys.version.split()[0],'packages':packages,'status':'CHECK_PASS'},ensure_ascii=False,indent=2))
