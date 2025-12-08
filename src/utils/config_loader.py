"""
Carregador de configurações do projeto
"""

import yaml
from pathlib import Path
from typing import Dict, Any


class ConfigLoader:
    """Classe para carregar e gerenciar configurações do projeto"""
    
    def __init__(self, config_path: str = None):
        """
        Inicializa o carregador de configurações
        
        Args:
            config_path: Caminho para o arquivo de configuração YAML
        """
        if config_path is None:
            # Usa o arquivo de configuração padrão
            project_root = Path(__file__).parent.parent.parent
            config_path = project_root / "config" / "munduruku_config.yaml"
        
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Carrega o arquivo de configuração YAML
        
        Returns:
            Dicionário com as configurações
        """
        if not self.config_path.exists():
            raise FileNotFoundError(f"Arquivo de configuração não encontrado: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        return config
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Obtém um valor de configuração
        
        Args:
            key: Chave da configuração (pode usar notação de ponto, ex: 'study_area.name')
            default: Valor padrão se a chave não existir
            
        Returns:
            Valor da configuração
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_study_area(self) -> Dict[str, Any]:
        """Retorna configurações da área de estudo"""
        return self.config.get('study_area', {})
    
    def get_satellite_config(self) -> Dict[str, Any]:
        """Retorna configurações de dados de satélite"""
        return self.config.get('satellite_data', {})
    
    def get_preprocessing_config(self) -> Dict[str, Any]:
        """Retorna configurações de pré-processamento"""
        return self.config.get('preprocessing', {})
    
    def get_classification_config(self) -> Dict[str, Any]:
        """Retorna configurações de classificação"""
        return self.config.get('classification', {})
    
    def get_detection_config(self) -> Dict[str, Any]:
        """Retorna configurações de detecção"""
        return self.config.get('detection', {})
    
    def get_monitoring_config(self) -> Dict[str, Any]:
        """Retorna configurações de monitoramento"""
        return self.config.get('monitoring', {})
    
    def get_output_config(self) -> Dict[str, Any]:
        """Retorna configurações de saída"""
        return self.config.get('output', {})


# Instância global para facilitar o acesso
config_loader = ConfigLoader()
