"""Process command line arguments for pyui test programs
Command line options to this are:
    -w window/screen width
    -h window/screen height
    -f fullscreen flag (0 or 1)
    -r renderer ("dx" or other PyUI renderer)
"""

import getopt
import sys

def parseCommandLine( width = 0, height = 0, renderer = "p3d", fullscreen = 0 ):
    """Get and validate command line args."""
    
    opts, pargs = getopt.getopt(sys.argv[1:], "w:h:f:r:")
    for (opt, val) in opts:
        
        if opt == '-w':
            width = int(val)
            
        elif opt == '-h':
            height = int(val)
            
        elif opt == '-r':
            renderer = val

        elif opt == '-f':
            fullscreen = int(val)
            
    # parsed args successfully
    return (width, height, renderer, fullscreen)
