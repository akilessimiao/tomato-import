# Importação completa
python main.py --pdf data/input/TOMATE_GERAL.pdf

# Com saída personalizada
python main.py --pdf catalogo.pdf --output loja/produtos.csv

# Modo validação (gera amostra de 10 produtos)
python main.py --pdf catalogo.pdf --sample

# Validar CSV sem importar
python main.py --pdf catalogo.pdf --validate