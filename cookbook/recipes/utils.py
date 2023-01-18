import re

# Convert string to kebabcase.
#-------------------------------------------------------------------------------
def kebabcase(s):
    return re.sub(r'([_ ])', '-', s).lower()

