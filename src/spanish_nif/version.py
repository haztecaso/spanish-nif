"""Utilities to retrieve the information of the program version."""

# Do not edit the version manually, let `cz bump` do it.
__version__ = "0.3.1"


def version_info() -> str:
    """Return a formatted summary of the library, Python, and platform versions."""
    import platform
    import sys
    from textwrap import dedent

    return dedent(
        f"""\
        ------------------------------------------------------------------
             spanish_nif: {__version__}
             Python: {sys.version.split(" ", maxsplit=1)[0]}
             Platform: {platform.platform()}
        ------------------------------------------------------------------"""
    )


if __name__ == "__main__":
    print(version_info())
