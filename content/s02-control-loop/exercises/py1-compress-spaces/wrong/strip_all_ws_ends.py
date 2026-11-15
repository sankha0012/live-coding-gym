import re
def compress_spaces(s):
    return re.sub(" +", " ", s).strip()
