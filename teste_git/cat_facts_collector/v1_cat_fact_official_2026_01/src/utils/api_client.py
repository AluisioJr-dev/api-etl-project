"""
Cliente HTTP para interação com a Cat Facts API.

Implementa retry logic, tratamento de erros e validação de respostas.
"""

import time
import warnings
from typing import Dict, List, Optional
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from urllib3.exceptions import InsecureRequestWarning

from src.config import Config
from src.utils.logger import setup_logger


logger = setup_logger(__name__)

# Suprime warnings de SSL quando verificação está desabilitada
warnings.filterwarnings('ignore', category=InsecureRequestWarning)


class CatFactsAPIClient:
    """Cliente para a Cat Facts API com retry logic e tratamento de erros."""
    
    def __init__(
        self,
        base_url: str = Config.API_BASE_URL,
        timeout: int = Config.API_TIMEOUT,
        max_retries: int = Config.API_MAX_RETRIES,
        retry_delay: int = Config.API_RETRY_DELAY,
        verify_ssl: bool = Config.API_VERIFY_SSL
    ):
        """
        Inicializa o cliente da API.
        
        Args:
            base_url: URL base da API
            timeout: Timeout das requisições em segundos
            max_retries: Número máximo de tentativas
            retry_delay: Delay entre tentativas em segundos
            verify_ssl: Se deve verificar certificados SSL
        """
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.verify_ssl = verify_ssl
        self.session = self._create_session()
        
        if not verify_ssl:
            logger.warning("⚠️  Verificação SSL desabilitada - use apenas em desenvolvimento!")
        logger.info(f"API Client inicializado: {base_url}")
    
    def _create_session(self) -> requests.Session:
        """
        Cria uma sessão HTTP com retry strategy.
        
        Returns:
            Sessão configurada
        """
        session = requests.Session()
        
        # Configuração de retry
        retry_strategy = Retry(
            total=self.max_retries,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"],
            backoff_factor=1
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Headers padrão
        session.headers.update({
            "User-Agent": "UOLCatLovers/1.0",
            "Accept": "application/json"
        })
        
        return session
    
    def _make_request(
        self,
        endpoint: str,
        params: Optional[Dict] = None,
        method: str = "GET"
    ) -> Dict:
        """
        Executa uma requisição HTTP com tratamento de erros.
        
        Args:
            endpoint: Endpoint da API
            params: Parâmetros da query string
            method: Método HTTP
        
        Returns:
            Dados da resposta em JSON
        
        Raises:
            requests.exceptions.RequestException: Erro na requisição
        """
        url = urljoin(self.base_url, endpoint)
        
        for attempt in range(1, self.max_retries + 1):
            try:
                logger.debug(f"Tentativa {attempt}/{self.max_retries} - {method} {url}")
                
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    timeout=self.timeout,
                    verify=self.verify_ssl
                )
                
                response.raise_for_status()
                
                logger.debug(f"Requisição bem-sucedida: {url}")
                return response.json()
                
            except requests.exceptions.HTTPError as e:
                logger.error(f"HTTP Error {e.response.status_code}: {e}")
                
                if e.response.status_code == 429:  # Rate limit
                    wait_time = self.retry_delay * attempt
                    logger.warning(f"Rate limit atingido. Aguardando {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                
                if attempt == self.max_retries:
                    raise
                    
            except requests.exceptions.Timeout as e:
                logger.error(f"Timeout na requisição: {e}")
                if attempt == self.max_retries:
                    raise
                time.sleep(self.retry_delay)
                
            except requests.exceptions.ConnectionError as e:
                logger.error(f"Erro de conexão: {e}")
                if attempt == self.max_retries:
                    raise
                time.sleep(self.retry_delay)
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Erro na requisição: {e}")
                raise
        
        raise requests.exceptions.RequestException(
            f"Falha após {self.max_retries} tentativas"
        )
    
    def get_all_facts(self, animal_type: str = "cat", max_pages: int = 10) -> List[Dict]:
        """
        Busca todos os fatos disponíveis. Detecta automaticamente qual API está sendo usada.
        
        - catfact.ninja: Usa endpoint /facts com paginação (limit/page)
        - cat-fact.herokuapp.com: Usa endpoint /facts/random com amount
        
        Args:
            animal_type: Tipo de animal (padrão: 'cat')
            max_pages: Número máximo de páginas a buscar (para APIs com paginação)
        
        Returns:
            Lista de fatos
        """
        is_catfact_ninja = "catfact.ninja" in Config.API_BASE_URL
        
        if is_catfact_ninja:
            return self._get_facts_paginated(animal_type, max_pages)
        else:
            return self._get_facts_bulk(animal_type)
    
    def _get_facts_bulk(self, animal_type: str = "cat") -> List[Dict]:
        """
        Busca fatos em bulk da API oficial Heroku (endpoint /facts/random).
        
        Args:
            animal_type: Tipo de animal
            
        Returns:
            Lista de fatos
        """
        logger.info(f"Buscando fatos da API oficial cat-fact.herokuapp.com...")
        
        try:
            params = {
                "animal_type": animal_type,
                "amount": 500  # Máximo permitido pela API oficial
            }
            
            data = self._make_request(Config.RANDOM_FACT_ENDPOINT, params=params)
            
            # A API retorna um array direto quando amount > 1
            if isinstance(data, list):
                all_facts = data
            elif isinstance(data, dict):
                # Se retornar um único objeto, coloca em lista
                all_facts = [data]
            else:
                logger.warning(f"Resposta inesperada da API: {type(data)}")
                all_facts = []
            
            logger.info(f"Total de {len(all_facts)} fatos obtidos")
            return all_facts
            
        except Exception as e:
            logger.error(f"Erro ao buscar fatos: {str(e)}")
            return []
    
    def _get_facts_paginated(self, animal_type: str = "cat", max_pages: int = 10) -> List[Dict]:
        """
        Busca fatos com paginação da API catfact.ninja (endpoint /facts).
        
        Args:
            animal_type: Tipo de animal
            max_pages: Número máximo de páginas
            
        Returns:
            Lista de fatos
        """
        logger.info(f"Buscando fatos da API catfact.ninja...")
        
        all_facts = []
        page = 1
        
        while page <= max_pages:
            try:
                params = {"limit": 100, "page": page}
                data = self._make_request(Config.FACTS_ENDPOINT, params=params)
                
                # catfact.ninja retorna: {"current_page": 1, "data": [...], "last_page": 4}
                if isinstance(data, dict) and "data" in data:
                    facts = data["data"]
                    
                    if not facts:
                        logger.info("Nenhum fato encontrado na página atual")
                        break
                    
                    all_facts.extend(facts)
                    logger.info(f"Página {page}/{data.get('last_page', '?')}: {len(facts)} fatos obtidos")
                    
                    # Verifica se chegou na última página
                    if "last_page" in data and page >= data["last_page"]:
                        break
                    
                    page += 1
                    
                else:
                    logger.warning(f"Formato de resposta inesperado: {type(data)}")
                    break
                
            except Exception as e:
                logger.error(f"Erro ao buscar página {page}: {e}")
                break
        
        logger.info(f"Total de {len(all_facts)} fatos obtidos")
        return all_facts
    
    def get_random_fact(self, animal_type: str = "cat") -> Dict:
        """
        Busca um fato aleatório.
        
        Args:
            animal_type: Tipo de animal (padrão: 'cat')
        
        Returns:
            Fato aleatório
        """
        logger.info(f"Buscando fato aleatório de {animal_type}...")
        
        params = {"animal_type": animal_type}
        data = self._make_request(Config.RANDOM_FACT_ENDPOINT, params=params)
        
        return data
    
    def close(self):
        """Fecha a sessão HTTP."""
        self.session.close()
        logger.info("API Client encerrado")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
