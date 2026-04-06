import unittest
import sys
import os

# Adicionar o diretório raiz ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patterns.criacionais.builder import (
    GeradorDeProtocolo, ProtocoloDirector
)


class TestBuilder(unittest.TestCase):
    """Testes para o padrão Builder."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.gerador = GeradorDeProtocolo()
        self.director = ProtocoloDirector()
    
    def test_criar_protocolo_vazio(self):
        """Testa criação de protocolo vazio."""
        protocolo = self.gerador.obter_protocolo()
        
        self.assertIsNone(protocolo.nome)
        self.assertIsNone(protocolo.pesquisador)
        self.assertEqual(protocolo.volume_amostra, 0.0)
        self.assertEqual(protocolo.tipo_analise, "")
        self.assertIsNone(protocolo.metodologia)
    
    def test_construir_protocolo_completo(self):
        """Testa construção de protocolo completo."""
        protocolo = (self.gerador
                     .com_nome("Protocolo Teste")
                     .com_pesquisador("Dr. Teste")
                     .com_volume_amostra(15.5)
                     .com_tipo_analise("Sequenciamento")
                     .com_metodologia("Illumina")
                     .gerar())
        
        self.assertEqual(protocolo.nome, "Protocolo Teste")
        self.assertEqual(protocolo.pesquisador, "Dr. Teste")
        self.assertEqual(protocolo.volume_amostra, 15.5)
        self.assertEqual(protocolo.tipo_analise, "Sequenciamento")
        self.assertEqual(protocolo.metodologia, "Illumina")
    
    def test_construir_protocolo_parcial(self):
        """Testa construção de protocolo parcial."""
        protocolo = (self.gerador
                     .com_nome("Protocolo Parcial")
                     .com_pesquisador("Dra. Teste")
                     .com_tipo_analise("Proteômica")
                     .gerar())
        
        self.assertEqual(protocolo.nome, "Protocolo Parcial")
        self.assertEqual(protocolo.pesquisador, "Dra. Teste")
        self.assertEqual(protocolo.tipo_analise, "Proteômica")
        self.assertEqual(protocolo.volume_amostra, 0.0)  # valor padrão
        self.assertIsNone(protocolo.metodologia)  # não definido
    
    def test_construir_protocolo_sequenciamento(self):
        """Testa construção de protocolo de sequenciamento via director."""
        protocolo = self.director.construir_protocolo_sequenciamento(
            self.gerador, "Seq_001", "Dr. Silva"
        )
        
        self.assertEqual(protocolo.nome, "Seq_001")
        self.assertEqual(protocolo.pesquisador, "Dr. Silva")
        self.assertEqual(protocolo.tipo_analise, "Sequenciamento")
        self.assertEqual(protocolo.metodologia, "Illumina")
        self.assertGreater(protocolo.volume_amostra, 0)
    
    def test_construir_protocolo_proteomica(self):
        """Testa construção de protocolo proteômico via director."""
        protocolo = self.director.construir_protocolo_proteomica(
            self.gerador, "Prot_001", "Dra. Santos"
        )
        
        self.assertEqual(protocolo.nome, "Prot_001")
        self.assertEqual(protocolo.pesquisador, "Dra. Santos")
        self.assertEqual(protocolo.tipo_analise, "Proteômica")
        self.assertEqual(protocolo.metodologia, "LC-MS/MS")
        self.assertGreater(protocolo.volume_amostra, 0)
    
    def test_construir_protocolo_metabolomica(self):
        """Testa construção de protocolo metabolômico via director."""
        protocolo = self.director.construir_protocolo_metabolomica(
            self.gerador, "Met_001", "Dr. Oliveira"
        )
        
        self.assertEqual(protocolo.nome, "Met_001")
        self.assertEqual(protocolo.pesquisador, "Dr. Oliveira")
        self.assertEqual(protocolo.tipo_analise, "Metabolômica")
        self.assertEqual(protocolo.metodologia, "NMR")
        self.assertGreater(protocolo.volume_amostra, 0)
    
    def test_validar_protocolo_completo(self):
        """Testa validação de protocolo completo."""
        protocolo = (self.gerador
                     .com_nome("Teste Validação")
                     .com_pesquisador("Dr. Teste")
                     .com_volume_amostra(10.0)
                     .com_tipo_analise("Sequenciamento")
                     .com_metodologia("Illumina")
                     .gerar())
        
        self.assertTrue(protocolo.validar())
    
    def test_validar_protocolo_incompleto(self):
        """Testa validação de protocolo incompleto."""
        protocolo = (self.gerador
                     .com_nome("Teste Incompleto")
                     .com_tipo_analise("Sequenciamento")
                     .gerar())
        
        self.assertFalse(protocolo.validar())
    
    def test_volume_amostra_invalido(self):
        """Testa volume de amostra inválido."""
        with self.assertRaises(ValueError):
            self.gerador.com_volume_amostra(-5.0)
    
    def test_volume_amostra_zero(self):
        """Testa volume de amostra zero."""
        protocolo = (self.gerador
                     .com_nome("Teste Zero")
                     .com_volume_amostra(0.0)
                     .gerar())
        
        self.assertEqual(protocolo.volume_amostra, 0.0)
    
    def test_resetar_builder(self):
        """Testa reset do builder."""
        protocolo1 = (self.gerador
                      .com_nome("Protocolo 1")
                      .com_pesquisador("Dr. Teste")
                      .gerar())
        
        self.gerador.resetar()
        
        protocolo2 = self.gerador.obter_protocolo()
        
        self.assertIsNone(protocolo2.nome)
        self.assertIsNone(protocolo2.pesquisador)
        self.assertNotEqual(protocolo1.nome, protocolo2.nome)
    
    def test_builder_imutabilidade(self):
        """Testa que o builder não modifica protocolos existentes."""
        protocolo1 = (self.gerador
                      .com_nome("Protocolo Original")
                      .gerar())
        
        protocolo2 = (self.gerador
                      .com_nome("Protocolo Modificado")
                      .gerar())
        
        self.assertEqual(protocolo1.nome, "Protocolo Original")
        self.assertEqual(protocolo2.nome, "Protocolo Modificado")
    
    def test_metodologia_vazia(self):
        """Testa construção com metodologia vazia."""
        protocolo = (self.gerador
                     .com_nome("Teste")
                     .com_metodologia("")
                     .gerar())
        
        self.assertEqual(protocolo.metodologia, "")
    
    def test_construir_multiplos_protocolos(self):
        """Testa construção de múltiplos protocolos."""
        protocolos = []
        
        for i in range(3):
            protocolo = (self.gerador
                         .com_nome(f"Protocolo_{i}")
                         .com_pesquisador(f"Pesquisador_{i}")
                         .gerar())
            protocolos.append(protocolo)
        
        self.assertEqual(len(protocolos), 3)
        self.assertEqual(protocolos[0].nome, "Protocolo_0")
        self.assertEqual(protocolos[1].nome, "Protocolo_1")
        self.assertEqual(protocolos[2].nome, "Protocolo_2")


if __name__ == "__main__":
    unittest.main()
