import unittest
import sys
import os

# Adicionar o diretório raiz ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patterns.criacionais.abstract_factory import (
    FactoryProvider, GeneticaFactory, BioquimicaFactory, MolecularFactory
)


class TestAbstractFactory(unittest.TestCase):
    """Testes para o padrão Abstract Factory."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.factory_genetica = FactoryProvider.get_factory("genetica")
        self.factory_bioquimica = FactoryProvider.get_factory("bioquimica")
        self.factory_molecular = FactoryProvider.get_factory("molecular")
    
    def test_criar_factory_genetica(self):
        """Testa criação de factory genética."""
        self.assertIsInstance(self.factory_genetica, GeneticaFactory)
    
    def test_criar_factory_bioquimica(self):
        """Testa criação de factory bioquímica."""
        self.assertIsInstance(self.factory_bioquimica, BioquimicaFactory)
    
    def test_criar_factory_molecular(self):
        """Testa criação de factory molecular."""
        self.assertIsInstance(self.factory_molecular, MolecularFactory)
    
    def test_factory_invalido(self):
        """Testa criação de factory inválida."""
        with self.assertRaises(ValueError):
            FactoryProvider.get_factory("invalida")
    
    def test_criar_centrifuga_genetica(self):
        """Testa criação de centrífuga genética."""
        centrifuga = self.factory_genetica.criar_centrifuga()
        resultado = centrifuga.centrifugar("amostra_dna", 15000)
        
        self.assertIn("Centrífuga Genética", resultado)
        self.assertIn("15000 RPM", resultado)
        self.assertIn("amostra_dna", resultado)
    
    def test_criar_centrifuga_bioquimica(self):
        """Testa criação de centrífuga bioquímica."""
        centrifuga = self.factory_bioquimica.criar_centrifuga()
        resultado = centrifuga.centrifugar("amostra_proteina", 10000)
        
        self.assertIn("Centrífuga Bioquímica", resultado)
        self.assertIn("10000 RPM", resultado)
        self.assertIn("amostra_proteina", resultado)
    
    def test_criar_microscopio_genetica(self):
        """Testa criação de microscópio genético."""
        microscopio = self.factory_genetica.criar_microscopio()
        resultado = microscopio.observar("celula", 1000)
        
        self.assertIn("Microscópio Genético", resultado)
        self.assertIn("1000x", resultado)
        self.assertIn("celula", resultado)
    
    def test_criar_espectrofotometro_molecular(self):
        """Testa criação de espectrofotômetro molecular."""
        espectrofotometro = self.factory_molecular.criar_espectrofotometro()
        resultado = espectrofotometro.medir_absorbancia("280nm")
        
        self.assertIn("Espectrofotômetro Molecular", resultado)
        self.assertIn("280nm", resultado)
    
    def test_kit_genetico(self):
        """Testa criação de kit genético."""
        kit = self.factory_genetica.criar_kit_extracao()
        resultado = kit.extrair_dna("sangue")
        
        self.assertIn("Kit Genético", resultado)
        self.assertIn("sangue", resultado)
        self.assertIn("DNA extraído", resultado)
    
    def test_kit_bioquimico(self):
        """Testa criação de kit bioquímico."""
        kit = self.factory_bioquimica.criar_kit_extracao()
        resultado = kit.extrair_proteina("tecido")
        
        self.assertIn("Kit Bioquímico", resultado)
        self.assertIn("tecido", resultado)
        self.assertIn("Proteína extraída", resultado)
    
    def test_reagentes_moleculares(self):
        """Testa criação de reagentes moleculares."""
        reagentes = self.factory_molecular.criar_reagentes()
        resultado = reagentes.preparar_buffer("PCR")
        
        self.assertIn("Reagentes Moleculares", resultado)
        self.assertIn("PCR", resultado)
        self.assertIn("buffer preparado", resultado)
    
    def test_consistencia_factory(self):
        """Testa consistência dos produtos da mesma factory."""
        centrifuga1 = self.factory_genetica.criar_centrifuga()
        centrifuga2 = self.factory_genetica.criar_centrifuga()
        
        # Mesmo tipo de equipamento da mesma factory
        resultado1 = centrifuga1.centrifugar("teste", 10000)
        resultado2 = centrifuga2.centrifugar("teste", 10000)
        
        self.assertEqual(type(centrifuga1), type(centrifuga2))
        self.assertIn("Genética", resultado1)
        self.assertIn("Genética", resultado2)
    
    def test_diferencas_factories(self):
        """Testa diferenças entre factories."""
        centrifuga_genetica = self.factory_genetica.criar_centrifuga()
        centrifuga_bioquimica = self.factory_bioquimica.criar_centrifuga()
        
        resultado_genetica = centrifuga_genetica.centrifugar("teste", 10000)
        resultado_bioquimica = centrifuga_bioquimica.centrifugar("teste", 10000)
        
        self.assertNotEqual(type(centrifuga_genetica), type(centrifuga_bioquimica))
        self.assertIn("Genética", resultado_genetica)
        self.assertIn("Bioquímica", resultado_bioquimica)


if __name__ == "__main__":
    unittest.main()
