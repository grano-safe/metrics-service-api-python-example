import json
import time
import hmac
import hashlib
import secrets
import requests
from urllib.parse import urlencode
from typing import Any, Dict, Optional


def chamar_metrics_api(
    url: str,
    metodo: str,
    api_key: str,
    hmac_secret: str,
    culture_mode: str,
    payload: Optional[Any] = None,
    timeout: int = 30,
) -> Dict[str, Any]:
    """
    Faz uma requisição assinada para a API Metrics.

    Para métodos GET, HEAD e OPTIONS, a assinatura usa corpo vazio.
    Para métodos POST, PUT, PATCH e DELETE, a assinatura usa exatamente
    o corpo enviado na requisição.
    """

    metodos_com_corpo = {"POST", "PUT", "PATCH", "DELETE"}
    metodo = metodo.upper()

    if not api_key:
        raise ValueError("api_key é obrigatório.")

    if not hmac_secret:
        raise ValueError("hmac_secret é obrigatório.")

    if payload is None:
        raw_body = ""
    elif isinstance(payload, str):
        raw_body = payload
    else:
        raw_body = json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":"),
        )

    body_para_assinatura = raw_body if metodo in metodos_com_corpo else ""

    nonce = secrets.token_hex(24)
    timestamp = str(time.time_ns() // 1_000_000)
    payload_canonico = f"n:{nonce};t:{timestamp};d:{body_para_assinatura}"

    assinatura = hmac.new(
        key=hmac_secret.encode("utf-8"),
        msg=payload_canonico.encode("utf-8"),
        digestmod=hashlib.sha3_512,
    ).hexdigest()

    headers = {
        "x-metrics-nonce": nonce,
        "x-metrics-timestamp": timestamp,
        "x-metrics-signature": assinatura,
        "x-metrics-authorization": api_key,
        "x-metrics-culture-mode": culture_mode,
        "content-type": "application/json",
    }

    deve_enviar_body = metodo in metodos_com_corpo and raw_body != ""

    resposta = requests.request(
        method=metodo,
        url=url,
        headers=headers,
        data=raw_body.encode("utf-8") if deve_enviar_body else None,
        timeout=timeout,
    )

    try:
        resposta_json = resposta.json()
    except ValueError:
        resposta_json = None

    return {
        "ok": resposta.ok,
        "status_code": resposta.status_code,
        "json": resposta_json,
        "text": resposta.text,
        "headers": dict(resposta.headers),
    }


def listar_lotes_de_analises(
    base_url: str,
    api_key: str,
    hmac_secret: str,
    culture_mode: str,
    page: int = 1,
    page_size: int = 10,
    q: Optional[str] = None,
    search_mode: Optional[str] = None,
    filter_start_datetime: Optional[str] = None,
    filter_end_datetime: Optional[str] = None,
    filter_in_date: Optional[str] = None,
    filter_related_equipment_industry_step: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Lista lotes de análises industriais.

    Endpoint:
        GET /core/v1/si/industry/analysis-batches
    """

    parametros: Dict[str, str | int] = {
        "page": page,
        "pageSize": page_size,
    }

    if q:
        parametros["q"] = q

    if search_mode:
        parametros["searchMode"] = search_mode

    if filter_start_datetime:
        parametros["filter-startDatetime"] = filter_start_datetime

    if filter_end_datetime:
        parametros["filter-endDatetime"] = filter_end_datetime

    if filter_in_date:
        parametros["filter-inDate"] = filter_in_date

    if filter_related_equipment_industry_step:
        parametros[
            "filter-RelatedEquipmentIndustryStep"
        ] = filter_related_equipment_industry_step

    query_string = urlencode(parametros)

    url = f"{base_url}/core/v1/si/industry/analysis-batches?{query_string}"

    return chamar_metrics_api(
        url=url,
        metodo="GET",
        api_key=api_key,
        hmac_secret=hmac_secret,
        culture_mode=culture_mode,
    )


def obter_lote_de_analise_por_id(
    base_url: str,
    industry_analysis_batch_id: str,
    api_key: str,
    hmac_secret: str,
    culture_mode: str,
) -> Dict[str, Any]:
    """
    Obtém um lote de análises industriais pelo ID do Metrics.

    Endpoint:
        GET /core/v1/si/industry/analysis-batches/:industryAnalysisBatchId
    """

    url = (
        f"{base_url}/core/v1/si/industry/analysis-batches/"
        f"{industry_analysis_batch_id}"
    )

    return chamar_metrics_api(
        url=url,
        metodo="GET",
        api_key=api_key,
        hmac_secret=hmac_secret,
        culture_mode=culture_mode,
    )
