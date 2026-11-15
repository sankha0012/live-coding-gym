from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Version:
    patch: int
    minor: int
    major: int


def sort_versions(versions):
    return sorted(versions)
