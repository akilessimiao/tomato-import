# src/price_calculator.py
from config import MARGEM_LUCRO

def calculate_final_price(revenda_price: str, is_promo: bool = False) -> dict:
    """
    Retorna dicionário com preço regular e preço promocional
    """
    base_price = parse_price_brl(revenda_price)
    
    # Aplica margem de 40%
    price_with_margin = base_price * MARGEM_LUCRO
    
    # Formatação psicológica (ex: 19.90)
    final_price = format_psychological_price(price_with_margin)
    
    # Lógica de Promoção
    # Se for arquivo OPAPRO, definimos o Sale Price igual ao Regular
    # para ativar o badge de oferta no WooCommerce
    if is_promo:
        return {
            "regular_price": final_price,
            "sale_price": final_price  # Ativa etiqueta de oferta
        }
    else:
        return {
            "regular_price": final_price,
            "sale_price": ""
        }