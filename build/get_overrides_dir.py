import os
import pygtk
pygtk.require('2.0')

try:
    import gi.overrides
    print os.path.dirname(gi.overrides.__file__)
except:
    pass
