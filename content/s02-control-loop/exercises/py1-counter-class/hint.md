Keep a dict on self in __init__, and use dict.get(item, 0) so a missing item reads as zero. Sort with a tuple key for most_common.
