"""
Parser para extrair produtos do PDF do catálogo Tomate Eletrônicos
"""
import re
import pdfplumber
from typing import List, Dict, Optional
from pathlib import Path
from tqdm import tqdm
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TomatePDFParser:
    """Parser especializado para o layout do catálogo Tomate"""
    
    # Padrões regex para extração
    PATTERNS = {
        'sku': r'^(?:SKU[:\s]*)?([A-Z]{2,}-?\d+[A-Z]?)$',
        'price': r'(?:UNID\.\s*CX:|R\$)\s*([R\$]?\s*\d+[.,]?\d*)',
        'pcs_cx': r'PCS/CX:\s*(\d+)',
        'product_name': r'^([A-Z][A-Z\s\-\.]+?)(?:\n|$)',
    }
    
    def __init__(self, pdf_path: str):
        self.pdf_path = Path(pdf_path)
        self.products: List[Dict] = []
        self.current_category: Optional[str] = None
        
    def parse(self) -> List[Dict]:
        """Extrai todos os produtos do PDF"""
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF não encontrado: {self.pdf_path}")
        
        logger.info(f"📄 Processando: {self.pdf_path.name}")
        
        with pdfplumber.open(self.pdf_path) as pdf:
            for page_num, page in enumerate(tqdm(pdf.pages, desc="Páginas"), 1):
                self._parse_page(page, page_num)
        
        logger.info(f"✅ Extraídos {len(self.products)} produtos")
        return self.products
    
    def _parse_page(self, page, page_num: int):
        """Processa uma página do PDF"""
        text = page.extract_text()
        if not text:
            return
            
        lines = text.split('\n')
        
        # Detecta mudança de categoria
        category = self._detect_category(lines)
        if category:
            self.current_category = category
            return
            
        # Extrai blocos de produto
        products_on_page = self._extract_products_from_lines(lines, page_num)
        self.products.extend(products_on_page)
    
    def _detect_category(self, lines: List[str]) -> Optional[str]:
        """Detecta título de categoria na página"""
        categories = [
            "BALANÇA", "CASA", "FERRAMENTAS", "PAPELARIA", "MICROFONE",
            "MESA DE SOM", "TV E TRANSMISSORES", "LOCALIZADORES", 
            "INFORMÁTICA", "CÂMERA", "CAIXA DE SOM", "PROJETORES",
            "RING LIGHT", "LUMINÁRIA", "CABELO", "HUB E ADAPTADOR",
            "MEMÓRIA", "FONE", "VIDEOGAME", "RELÓGIO", "TRIPÉ", 
            "SUPORTE", "CABO", "AUTOMOTIVO", "UTENSÍLHOS E COZINHA",
            "QUARTO", "BELEZA E EXERCICIOS", "MASSAGEADOR", "CALCULADORA"
        ]
        
        for line in lines[:10]:  # Categorias geralmente no topo
            line_upper = line.strip().upper()
            for cat in categories:
                if cat in line_upper and len(line_upper) < 50:
                    logger.debug(f"📁 Categoria detectada: {cat}")
                    return cat
        return None
    
    def _extract_products_from_lines(self, lines: List[str], page_num: int) -> List[Dict]:
        """Extrai produtos de uma lista de linhas"""
        products = []
        i = 0
        
        while i < len(lines) - 3:
            # Tenta identificar um bloco de produto
            product = self._try_parse_product_block(lines, i)
            
            if product and product.get('sku'):
                product['page'] = page_num
                product['category'] = self.current_category
                products.append(product)
                i += 5  # Pula linhas do produto
            else:
                i += 1
                
        return products
    
    def _try_parse_product_block(self, lines: List[str], start_idx: int) -> Optional[Dict]:
        """Tenta parsear um bloco de produto a partir de uma linha"""
        product = {}
        
        # Procura por SKU (indicador forte de produto)
        for i in range(start_idx, min(start_idx + 8, len(lines))):
            line = lines[i].strip()
            
            # Detecta SKU
            if re.match(r'^[A-Z]{2,}-?\d+[A-Z]?$', line):
                product['sku'] = line
            
            # Detecta preço
            if 'R$' in line or 'UNID. CX:' in line:
                price_match = re.search(r'R\$\s*([\d,.]+)', line)
                if price_match:
                    product['price_revenda'] = f"R${price_match.group(1)}"
            
            # Detecta PCS/CX (estoque por caixa)
            pcs_match = re.search(r'PCS/CX:\s*(\d+)', line)
            if pcs_match:
                product['pcs_per_box'] = int(pcs_match.group(1))
            
            # Nome do produto (linha em maiúsculas, não é SKU)
            if (line.isupper() and len(line) > 10 and 
                not re.match(r'^[A-Z]{2,}-?\d+', line) and
                'PCS/CX' not in line and 'UNID' not in line):
                product['name'] = line.strip()
            
            # Especificações (linhas com •)
            if line.startswith('•'):
                specs = product.get('specs', [])
                specs.append(line.replace('•', '').strip())
                product['specs'] = specs
        
        # Só retorna se tiver SKU e preço (mínimo para produto válido)
        if product.get('sku') and product.get('price_revenda'):
            return product
        return None
    
    def export_sample(self, output_path: str, limit: int = 10):
        """Exporta amostra para validação"""
        import json
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.products[:limit], f, ensure_ascii=False, indent=2)
        logger.info(f"📋 Amostra exportada: {output_path}")