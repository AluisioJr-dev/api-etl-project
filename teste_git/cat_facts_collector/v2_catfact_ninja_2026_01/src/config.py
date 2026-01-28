"""
Configurações centralizadas para o projeto UOLCatLovers.

Este módulo gerencia todas as configurações da aplicação,
incluindo variáveis de ambiente, URLs da API e parâmetros de execução.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()


class Config:
    """Classe de configuração centralizada."""
    
    # Diretórios do projeto
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / os.getenv("OUTPUT_DIR", "data")
    LOGS_DIR = BASE_DIR / "logs"
    
    # API Configuration - V2: catfact.ninja (API alternativa - ONLINE)
    API_BASE_URL = os.getenv("API_BASE_URL", "https://catfact.ninja")
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))
    API_MAX_RETRIES = int(os.getenv("API_MAX_RETRIES", "3"))
    API_RETRY_DELAY = int(os.getenv("API_RETRY_DELAY", "2"))
    API_VERIFY_SSL = os.getenv("API_VERIFY_SSL", "False").lower() in ("true", "1", "yes")
    
    # API Endpoints - V2: catfact.ninja usa /facts com paginação
    @classmethod
    def get_facts_endpoint(cls) -> str:
        """Retorna o endpoint /facts da API catfact.ninja (paginado)."""
        return "/facts"
    
    # Endpoints estáticos
    FACTS_ENDPOINT = "/facts"  # catfact.ninja: retorna lista paginada
    RANDOM_FACT_ENDPOINT = "/fact"  # catfact.ninja: retorna fact aleatório (sem 's')
    
    # Output Configuration
    OUTPUT_FILENAME = os.getenv("OUTPUT_FILENAME", "cat_facts.csv")
    
    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = LOGS_DIR / "cat_facts_extraction.log"
    
    # Execution Configuration
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", "100"))
    MAX_RECORDS = int(os.getenv("MAX_RECORDS", "1000"))
    
    @classmethod
    def ensure_directories(cls):
        """Garante que os diretórios necessários existam."""
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.LOGS_DIR.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_output_path(cls) -> Path:
        """Retorna o caminho completo do arquivo de saída."""
        return cls.DATA_DIR / cls.OUTPUT_FILENAME
    
    @classmethod
    def display_config(cls):
        """Exibe as configurações atuais (útil para debug)."""
        return {
            "API_BASE_URL": cls.API_BASE_URL,
            "API_TIMEOUT": cls.API_TIMEOUT,
            "API_MAX_RETRIES": cls.API_MAX_RETRIES,
            "OUTPUT_PATH": str(cls.get_output_path()),
            "LOG_LEVEL": cls.LOG_LEVEL,
            "BATCH_SIZE": cls.BATCH_SIZE,
            "MAX_RECORDS": cls.MAX_RECORDS,
        }
