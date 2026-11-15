def parse_quantity(raw):
    try:
        return int(raw.strip())
    except ValueError:
        return 0
    except AttributeError:
        return 0
