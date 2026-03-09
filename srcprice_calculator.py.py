"""
Módulo para cálculo de preços com margem e formatação psicológica
"""
import re
from config import MARGEM_LUCRO, PSYCHOLOGICAL_PRICING


def parse_price_brl(price_str: str) -> float:
    """
    Converte string de preço BRL para float
    Ex: 'R$14.00' -> 14.00 | 'R$ 1.250,50' -> 1250.50
    """
    if not price_str:
        return 0.0
    
    # Remove símbolos e espaços
    clean = re.sub(r'[R$\s]', '', str(price_str).strip())
    
    # Substitui vírgula por ponto para conversão
    clean = clean.replace(',', '.')
    
    try:
        return float(clean)
    except ValueError:
        return 0.0


def apply_margin(price: float, margin: float = MARGEM_LUCRO) -> float:
    """Aplica margem de lucro sobre o preço base"""
    return price * margin


def format_psychological_price(price: float) -> str:
    """
    Formata preço com estratégia psicológica:
    - < R$50: termina em ,90
    - < R$200: termina em ,99
    - >= R$200: termina em ,00
    """
    if price < 50:
        suffix = PSYCHOLOGICAL_PRICING["under_50"]
    elif price < 200:
        suffix = PSYCHOLOGICAL_PRICING["under_200"]
    else:
        suffix = PSYCHOLOGICAL_PRICING["above_200"]
    
    # Arredonda para inteiro e adiciona sufixo
    return f"{int(price)}{suffix}"


def calculate_final_price(revenda_price: str, margin: float = MARGEM_LUCRO) -> str:
    """
    Pipeline completo: parse -> margem -> formatação psicológica
    """
    base_price = parse_price_brl(revenda_price)
    price_with_margin = apply_margin(base_price, margin)
    return format_psychological_price(price_with_margin)


# Testes rápidos
if __name__ == "__main__":
    test_cases = [
        ("R$14.00", "19.90"),
        ("R$ 395,00", "553.00"),
        ("R$1.250,50", "1750.00"),
    ]
    
    print("🧪 Testes de cálculo de preço:")
    for revenda, esperado in test_cases:
        resultado = calculate_final_price(revenda)
        status = "✅" if resultado == esperado else "❌"
        print(f"{status} {revenda} -> R$ {resultado} (esperado: R$ {esperado})")