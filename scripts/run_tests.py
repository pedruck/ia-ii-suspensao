import os,sys
from pathlib import Path
if Path('/content/project').exists():
 os.chdir('/content/project');sys.path.insert(0,os.getcwd())
for name in list(sys.modules):
 if name.startswith("test_") or name.startswith("src."): sys.modules.pop(name,None)
import importlib
importlib.invalidate_caches()
import unittest
r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover('tests'))
assert r.wasSuccessful()
