
# Como usar

Este script lista lotes de análises usando a API de Serviço do Grano Metrics.

## 1. Instale as dependências

O projeto já possui um arquivo `requirements.txt`, execute:

```bash
pip install -r requirements.txt
````

## 2. Configure o `.env`

Crie um arquivo `.env` na raiz do projeto com:

```env
METRICS_API_KEY="sua_api_key"
METRICS_HMAC_SECRET="seu_hmac_secret"
```

## 3. Configure a URL da API

No código, escolha a URL desejada:

```python
BASE_URL = "..."
```

Para produção, use:

```python
BASE_URL = "https://metrics-api.granosafe.com.br"
```

## 4. Execute

```bash
python main.py
```

## Listar lotes

O script usa a função:

```python
listar_lotes_de_analises(...)
```

Ela busca lotes de análises com os filtros definidos:

```python
page=1
page_size=10
search_mode="finished"
```

O `search_mode` pode ser:

* `finished`: lotes finalizados
* `in_progress`: lotes em andamento

Também é possível filtrar por etapa industrial:

```python
filter_related_equipment_industry_step="HUSK_ENTRANCE"
```

## Buscar lote por ID

Para buscar um lote específico, descomente este trecho no código:

```python
resultado_por_id = obter_lote_de_analise_por_id(
    base_url=BASE_URL,
    industry_analysis_batch_id="[meu_id_aqui]",
    api_key=API_KEY,
    hmac_secret=HMAC_SECRET,
    culture_mode=CULTURE_MODE,
)
```

## Documentação completa da API

A documentação completa está disponível com acesso autorizado ao [Console do Desenvolvedor](https://console.granosafe.com.br/docs/industry/analysis-batches).

Também, para mais opções de uso no código deste repositório, você pode ler os detalhes do que pode ser configurado na [implementação do cliente HTTP](./api.py).
