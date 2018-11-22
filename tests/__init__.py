import sys
import os

import restatic.models
resource_file = os.path.join(os.path.dirname(restatic.models.__file__), 'assets/icons')
sys.path.append(resource_file)
