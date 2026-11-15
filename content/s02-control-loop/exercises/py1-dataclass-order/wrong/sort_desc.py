from dataclasses import dataclass
@dataclass(frozen=True, order=True)
class Version:
    major: int
    minor: int
    patch: int
def sort_versions(versions):
    return sorted(versions, reverse=True)
