"""
Testes para o padrão Composite
"""

import unittest
from unittest.mock import Mock, patch
from patterns.estruturais.composite import (
    ComponenteGenomico, BaseNitrogenada, Aminoacido, SequenciaNucleotidica
)


class TestComposite(unittest.TestCase):
    """Testes para o padrão Composite."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.base1 = BaseNitrogenada("A", 1)
        self.base2 = BaseNitrogenada("T", 2)
        self.base3 = BaseNitrogenada("G", 3)
        
        self.amino1 = Aminoacido("A", 1)
        self.amino2 = Aminoacido("R", 2)
        
        self.sequencia = SequenciaNucleotidica("SEQ001")
        self.sequencia2 = SequenciaNucleotidica("SEQ002")
    
    def test_base_nitrogenada_creation(self):
        """Testa criação de base nitrogenada."""
        base = BaseNitrogenada("A", 1)
        
        self.assertIsInstance(base, ComponenteGenomico)
        self.assertEqual(base.nome, "Base_A_1")
        self.assertEqual(base.base, "A")
        self.assertEqual(base.posicao, 1)
        self.assertEqual(base.pares_hidrogenio, 2)
    
    def test_aminoacido_creation(self):
        """Testa criação de aminoácido."""
        amino = Aminoacido("A", 1)
        
        self.assertIsInstance(amino, ComponenteGenomico)
        self.assertEqual(amino.nome, "Aminoacido_A_1")
        self.assertEqual(amino.codigo, "A")
        self.assertEqual(amino.posicao, 1)
        self.assertEqual(amino.peso_molecular, 89.09)
    
    def test_sequencia_nucleotidica_creation(self):
        """Testa criação de sequência nucleotídica."""
        sequencia = SequenciaNucleotidica("SEQ001")
        
        self.assertIsInstance(sequencia, ComponenteGenomico)
        self.assertEqual(sequencia.nome, "SEQ001")
        self.assertEqual(len(sequencia.filhos), 0)
    
    def test_base_nitrogenada_adicionar(self):
        """Testa adição em base nitrogenada (deve falhar)."""
        with self.assertRaises(Exception):
            self.base1.adicionar(self.base2)
    
    def test_sequencia_nucleotidica_adicionar(self):
        """Testa adição em sequência nucleotídica."""
        self.sequencia.adicionar(self.base1)
        self.sequencia.adicionar(self.base2)
        
        self.assertEqual(len(self.sequencia.filhos), 2)
        self.assertIn(self.base1, self.sequencia.filhos)
    
    def test_sequencia_nucleotidica_remover(self):
        """Testa remoção em sequência nucleotídica."""
        self.sequencia.adicionar(self.base1)
        self.sequencia.adicionar(self.base2)
        
        self.sequencia.remover(self.base1)
        
        self.assertEqual(len(self.sequencia.filhos), 1)
        self.assertNotIn(self.base1, self.sequencia.filhos)
        self.assertIn(self.base2, self.sequencia.filhos)
    
    def test_base_nitrogenada_exibir(self):
        """Testa exibição de base nitrogenada."""
        resultado = self.base1.exibir()
        
        self.assertIsInstance(resultado, str)
        self.assertIn("Base: A", resultado)
        self.assertIn("Posição: 1", resultado)
        self.assertIn("Pares H: 2", resultado)
    
    def test_sequencia_nucleotidica_exibir(self):
        """Testa exibição de sequência nucleotídica."""
        self.sequencia.adicionar(self.base1)
        self.sequencia.adicionar(self.base2)
        
        resultado = self.sequencia.exibir()
        
        self.assertIsInstance(resultado, str)
        self.assertIn("Sequência: SEQ001", resultado)
        self.assertIn("Base: A", resultado)
        self.assertIn("Base: T", resultado)
    
    def test_base_nitrogenada_contar_componentes(self):
        """Testa contagem de componentes em base nitrogenada."""
        resultado = self.base1.contar_componentes()
        
        self.assertEqual(resultado, 1)
    
    def test_sequencia_nucleotidica_contar_componentes(self):
        """Testa contagem de componentes em sequência nucleotídica."""
        self.sequencia.adicionar(self.base1)
        self.sequencia.adicionar(self.base2)
        self.sequencia.adicionar(self.base3)
        
        resultado = self.sequencia.contar_componentes()
        
        self.assertEqual(resultado, 3)
    
    def test_base_nitrogenada_buscar(self):
        """Testa busca em base nitrogenada."""
        resultado = self.base1.buscar("Base_A_1")
        
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0], self.base1)
        
        resultado_vazio = self.base1.buscar("NomeInexistente")
        self.assertEqual(len(resultado_vazio), 0)
    
    def test_sequencia_nucleotidica_buscar(self):
        """Testa busca em sequência nucleotídica."""
        self.sequencia.adicionar(self.base1)
        self.sequencia.adicionar(self.base2)
        
        resultado = self.sequencia.buscar("Base_A_1")
        
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0], self.base1)
    
    def test_base_nitrogenada_complementar(self):
        """Testa complemento de base nitrogenada."""
        complemento_a = self.base1.complementar()
        complemento_t = self.base2.complementar()
        
        self.assertEqual(complemento_a.base, "T")
        self.assertEqual(complemento_t.base, "A")
    
    def test_nested_composite(self):
        """Testa composição aninhada."""
        # Criar sequências menores
        seq1 = SequenciaNucleotidica("SEQ001")
        seq2 = SequenciaNucleotidica("SEQ002")
        
        seq1.adicionar(BaseNitrogenada("A", 1))
        seq1.adicionar(BaseNitrogenada("T", 2))
        
        seq2.adicionar(BaseNitrogenada("G", 1))
        seq2.adicionar(BaseNitrogenada("C", 2))
        
        # Criar sequência principal
        seq_principal = SequenciaNucleotidica("MAIN001")
        seq_principal.adicionar(seq1)
        seq_principal.adicionar(seq2)
        
        # Verificar contagem
        resultado = seq_principal.contar_componentes()
        self.assertEqual(resultado, 4)
        
        # Verificar busca
        encontrados = seq_principal.buscar("Base_A_1")
        self.assertEqual(len(encontrados), 1)
    
    def test_composite_uniform_interface(self):
        """Testa interface uniforme entre componentes."""
        componentes = [self.base1, self.sequencia]
        
        for componente in componentes:
            # Todos devem ter os mesmos métodos
            self.assertTrue(hasattr(componente, 'exibir'))
            self.assertTrue(hasattr(componente, 'contar_componentes'))
            self.assertTrue(hasattr(componente, 'buscar'))
            
            # Todos devem retornar resultados consistentes
            contagem = componente.contar_componentes()
            self.assertIsInstance(contagem, int)
            self.assertGreaterEqual(contagem, 1)
    
    def test_composite_tree_structure(self):
        """Testa estrutura em árvore do composite."""
        # Nível 1: Sequência principal
        seq_principal = SequenciaNucleotidica("MAIN001")
        
        # Nível 2: Sub-sequências
        seq1 = SequenciaNucleotidica("SEQ001")
        seq2 = SequenciaNucleotidica("SEQ002")
        
        # Nível 3: Bases
        seq1.adicionar(BaseNitrogenada("A", 1))
        seq1.adicionar(BaseNitrogenada("T", 2))
        
        seq2.adicionar(BaseNitrogenada("G", 1))
        seq2.adicionar(BaseNitrogenada("C", 2))
        
        # Montar árvore
        seq_principal.adicionar(seq1)
        seq_principal.adicionar(seq2)
        
        # Verificar estrutura
        self.assertEqual(len(seq_principal.filhos), 2)
        self.assertEqual(seq_principal.contar_componentes(), 4)
        
        # Verificar exibição
        exibicao = seq_principal.exibir()
        self.assertIn("MAIN001", exibicao)
        self.assertIn("SEQ001", exibicao)
        self.assertIn("SEQ002", exibicao)


if __name__ == '__main__':
    unittest.main()
