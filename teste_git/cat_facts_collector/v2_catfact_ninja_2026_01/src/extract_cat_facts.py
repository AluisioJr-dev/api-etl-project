"""
Script principal de extração de Cat Facts da API.

Este script extrai dados de fatos sobre gatos da Cat Facts API
e salva em formato CSV para análise local.

Uso:
    python src/extract_cat_facts.py

Autor: UOLCatLovers Data Engineering Team
Data: 2026-01-26
"""

import sys
from pathlib import Path
from typing import List, Dict
from datetime import datetime

import pandas as pd
from pydantic import ValidationError

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import Config
from src.utils.logger import setup_logger
from src.utils.api_client import CatFactsAPIClient
from src.models import CatFact


# Configuração do logger
logger = setup_logger(
    name="cat_facts_extraction",
    log_level=Config.LOG_LEVEL,
    log_file=Config.LOG_FILE
)


class CatFactsExtractor:
    """Classe responsável pela extração e processamento de Cat Facts."""
    
    def __init__(self):
        """Inicializa o extrator."""
        self.api_client = CatFactsAPIClient()
        self.facts: List[CatFact] = []
        
    def extract(self) -> List[Dict]:
        """
        Extrai os dados da API.
        
        Returns:
            Lista de fatos em formato de dicionário
        """
        logger.info("=" * 60)
        logger.info("INICIANDO EXTRAÇÃO DE CAT FACTS")
        logger.info("=" * 60)
        
        try:
            # Busca todos os fatos da API
            raw_facts = self.api_client.get_all_facts(animal_type="cat")
            logger.info(f"Total de registros recebidos da API: {len(raw_facts)}")
            
            if not raw_facts:
                logger.warning("Nenhum fato retornado pela API")
                return []
            
            # Valida e transforma os dados
            validated_facts = self._validate_and_transform(raw_facts)
            
            logger.info(f"Total de registros validados: {len(validated_facts)}")
            return validated_facts
            
        except Exception as e:
            logger.error(f"Erro durante a extração: {e}", exc_info=True)
            raise
    
    def _validate_and_transform(self, raw_facts: List[Dict]) -> List[Dict]:
        """
        Valida e transforma os dados brutos usando Pydantic.
        
        Args:
            raw_facts: Lista de dicionários brutos da API
        
        Returns:
            Lista de dicionários validados e transformados
        """
        logger.info("Validando e transformando dados...")
        
        # Timestamp de extração (mesmo para todos os registros desta execução)
        from datetime import datetime, timezone
        extraction_time = datetime.now(timezone.utc)
        
        validated_facts = []
        errors_count = 0
        
        for i, fact_data in enumerate(raw_facts, 1):
            try:
                # Valida usando o modelo Pydantic
                fact = CatFact(**fact_data)
                fact.extracted_at = extraction_time  # Adiciona timestamp de extração
                validated_facts.append(fact.to_dict())
                
                if i % 100 == 0:
                    logger.debug(f"Processados {i}/{len(raw_facts)} registros")
                    
            except ValidationError as e:
                errors_count += 1
                logger.warning(f"Erro de validação no registro {i}: {e}")
                
            except Exception as e:
                errors_count += 1
                logger.error(f"Erro inesperado no registro {i}: {e}")
        
        if errors_count > 0:
            logger.warning(f"Total de registros com erro: {errors_count}")
        
        logger.info(f"Validação concluída: {len(validated_facts)} registros válidos")
        return validated_facts
    
    def save_to_csv(self, facts: List[Dict], output_path: Path) -> None:
        """
        Salva os dados em arquivo CSV.
        
        Args:
            facts: Lista de fatos a serem salvos
            output_path: Caminho do arquivo de saída
        """
        if not facts:
            logger.warning("Nenhum dado para salvar")
            return
        
        logger.info(f"Salvando dados em CSV: {output_path}")
        
        try:
            # Cria DataFrame
            df = pd.DataFrame(facts)
            
            # Remove duplicatas baseado no ID
            original_count = len(df)
            df = df.drop_duplicates(subset=['id'], keep='first')
            duplicates_removed = original_count - len(df)
            
            if duplicates_removed > 0:
                logger.info(f"Removidas {duplicates_removed} duplicatas")
            
            # Ordena por data de atualização
            if 'updated_at' in df.columns:
                df = df.sort_values('updated_at', ascending=False)
            
            # Salva em CSV
            df.to_csv(output_path, index=False, encoding='utf-8')
            
            logger.info(f"✓ Dados salvos com sucesso: {len(df)} registros")
            logger.info(f"✓ Arquivo: {output_path}")
            
            # Exibe estatísticas
            self._display_statistics(df)
            
        except Exception as e:
            logger.error(f"Erro ao salvar CSV: {e}", exc_info=True)
            raise
    
    def _display_statistics(self, df: pd.DataFrame) -> None:
        """
        Exibe estatísticas sobre os dados extraídos.
        
        Args:
            df: DataFrame com os dados
        """
        logger.info("")
        logger.info("=" * 60)
        logger.info("ESTATÍSTICAS DOS DADOS")
        logger.info("=" * 60)
        
        logger.info(f"Total de registros: {len(df)}")
        logger.info(f"Total de colunas: {len(df.columns)}")
        logger.info(f"Tamanho do arquivo: {Config.get_output_path().stat().st_size / 1024:.2f} KB")
        
        if 'type' in df.columns:
            logger.info(f"\nDistribuição por tipo:")
            for type_name, count in df['type'].value_counts().items():
                logger.info(f"  - {type_name}: {count}")
        
        if 'created_at' in df.columns and df['created_at'].notna().any():
            try:
                df['created_date'] = pd.to_datetime(df['created_at'])
                min_date = df['created_date'].min()
                max_date = df['created_date'].max()
                logger.info(f"\nPeríodo dos dados:")
                logger.info(f"  - Data mais antiga: {min_date}")
                logger.info(f"  - Data mais recente: {max_date}")
            except Exception as e:
                logger.debug(f"Não foi possível calcular período: {e}")
        
        if 'upvotes' in df.columns:
            total_upvotes = df['upvotes'].sum()
            avg_upvotes = df['upvotes'].mean()
            logger.info(f"\nUpvotes:")
            logger.info(f"  - Total: {total_upvotes}")
            logger.info(f"  - Média: {avg_upvotes:.2f}")
        
        logger.info("=" * 60)
    
    def run(self) -> None:
        """Executa o fluxo completo de extração."""
        start_time = datetime.now()
        
        try:
            # Garante que os diretórios existem
            Config.ensure_directories()
            
            # Exibe configurações
            logger.info("Configurações:")
            for key, value in Config.display_config().items():
                logger.info(f"  {key}: {value}")
            logger.info("")
            
            # Extrai os dados
            facts = self.extract()
            
            # Salva em CSV
            output_path = Config.get_output_path()
            self.save_to_csv(facts, output_path)
            
            # Tempo de execução
            elapsed_time = datetime.now() - start_time
            logger.info("")
            logger.info("=" * 60)
            logger.info(f"✓ EXTRAÇÃO CONCLUÍDA COM SUCESSO")
            logger.info(f"✓ Tempo de execução: {elapsed_time}")
            logger.info("=" * 60)
            
        except Exception as e:
            logger.error("")
            logger.error("=" * 60)
            logger.error(f"✗ FALHA NA EXTRAÇÃO: {e}")
            logger.error("=" * 60)
            raise
            
        finally:
            # Fecha o cliente da API
            self.api_client.close()


def main():
    """Função principal."""
    try:
        extractor = CatFactsExtractor()
        extractor.run()
        sys.exit(0)
        
    except KeyboardInterrupt:
        logger.warning("\nExtração interrompida pelo usuário")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"Erro fatal: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
