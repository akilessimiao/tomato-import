"""
Gera CSV compatível com WooCommerce Importer
"""
import csv
import logging
from typing import List, Dict
from pathlib import Path
from config import WOOCOMMERCE_FIELDS, CATEGORIES_MAP, IMAGE_CONFIG, STORE_CONFIG

logger = logging.getLogger(__name__)


class WooCommerceCSVGenerator:
    """Gera CSV no formato oficial do WooCommerce"""
    
    def __init__(self, output_path: str):
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        
    def generate(self, products: List[Dict]) -> str:
        """Gera o CSV final"""
        with open(self.output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=WOOCOMMERCE_FIELDS, quoting=csv.QUOTE_MINIMAL)
            writer.writeheader()
            
            for product in products:
                row = self._build_product_row(product)
                writer.writerow(row)
        
        logger.info(f"✅ CSV gerado: {self.output_path} ({len(products)} produtos)")
        return str(self.output_path)
    
    def _build_product_row(self, product: Dict) -> Dict:
        """Constrói uma linha do CSV para um produto"""
        from src.price_calculator import calculate_final_price
        
        # Nome e descrições
        name = product.get('name', product.get('sku', 'Produto sem nome'))
        short_desc = product.get('specs', [''])[0][:160] if product.get('specs') else name
        description = self._format_description_html(product)
        
        # Preço
        regular_price = calculate_final_price(product.get('price_revenda', '0'))
        
        # Categoria
        raw_category = product.get('category', 'Geral')
        category = CATEGORIES_MAP.get(raw_category, 'Geral')
        
        # Tags
        tags = ';'.join([
            product.get('sku', '').lower(),
            category.lower().split(' > ')[-1],
            'tomate-eletronicos',
            'importado'
        ])
        
        # Imagem
        image_url = self._build_image_url(product.get('sku'))
        
        # Estoque
        pcs = product.get('pcs_per_box', STORE_CONFIG['default_stock'])
        stock = pcs * 10  # Estimativa: 10 caixas como estoque inicial
        
        return {
            'Name': name,
            'Short description': short_desc,
            'Description': description,
            'Regular price': regular_price,
            'Sale price': '',
            'Categories': category,
            'Tags': tags,
            'Images': image_url,
            'Stock': stock,
            'SKU': product.get('sku', ''),
            'Manage stock': '1' if STORE_CONFIG['manage_stock'] else '0',
            'Stock status': 'instock',
            'Weight': '',
            'Length': '',
            'Width': '',
            'Height': '',
            'Allow reviews': '1',
            'Purchase note': 'Produto importado do catálogo Tomate Eletrônicos. Consulte disponibilidade.',
            'Sale price dates from': '',
            'Sale price dates to': '',
        }
    
    def _format_description_html(self, product: Dict) -> str:
        """Formata especificações como HTML para WooCommerce"""
        specs = product.get('specs', [])
        if not specs:
            return product.get('name', '')
        
        html = '<ul style="margin:0;padding-left:20px;">'
        for spec in specs[:8]:  # Limita a 8 itens
            html += f'<li>{spec}</li>'
        html += '</ul>'
        return html
    
    def _build_image_url(self, sku: str) -> str:
        """Gera URL da imagem no padrão da loja"""
        if not sku:
            return ''
        pattern = IMAGE_CONFIG['naming_pattern']
        filename = pattern.format(sku=sku.lower()) + IMAGE_CONFIG['extension']
        return IMAGE_CONFIG['base_url'] + filename