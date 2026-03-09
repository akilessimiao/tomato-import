# main.py
# ... imports ...
from config import PROMO_FILENAME_PATTERN

def main():
    # ... (argparse setup) ...
    args = parser.parse_args()
    
    # Detecta se é arquivo de promoção pelo nome
    filename = Path(args.pdf).name.upper()
    is_promo = filename.startswith(PROMO_FILENAME_PATTERN)
    
    if is_promo:
        logger.info("🏷️ Arquivo de PROMOÇÃO detectado (OPAPRO).")
    else:
        logger.info("📦 Arquivo de CATÁLOGO GERAL detectado.")

    # ... (parser setup) ...
    
    # Passa o flag para o gerador de CSV
    csv_generator = WooCommerceCSVGenerator(args.output, is_promo_file=is_promo)
    output_file = csv_generator.generate(products)
    
    # ... (resto do script) ...