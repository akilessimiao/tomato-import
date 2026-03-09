# config.py
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ... (caminhos permanecem iguais) ...

# 💰 Configurações de Preço
MARGEM_LUCRO = float(os.getenv("MARGEM_LUCRO", "1.40"))  # 40%
ARREDONDAMENTO_PSICOLOGICO = True

# 🏷️ Configurações de Promoção
PROMO_FILENAME_PATTERN = os.getenv("PROMO_PATTERN", "OPAPRO")  # Arquivos que começam assim
PROMO_TAG = "Promoção"
PROMO_CATEGORY = "Ofertas"

# ... (resto do config) ...