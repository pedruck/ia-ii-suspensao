import os,sys
from pathlib import Path
if Path('/content/project').exists():
 os.chdir('/content/project');sys.path.insert(0,os.getcwd())
import unittest
r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover('tests'))
assert r.wasSuccessful()
