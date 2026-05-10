"""
run_tests.py — Script para executar todos os testes

Uso: python run_tests.py
"""

import sys
import unittest

if __name__ == "__main__":
    # Descobrir e executar todos os testes
    loader = unittest.TestLoader()
    suite = loader.discover("tests", pattern="test_*.py")
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Retornar exit code apropriado
    sys.exit(0 if result.wasSuccessful() else 1)
