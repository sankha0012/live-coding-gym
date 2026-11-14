from dataclasses import dataclass


@dataclass(frozen=True)
class Version:
    major: int
    minor: int
    patch: int


def sort_versions(versions):
    return sorted(versions, key=lambda v: (v.major, v.minor, v.patch))
