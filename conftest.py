import sys
import os

# Garantir que a raiz do repositório esteja no PYTHONPATH para imports locais (pages, utils)
ROOT = os.path.abspath(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
