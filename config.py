"""
Configurações globais do Tanque Importer
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Caminhos
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "output"

# Garantir que os diretórios existam
for directory in [INPUT_DIR, OUTPUT_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Configurações da loja
STORE_CONFIG = {
    "domain": os.getenv("STORE_DOMAIN", "tanquedigital.com.br"),
    "currency": "BRL",
    "default_stock": int(os.getenv("DEFAULT_STOCK", "50")),
    "manage_stock": os.getenv("MANAGE_STOCK", "true").lower() == "true",
}

# Margem de lucro
MARGEM_LUCRO = float(os.getenv("MARGEM_LUCRO", "1.40"))  # 40%

# Mapeamento de categorias do catálogo para WooCommerce
CATEGORIES_MAP = {
    "BALANÇA": "Balanças",
    "CASA": "Casa e Cozinha",
    "FERRAMENTAS": "Ferramentas e Jardinagem",
    "PAPELARIA": "Papelaria e Escritório",
    "MICROFONE": "Áudio Profissional > Microfones",
    "MESA DE SOM": "Áudio Profissional > Mixers",
    "TV E TRANSMISSORES": "TV e Vídeo",
    "LOCALIZADORES": "Acessórios > Rastreadores",
    "INFORMÁTICA": "Informática e Acessórios",
    "CÂMERA": "Foto e Vídeo > Câmeras",
    "CAIXA DE SOM": "Áudio > Caixas de Som",
    "PROJETORES": "TV e Vídeo > Projetores",
    "RING LIGHT": "Foto e Vídeo > Iluminação",
    "LUMINÁRIA": "Casa e Cozinha > Iluminação",
    "CABELO": "Beleza e Cuidados > Cabelo",
    "HUB E ADAPTADOR": "Informática > Adaptadores e Hubs",
    "MEMÓRIA": "Informática > Armazenamento",
    "FONE": "Áudio > Fones de Ouvido",
    "VIDEOGAME": "Games e Consoles",
    "RELÓGIO": "Acessórios > Relógios",
    "TRIPÉ": "Foto e Vídeo > Tripés e Suportes",
    "SUPORTE": "Acessórios > Suportes",
    "CABO": "Cabos e Conectores",
    "AUTOMOTIVO": "Automotivo",
    "UTENSÍLHOS E COZINHA": "Casa e Cozinha > Utensílios",
    "QUARTO": "Casa e Decoração",
    "BELEZA E EXERCICIOS": "Beleza e Saúde",
    "MASSAGEADOR": "Beleza e Saúde > Massagem",
    "CALCULADORA": "Escritório > Calculadoras",
    "FONTE E CARREGADOR": "Eletrônicos > Carregadores",
}

# Padrões de preço psicológico
PSYCHOLOGICAL_PRICING = {
    "under_50": ".90",      # R$ X,90
    "under_200": ".99",     # R$ X,99
    "above_200": ".00",     # R$ X,00
}

# Configurações de imagens
IMAGE_CONFIG = {
    "base_url": f"https://{STORE_CONFIG['domain']}/wp-content/uploads/tomate/",
    "extension": ".jpg",
    "naming_pattern": "{sku}",  # Ex: SF-400.jpg
}

# Campos do CSV WooCommerce
WOOCOMMERCE_FIELDS = [
    "Name", "Short description", "Description", "Regular price", 
    "Sale price", "Categories", "Tags", "Images", "Stock", 
    "SKU", "Manage stock", "Stock status", "Weight", "Length", 
    "Width", "Height", "Allow reviews", "Purchase note", 
    "Sale price dates from", "Sale price dates to"
]