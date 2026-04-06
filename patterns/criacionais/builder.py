from typing import Any, Dict
from domain.analise import ProtocoloExperimental


class GeradorDeProtocolo:
    """Builder para construção incremental de protocolos experimentais."""
    
    def __init__(self):
        self.protocolo = ProtocoloExperimental()
    
    def com_nome_pesquisador(self, nome: str) -> 'GeradorDeProtocolo':
        """Define o nome do pesquisador responsável."""
        self.protocolo.nome_pesquisador = nome
        return self
    
    def com_volume_amostra(self, volume_ml: float) -> 'GeradorDeProtocolo':
        """Define o volume da amostra em mililitros."""
        self.protocolo.volume_amostra = volume_ml
        return self
    
    def com_tipo_analise(self, tipo: str) -> 'GeradorDeProtocolo':
        """Define o tipo de análise a ser realizada."""
        self.protocolo.tipo_analise = tipo
        return self
    
    def com_metodologia(self, metodologia: str) -> 'GeradorDeProtocolo':
        """Define a metodologia utilizada."""
        self.protocolo.metodologia = metodologia
        return self
    
    def com_parametro_adicional(self, chave: str, valor: Any) -> 'GeradorDeProtocolo':
        """Adiciona parâmetros adicionais ao protocolo."""
        self.protocolo.parametros_adicionais[chave] = valor
        return self
    
    def com_temperatura(self, temperatura_celsius: float) -> 'GeradorDeProtocolo':
        """Define a temperatura do experimento."""
        self.protocolo.parametros_adicionais["temperatura"] = temperatura_celsius
        return self
    
    def com_ph(self, ph: float) -> 'GeradorDeProtocolo':
        """Define o pH da solução."""
        self.protocolo.parametros_adicionais["ph"] = ph
        return self
    
    def com_tempo_incubacao(self, minutos: int) -> 'GeradorDeProtocolo':
        """Define o tempo de incubação em minutos."""
        self.protocolo.parametros_adicionais["tempo_incubacao"] = minutos
        return self
    
    def com_concentracao(self, concentracao: float, unidade: str = "mg/mL") -> 'GeradorDeProtocolo':
        """Define a concentração da amostra."""
        self.protocolo.parametros_adicionais["concentracao"] = f"{concentracao} {unidade}"
        return self
    
    def gerar(self) -> ProtocoloExperimental:
        """Gera o protocolo experimental configurado."""
        # Validações básicas
        if not self.protocolo.nome_pesquisador:
            raise ValueError("Nome do pesquisador é obrigatório")
        
        if self.protocolo.volume_amostra <= 0:
            raise ValueError("Volume da amostra deve ser maior que zero")
        
        if not self.protocolo.tipo_analise:
            raise ValueError("Tipo de análise é obrigatório")
        
        return self.protocolo
    
    def resetar(self) -> 'GeradorDeProtocolo':
        """Reseta o builder para criar um novo protocolo."""
        self.protocolo = ProtocoloExperimental()
        return self


class ProtocoloDirector:
    """Director que conhece receitas de protocolos comuns."""
    
    def __init__(self, builder: GeradorDeProtocolo):
        self.builder = builder
    
    def construir_protocolo_sequenciamento_padrao(self, nome_pesquisador: str) -> ProtocoloExperimental:
        """Constrói um protocolo padrão para sequenciamento."""
        return (self.builder
                .com_nome_pesquisador(nome_pesquisador)
                .com_volume_amostra(10.0)
                .com_tipo_analise("Sequenciamento")
                .com_metodologia("Sanger")
                .com_temperatura(37.0)
                .com_ph(7.5)
                .com_tempo_incubacao(60)
                .com_concentracao(50.0, "ng/μL")
                .gerar())
    
    def construir_protocolo_proteomica_padrao(self, nome_pesquisador: str) -> ProtocoloExperimental:
        """Constrói um protocolo padrão para análise proteômica."""
        return (self.builder
                .com_nome_pesquisador(nome_pesquisador)
                .com_volume_amostra(15.0)
                .com_tipo_analise("Proteômica")
                .com_metodologia("LC-MS/MS")
                .com_temperatura(4.0)
                .com_ph(8.0)
                .com_tempo_incubacao(120)
                .com_concentracao(1.0, "mg/mL")
                .com_parametro_adicional("enzima", "Tripsina")
                .gerar())
    
    def construir_protocolo_alinhamento_rapido(self, nome_pesquisador: str) -> ProtocoloExperimental:
        """Constrói um protocolo rápido para alinhamento."""
        return (self.builder
                .com_nome_pesquisador(nome_pesquisador)
                .com_volume_amostra(5.0)
                .com_tipo_analise("Alinhamento")
                .com_metodologia("BLAST")
                .com_temperatura(25.0)
                .com_concentracao(10.0, "ng/μL")
                .gerar())


# Exemplo de uso
if __name__ == "__main__":
    print("=== Exemplo 1: Construção manual de protocolo ===")
    # Exemplo: Construção incremental de protocolo
    protocolo_manual = (GeradorDeProtocolo()
                       .com_nome_pesquisador("Dr. Ana Silva")
                       .com_volume_amostra(15.5)
                       .com_tipo_analise("Sequenciamento")
                       .com_metodologia("Illumina")
                       .com_temperatura(37.0)
                       .com_ph(7.2)
                       .com_concentracao(25.0, "ng/μL")
                       .gerar())
    
    print("Protocolo Manual:")
    print(protocolo_manual)
    
    print("\n=== Exemplo 2: Uso do Director para protocolos padrão ===")
    builder = GeradorDeProtocolo()
    director = ProtocoloDirector(builder)
    
    # Protocolo de sequenciamento padrão
    protocolo_seq = director.construir_protocolo_sequenciamento_padrao("Dr. Carlos Mendes")
    print("Protocolo de Sequenciamento Padrão:")
    print(protocolo_seq)
    
    # Protocolo proteômico padrão
    protocolo_prot = director.construir_protocolo_proteomica_padrao("Dra. Maria Santos")
    print("\nProtocolo Proteômico Padrão:")
    print(protocolo_prot)
    
    # Protocolo rápido de alinhamento
    protocolo_alin = director.construir_protocolo_alinhamento_rapido("Dr. João Oliveira")
    print("\nProtocolo Rápido de Alinhamento:")
    print(protocolo_alin)
