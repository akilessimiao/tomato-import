# 🛒 Tanque Digital - Tomate Importer

> Script profissional para importar produtos do catálogo **Tomate Eletrônicos** para loja WooCommerce.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![WooCommerce](https://img.shields.io/badge/WooCommerce-Compatível-96588a.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Funcionalidades

- ✅ Extração automática de produtos de PDF
- ✅ Cálculo de preço com margem de 40% + preço psicológico
- ✅ Geração de CSV 100% compatível com WooCommerce Importer
- ✅ Mapeamento inteligente de categorias
- ✅ URLs de imagens no padrão da loja
- ✅ Logging detalhado e tratamento de erros
- ✅ Modo de validação e amostra para testes

## 🚀 Instalação Rápida

```bash
# 1. Clone o repositório
git clone https://github.com/akilessimiao/tomate-importer.git
cd tomate-importer

# 2. Crie ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 3. Instale dependências
pip install -r requirements.txt

# 4. Configure variáveis de ambiente (opcional)
cp .env.example .env
# Edite .env com suas configurações
