"""
Root-level conftest.py

Ensures the project root is on sys.path so that all
package imports (ui_tests, utils) resolve
correctly regardless of the directory pytest is invoked from.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
