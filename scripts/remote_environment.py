import json, platform, sys
import numpy, scipy, torch, matplotlib
print(json.dumps({'python':sys.version,'platform':platform.platform(),'numpy':numpy.__version__,'scipy':scipy.__version__,'torch':torch.__version__,'gpu':torch.cuda.get_device_name(0) if torch.cuda.is_available() else None},indent=2))
