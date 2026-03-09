#!/usr/bin/env python3
"""
Tanque Digital - Tomate Importer
================================
Script principal para importar produtos do catálogo Tomate Eletrônicos
para loja WooCommerce.

Uso:
    python main.py --pdf caminho/para/catalogo.pdf --output dados/produtos.csv

Autor: Akiles Simião | Tanque Digital
GitHub: github.com/akilessimiao
"""
import argparse
import sys
import logging
from pathlib import Path
from config import OUTPUT_DIR
from src.pdf_parser import TomatePDFParser
from src.csv_generator import WooCommerceCSVGenerator

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(OUTPUT_DIR / 'import.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description='Importador Tomate Eletrônicos → WooCommerce',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  %(prog)s --pdf catalogo.pdf
  %(prog)s --pdf catalogo.pdf --output meus_produtos.csv
  %(prog)s --pdf catalogo.pdf --sample  # Gera amostra para validação
        """
    )
    
    parser.add_argument(
        '--pdf', '-p', 
        required=True, 
        help='Caminho para o PDF do catálogo Tomate'
    )
    parser.add_argument(
        '--output', '-o',
        default=OUTPUT_DIR / 'tanque_produtos.csv',
        help='Caminho para o CSV de saída (padrão: data/output/tanque_produtos.csv)'
    )
    parser.add_argument(
        '--sample', '-s',
        action='store_true',
        help='Gera apenas amostra de 10 produtos para validação'
    )
    parser.add_argument(
        '--validate', '-v',
        action='store_true',
        help='Valida o CSV gerado sem importar'
    )
    
    args = parser.parse_args()
    
    try:
        logger.info("🚀 Iniciando importação Tomate → Tanque Digital")
        
        # 1. Parse do PDF
        logger.info("📄 Extraindo dados do PDF...")
        pdf_parser = TomatePDFParser(args.pdf)
        products = pdf_parser.parse()
        
        if not products:
            logger.error("❌ Nenhum produto extraído. Verifique o PDF.")
            return 1
        
        # 2. Amostra para validação (opcional)
        if args.sample:
            sample_path = OUTPUT_DIR / 'amostra_validacao.json'
            pdf_parser.export_sample(str(sample_path))
            logger.info(f"✅ Amostra gerada: {sample_path}")
            logger.info("🔍 Revise a amostra antes de prosseguir com a importação completa.")
            return 0
        
        # 3. Geração do CSV WooCommerce
        logger.info("📊 Gerando CSV compatível com WooCommerce...")
        csv_generator = WooCommerceCSVGenerator(args.output)
        output_file = csv_generator.generate(products)
        
        # 4. Validação (opcional)
        if args.validate:
            logger.info("🔍 Validando CSV gerado...")
            if _validate_csv(output_file):
                logger.info("✅ Validação concluída com sucesso!")
            else:
                logger.warning("⚠️ Validação identificou possíveis problemas. Revise o CSV.")
        
        # 5. Resumo final
        logger.info("\n" + "="*60)
        logger.info("📋 RESUMO DA IMPORTAÇÃO")
        logger.info("="*60)
        logger.info(f"✅ Produtos processados: {len(products)}")
        logger.info(f"📁 Arquivo de saída: {output_file}")
        logger.info(f"💰 Margem aplicada: 40%")
        logger.info(f"🛒 Loja: {Path(args.output).parent}")
        logger.info("\n📦 Próximos passos:")
        logger.info("   1. Faça upload das imagens para: wp-content/uploads/tomate/")
        logger.info("   2. No WordPress: Produtos > Importar > Selecione o CSV")
        logger.info("   3. Marque 'Atualizar produtos existentes' se necessário")
        logger.info("   4. Execute a importação e revise os produtos")
        logger.info("="*60 + "\n")
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"❌ Arquivo não encontrado: {e}")
        return 1
    except Exception as e:
        logger.exception(f"❌ Erro inesperado: {e}")
        return 1


def _validate_csv(filepath: str) -> bool:
    """Validação básica do CSV gerado"""
    import csv
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
        if not rows:
            logger.error("CSV vazio!")
            return False
            
        # Verifica campos obrigatórios
        required = ['Name', 'Regular price', 'SKU', 'Categories']
        for row in rows[:5]:  # Testa primeiras 5 linhas
            for field in required:
                if not row.get(field):
                    logger.warning(f"Campo '{field}' vazio na linha {rows.index(row)+2}")
                    return False
        
        logger.info(f"✓ CSV válido: {len(rows)} linhas, campos obrigatórios OK")
        return True
    except Exception as e:
        logger.error(f"Erro na validação: {e}")
        return False


if __name__ == '__main__':
    sys.exit(main())