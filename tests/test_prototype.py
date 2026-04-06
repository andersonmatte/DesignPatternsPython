import unittest
import sys
import os

# Adicionar o diretório raiz ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patterns.criacionais.prototype import (
    PrototipoAmostra, AmostraDNA, AmostraRNA, RegistroPrototipos
)


class TestPrototype(unittest.TestCase):
    """Testes para o padrão Prototype."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.amostra_dna = AmostraDNA("DNA_001", "ATCGATCGATCG", "Humano")
        self.amostra_rna = AmostraRNA("RNA_001", "AUCGAUCGAUCG", "Humano")
        self.registro = RegistroPrototipos()
        
        # Adicionar protótipos ao registro
        self.registro.adicionar_prototipo("dna_padrao", self.amostra_dna)
        self.registro.adicionar_prototipo("rna_padrao", self.amostra_rna)
    
    def test_criar_amostra_dna(self):
        """Testa criação de amostra de DNA."""
        self.assertEqual(self.amostra_dna.id_amostra, "DNA_001")
        self.assertEqual(self.amostra_dna.sequencia, "ATCGATCGATCG")
        self.assertEqual(self.amostra_dna.especie, "Humano")
        self.assertEqual(self.amostra_dna.tipo, "DNA")
    
    def test_criar_amostra_rna(self):
        """Testa criação de amostra de RNA."""
        self.assertEqual(self.amostra_rna.id_amostra, "RNA_001")
        self.assertEqual(self.amostra_rna.sequencia, "AUCGAUCGAUCG")
        self.assertEqual(self.amostra_rna.especie, "Humano")
        self.assertEqual(self.amostra_rna.tipo, "RNA")
    
    def test_clonar_amostra_dna(self):
        """Testa clonagem de amostra de DNA."""
        clone_dna = self.amostra_dna.clonar("DNA_CLONE_001")
        
        self.assertEqual(clone_dna.id_amostra, "DNA_CLONE_001")
        self.assertEqual(clone_dna.sequencia, self.amostra_dna.sequencia)
        self.assertEqual(clone_dna.especie, self.amostra_dna.especie)
        self.assertEqual(clone_dna.tipo, self.amostra_dna.tipo)
        self.assertIsNot(clone_dna, self.amostra_dna)  # Objetos diferentes
    
    def test_clonar_amostra_rna(self):
        """Testa clonagem de amostra de RNA."""
        clone_rna = self.amostra_rna.clonar("RNA_CLONE_001")
        
        self.assertEqual(clone_rna.id_amostra, "RNA_CLONE_001")
        self.assertEqual(clone_rna.sequencia, self.amostra_rna.sequencia)
        self.assertEqual(clone_rna.especie, self.amostra_rna.especie)
        self.assertEqual(clone_rna.tipo, self.amostra_rna.tipo)
        self.assertIsNot(clone_rna, self.amostra_rna)  # Objetos diferentes
    
    def test_registro_adicionar_prototipo(self):
        """Testa adição de protótipo ao registro."""
        self.registro.adicionar_prototipo("novo_prototipo", self.amostra_dna)
        
        prototipo_recuperado = self.registro.obter_prototipo("novo_prototipo")
        self.assertEqual(prototipo_recuperado.id_amostra, "DNA_001")
        self.assertEqual(prototipo_recuperado.sequencia, "ATCGATCGATCG")
    
    def test_registro_obter_prototipo_inexistente(self):
        """Testa obtenção de protótipo inexistente."""
        prototipo = self.registro.obter_prototipo("inexistente")
        self.assertIsNone(prototipo)
    
    def test_registro_clonar_prototipo(self):
        """Testa clonagem via registro."""
        clone_registro = self.registro.clonar_prototipo("dna_padrao", "DNA_REG_CLONE")
        
        self.assertEqual(clone_registro.id_amostra, "DNA_REG_CLONE")
        self.assertEqual(clone_registro.sequencia, "ATCGATCGATCG")
        self.assertEqual(clone_registro.especie, "Humano")
        self.assertEqual(clone_registro.tipo, "DNA")
    
    def test_registro_clonar_prototipo_inexistente(self):
        """Testa clonagem de protótipo inexistente via registro."""
        clone = self.registro.clonar_prototipo("inexistente", "CLONE_TESTE")
        self.assertIsNone(clone)
    
    def test_modificar_clone_sem_afetar_original(self):
        """Testa que modificações no clone não afetam o original."""
        clone_dna = self.amostra_dna.clonar("DNA_MODIFICADO")
        
        # Modificar o clone
        clone_dna.sequencia = "CCCCCCCCCCCC"
        clone_dna.especie = "Modificado"
        
        # Verificar que o original não foi modificado
        self.assertEqual(self.amostra_dna.sequencia, "ATCGATCGATCG")
        self.assertEqual(self.amostra_dna.especie, "Humano")
        
        # Verificar que o clone foi modificado
        self.assertEqual(clone_dna.sequencia, "CCCCCCCCCCCC")
        self.assertEqual(clone_dna.especie, "Modificado")
    
    def test_multiplos_clones(self):
        """Testa criação de múltiplos clones."""
        clones = []
        
        for i in range(5):
            clone = self.amostra_dna.clonar(f"DNA_CLONE_{i}")
            clones.append(clone)
        
        # Verificar que todos os clones têm dados base
        for clone in clones:
            self.assertEqual(clone.sequencia, self.amostra_dna.sequencia)
            self.assertEqual(clone.especie, self.amostra_dna.especie)
            self.assertEqual(clone.tipo, self.amostra_dna.tipo)
        
        # Verificar que todos são objetos diferentes
        for i in range(len(clones)):
            for j in range(i + 1, len(clones)):
                self.assertIsNot(clones[i], clones[j])
    
    def test_clonar_com_diferentes_ids(self):
        """Testa clonagem com IDs diferentes."""
        clone1 = self.amostra_dna.clonar("CLONE_1")
        clone2 = self.amostra_dna.clonar("CLONE_2")
        
        self.assertNotEqual(clone1.id_amostra, clone2.id_amostra)
        self.assertEqual(clone1.sequencia, clone2.sequencia)
        self.assertEqual(clone1.especie, clone2.especie)
    
    def test_registro_listar_prototipos(self):
        """Testa listagem de protótipos no registro."""
        prototipos = self.registro.listar_prototipos()
        
        self.assertIn("dna_padrao", prototipos)
        self.assertIn("rna_padrao", prototipos)
        self.assertEqual(len(prototipos), 2)
    
    def test_registro_remover_prototipo(self):
        """Testa remoção de protótipo do registro."""
        self.registro.remover_prototipo("dna_padrao")
        
        prototipos = self.registro.listar_prototipos()
        self.assertNotIn("dna_padrao", prototipos)
        self.assertIn("rna_padrao", prototipos)
        self.assertEqual(len(prototipos), 1)
    
    def test_registro_remover_prototipo_inexistente(self):
        """Testa remoção de protótipo inexistente."""
        resultado = self.registro.remover_prototipo("inexistente")
        self.assertFalse(resultado)
    
    def test_clonar_profundidade(self):
        """Testa clonagem profunda de dados complexos."""
        # Adicionar dados complexos à amostra original
        self.amostra_dna.metadados = {
            "coleta": {"data": "2023-01-01", "local": "Lab A"},
            "processamento": ["etapa1", "etapa2", "etapa3"]
        }
        
        clone = self.amostra_dna.clonar("DNA_COMPLEXO")
        
        # Verificar que dados foram copiados
        self.assertEqual(clone.metadados, self.amostra_dna.metadados)
        
        # Modificar dados no clone
        clone.metadados["coleta"]["local"] = "Lab B"
        clone.metadados["processamento"].append("etapa4")
        
        # Verificar que original não foi afetado (se for shallow copy)
        # Nota: Esta implementação pode ser shallow ou deep dependendo dos requisitos
        self.assertEqual(self.amostra_dna.metadados["coleta"]["local"], "Lab A")
    
    def test_tipo_amostra_dna(self):
        """Testa métodos específicos de amostra DNA."""
        self.assertEqual(self.amostra_dna.obter_tipo_sequencia(), "DNA")
        self.assertEqual(self.amostra_dna.obter_comprimento(), 12)
        self.assertEqual(self.amostra_dna.obter_composicao()["A"], 3)
        self.assertEqual(self.amostra_dna.obter_composicao()["T"], 3)
        self.assertEqual(self.amostra_dna.obter_composicao()["C"], 3)
        self.assertEqual(self.amostra_dna.obter_composicao()["G"], 3)
    
    def test_tipo_amostra_rna(self):
        """Testa métodos específicos de amostra RNA."""
        self.assertEqual(self.amostra_rna.obter_tipo_sequencia(), "RNA")
        self.assertEqual(self.amostra_rna.obter_comprimento(), 12)
        self.assertEqual(self.amostra_rna.obter_composicao()["A"], 3)
        self.assertEqual(self.amostra_rna.obter_composicao()["U"], 3)
        self.assertEqual(self.amostra_rna.obter_composicao()["C"], 3)
        self.assertEqual(self.amostra_rna.obter_composicao()["G"], 3)
    
    def test_transcricao_rna(self):
        """Testa método de transcrição de RNA."""
        transcricao = self.amostra_rna.obter_transcricao()
        self.assertEqual(transcricao, "ATCGATCGATCG")
    
    def test_registro_estatisticas(self):
        """Testa estatísticas do registro."""
        stats = self.registro.obter_estatisticas()
        
        self.assertEqual(stats["total_prototipos"], 2)
        self.assertEqual(stats["tipos_amostra"]["DNA"], 1)
        self.assertEqual(stats["tipos_amostra"]["RNA"], 1)
        self.assertEqual(stats["especies"]["Humano"], 2)


if __name__ == "__main__":
    unittest.main()
