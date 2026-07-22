"""PyInstaller entry point.

A thin top-level launcher (not inside the package) so that absolute imports work when
PyInstaller runs it as the program's main script.
"""

from codeanalyzer.__main__ import main

if __name__ == "__main__":
    main()
