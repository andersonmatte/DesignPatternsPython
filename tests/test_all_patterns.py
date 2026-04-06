import unittest
import sys
import os

# Adicionar o diretório raiz ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar todos os testes
from test_factory_method import TestFactoryMethod
from test_singleton import TestSingleton
from test_observer import TestObserver
from test_abstract_factory import TestAbstractFactory
from test_builder import TestBuilder
from test_prototype import TestPrototype
from test_multiton import TestMultiton
from test_object_pool import TestObjectPool
from test_adapter import TestAdapter
from test_command import TestCommand
from test_iterator import TestIterator


def criar_suite_testes():
    """Cria suite com todos os testes."""
    suite = unittest.TestSuite()
    
    # Adicionar testes criacionais
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestFactoryMethod))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSingleton))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestObserver))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestAbstractFactory))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestBuilder))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestPrototype))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestMultiton))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestObjectPool))
    
    # Adicionar testes estruturais
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestAdapter))
    
    # Adicionar testes comportamentais
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestCommand))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestIterator))
    
    return suite


def executar_todos_testes():
    """Executa todos os testes e retorna resultados."""
    runner = unittest.TextTestRunner(verbosity=2)
    suite = criar_suite_testes()
    resultado = runner.run(suite)
    
    return resultado


if __name__ == "__main__":
    print("=" * 70)
    print("EXECUTANDO TODOS OS TESTES DO PROJETO DESIGN PATTERNS")
    print("=" * 70)
    
    resultado = executar_todos_testes()
    
    print("\n" + "=" * 70)
    print("RESUMO DOS TESTES")
    print("=" * 70)
    print(f"Testes executados: {resultado.testsRun}")
    print(f"Testes com falha: {len(resultado.failures)}")
    print(f"Testes com erro: {len(resultado.errors)}")
    print(f"Testes pulados: {len(resultado.skipped)}")
    
    if resultado.failures:
        print(f"\nFALHAS ({len(resultado.failures)}):")
        for test, traceback in resultado.failures:
            print(f"  - {test}")
    
    if resultado.errors:
        print(f"\nERROS ({len(resultado.errors)}):")
        for test, traceback in resultado.errors:
            print(f"  - {test}")
    
    if resultado.skipped:
        print(f"\nPULADOS ({len(resultado.skipped)}):")
        for test, reason in resultado.skipped:
            print(f"  - {test}: {reason}")
    
    # Status final
    if resultado.wasSuccessful():
        print("\n🎉 TODOS OS TESTES PASSARAM COM SUCESSO!")
        exit_code = 0
    else:
        print("\n❌ ALGUNS TESTES FALHARAM!")
        exit_code = 1
    
    print("=" * 70)
    sys.exit(exit_code)
