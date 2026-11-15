Write validate(row, schema). schema maps field → (type, min, max, default), type is 'float' or 'int'. For each schema field: missing, None or NaN → use default, record 'missing:<field>'. Can't convert to the type → default, record 'bad_type:<field>'. Out of range → clip, record 'clipped:<field>'. Fields not in the schema → record 'extra:<field>'. Return (clean_row, sorted list of issues). Don't modify the input.

*Garbage in: the first line of defence before a model sees real data.*

An AI assistant wrote the code below. The tests fail. Find the bug, fix it by hand, then name it in one sentence.
