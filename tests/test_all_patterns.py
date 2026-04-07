import unittest
import sys
import os

# Adicionar o diretório raiz ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar todos os testes dos 23 padrões GoF
from test_factory_method import TestFactoryMethod
from test_singleton import TestSingleton
from test_observer import TestObserver
from test_abstract_factory import TestAbstractFactory
from test_builder import TestBuilder
from test_prototype import TestPrototype
from test_adapter import TestAdapter
from test_bridge_fixed import TestBridge
from test_composite_final import TestComposite
from test_decorator_simple import TestDecorator
from test_facade_simple import TestFacade
from test_flyweight_working import TestFlyweight
from test_proxy_working import TestProxy
from test_chain_of_responsibility import TestChainOfResponsibility
from test_command import TestCommand
from test_iterator import TestIterator
from test_mediator_working import TestMediator
from test_memento import TestMemento
from test_observer import TestObserver
from test_state_working import TestState
from test_strategy import TestStrategy
from test_template_method_working import TestTemplateMethod
from test_visitor_working import TestVisitor


def criar_suite_testes():
    """Cria suite com todos os testes dos 23 padrões GoF."""
    suite = unittest.TestSuite()
    
    # Padrões Criacionais (5)
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestFactoryMethod))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestAbstractFactory))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestBuilder))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestPrototype))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSingleton))
    
    # Padrões Estruturais (7)
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestAdapter))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestBridge))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestComposite))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDecorator))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestFacade))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestFlyweight))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestProxy))
    
    # Padrões Comportamentais (11)
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestChainOfResponsibility))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestCommand))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestIterator))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestMediator))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestMemento))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestObserver))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestState))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestStrategy))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestTemplateMethod))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestVisitor))
    
    return suite


def executar_todos_testes():
    """Executa todos os testes e retorna resultados."""
    runner = unittest.TextTestRunner(verbosity=2)
    suite = criar_suite_testes()
    resultado = runner.run(suite)
    
    return resultado


if __name__ == "__main__":
    print("=" * 70)
    print("EXECUTANDO TODOS OS TESTES DOS 23 PADRÕES GOF")
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
