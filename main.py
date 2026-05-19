import os
import json

from dotenv import load_dotenv

from api import listar_lotes_de_analises, obter_lote_de_analise_por_id

load_dotenv()

# ? Configuração
BASE_URL = "https://metrics-api.granosafe.com.br"
API_KEY = os.environ["METRICS_API_KEY"]
HMAC_SECRET = os.environ["METRICS_HMAC_SECRET"]
CULTURE_MODE = "RICE_PARBO"

resultado_listagem = listar_lotes_de_analises(
    base_url=BASE_URL,
    api_key=API_KEY,
    hmac_secret=HMAC_SECRET,
    culture_mode=CULTURE_MODE,
    page=1,
    page_size=10,
    search_mode="finished", # ? finished ou in_progress
    # filter_related_equipment_industry_step="HUSK_ENTRANCE",
)

print(resultado_listagem["status_code"])

# ? Visualização simples
# print(resultado_listagem["json"])

# ? Visualização formatada
dados_formatados = json.dumps(resultado_listagem["json"], indent=2, ensure_ascii=False)

print(dados_formatados)

# ? Salvar em um arquivo JSON
# ? Salva em uma pasta "arquivos"
# os.makedirs('arquivos', exist_ok=True)
# arquivo = open('./arquivos/listagem_de_lotes_de_analises.json', 'w', encoding='utf8')
# arquivo.write(dados_formatados)
# arquivo.close()

# resultado_por_id = obter_lote_de_analise_por_id(
#     base_url=BASE_URL,
#     industry_analysis_batch_id="meu_id_aqui",
#     api_key=API_KEY,
#     hmac_secret=HMAC_SECRET,
#     culture_mode=CULTURE_MODE,
# )

# print(resultado_por_id["status_code"])
# print(resultado_por_id["json"])
