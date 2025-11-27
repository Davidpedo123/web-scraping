import re
import statistics
import matplotlib.pyplot as plt
from typing import Any, Dict, List, Optional
import os

# -------------------- Utilidades --------------------
def _abbr(text: str, max_len: int = 28) -> str:
    """Abrevia un texto para usarlo como etiqueta en el gráfico."""
    if not text:
        return ""
    t = re.sub(r'\s+', ' ', text).strip()
    return (t[:max_len] + "…") if len(t) > max_len else t

def _safe_float(x: Optional[float]) -> float:
    try:
        return float(x) if x is not None else 0.0
    except:
        return 0.0# -------------------- Utilidades --------------------
def _abbr(text: str, max_len: int = 28) -> str:
    """Abrevia un texto para usarlo como etiqueta en el gráfico."""
    if not text:
        return ""
    t = re.sub(r'\s+', ' ', text).strip()
    return (t[:max_len] + "…") if len(t) > max_len else t

def _safe_float(x: Optional[float]) -> float:
    try:
        return float(x) if x is not None else 0.0
    except:
        return 0.0

def _parse_price(text: Optional[str]) -> Optional[float]:
    if not text:
        return None
    s = str(text).strip()
    # Eliminar etiquetas de moneda
    s = re.sub(r'(?i)(usd|us\$|rd\$|dop|mxn|eur|precio|desde|s/|¢|₡|€)', ' ', s)
    # Mantener dígitos, puntos, comas, k/m
    s = re.sub(r'[^\d\.,kmKM]', ' ', s).strip()
    if not s:
        return None

    # Multiplicadores (k, M)
    m = re.search(r'([\d\.,]+)\s*([kKmM])', s)
    if m:
        num = m.group(1).replace(',', '.')
        try:
            val = float(num)
            unit = m.group(2).lower()
            return val * (1_000 if unit == 'k' else 1_000_000)
        except:
            pass

    # Primer número válido
    num_match = re.search(r'(\d[\d\.,]*)', s)
    if not num_match:
        return None
    num = num_match.group(1)

    # Heurísticas para separadores
    if '.' in num and ',' in num:
        if num.find('.') < num.find(','):
            num = num.replace('.', '').replace(',', '.')
        else:
            num = num.replace(',', '')
    elif ',' in num and '.' not in num:
        num = num.replace(',', '.')
    else:
        num = num.replace(',', '')

    try:
        return float(num)
    except:
        return None

# -------------------- Procesamiento y gráficos --------------------
async def diff_price(page1_data, page2_data, page3_data, usd_to_dop: float = 63.0) -> Dict[str, Any]:
    """
    page1/page3: precios ya en DOP
    page2: precios en USD -> convertir a DOP
    """
  
    pages: Dict[str, List[Dict[str, Any]]] = {
        "kicks.com": page1_data or [],
        "nike.com": page2_data or [],
        "citytenis.online": page3_data or [],
    }

    results: Dict[str, Dict[str, Any]] = {}
    all_products: List[Dict[str, Any]] = []

    # Parseo y conversión
    for site_name, items in pages.items():
        prices: List[float] = []
        parsed_items: List[Dict[str, Any]] = []

        for it in items:
            name = (it.get("nombre") or it.get("name") or it.get("title") or "") if isinstance(it, dict) else ""
            raw = (it.get("precio") or it.get("price") or "") if isinstance(it, dict) else ""
            price = _parse_price(raw)

          
            if price is not None and site_name == "nike.com":
                price *= usd_to_dop

            if price is not None:
                prices.append(price)

            parsed = {"name": name, "price": price, "raw": raw, "site": site_name}
            parsed_items.append(parsed)
            if price and price > 0:
                all_products.append(parsed)

        avg = float(statistics.mean(prices)) if prices else None
        results[site_name] = {"average": avg, "count_prices": len(prices), "parsed": parsed_items}

    # Calcular extremos por sitio
    extremes: Dict[str, Dict[str, Any]] = {}
    for site_name in pages.keys():
        valid = [p for p in results[site_name]["parsed"] if p["price"] and p["price"] > 0]
        cheapest = min(valid, key=lambda x: x["price"]) if valid else None
        most_expensive = max(valid, key=lambda x: x["price"]) if valid else None
        extremes[site_name] = {
            "cheapest": {"name": cheapest["name"], "price": cheapest["price"]} if cheapest else None,
            "most_expensive": {"name": most_expensive["name"], "price": most_expensive["price"]} if most_expensive else None,
            "count": len(valid)
        }

    # ---- Gráfico 1: extremos (min vs max) por sitio ----
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'logs', 'html'))
    os.makedirs(out_dir, exist_ok=True)

    labels = list(extremes.keys())
    cheap_values = [_safe_float(extremes[k]["cheapest"]["price"]) if extremes[k]["cheapest"] else 0 for k in labels]
    expensive_values = [_safe_float(extremes[k]["most_expensive"]["price"]) if extremes[k]["most_expensive"] else 0 for k in labels]

    fig_path_extremes = os.path.join(out_dir, "extremes.png")
    fig, ax = plt.subplots(figsize=(9, 5))
    x = range(len(labels))
    bar_width = 0.4

    ax.bar([i - bar_width/2 for i in x], cheap_values, width=bar_width, color='#4CAF50', label='Más barato')
    ax.bar([i + bar_width/2 for i in x], expensive_values, width=bar_width, color='#F44336', label='Más caro')

    # Etiquetas con precio
    top_val = max(expensive_values) if expensive_values else 0
    offset = top_val * 0.015 if top_val > 0 else 1.0
    for i, v in enumerate(cheap_values):
        ax.text(i - bar_width/2, v + offset, f"{v:.2f}", ha='center', fontsize=8)
    for i, v in enumerate(expensive_values):
        ax.text(i + bar_width/2, v + offset, f"{v:.2f}", ha='center', fontsize=8)

    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_ylabel("Precio (DOP)")
    ax.set_title("Precio más barato vs más caro por sitio")
    ax.legend()
    plt.tight_layout()
    plt.savefig(fig_path_extremes)
    plt.close(fig)

    # ---- Gráfico 2: versión 'summary' (extremes_summary.png) con nombres abreviados y counts ----
    fig_path_summary = os.path.join(out_dir, "extremes_summary.png")
    fig, ax = plt.subplots(figsize=(11, 6))
    x = range(len(labels))
    bar_width = 0.4

    ax.bar([i - bar_width/2 for i in x], cheap_values, width=bar_width, color='#2E7D32', label='Más barato')
    ax.bar([i + bar_width/2 for i in x], expensive_values, width=bar_width, color='#C62828', label='Más caro')

    # Etiquetas con nombre abreviado + precio
    for i, site in enumerate(labels):
        cheap = extremes[site]["cheapest"]
        exp = extremes[site]["most_expensive"]
        cheap_label = _abbr(cheap["name"]) if cheap else "N/A"
        exp_label = _abbr(exp["name"]) if exp else "N/A"
        ax.text(i - bar_width/2, cheap_values[i] + offset, f"{cheap_label}\n{cheap_values[i]:.0f}", 
                ha='center', va='bottom', fontsize=8, rotation=0)
        ax.text(i + bar_width/2, expensive_values[i] + offset, f"{exp_label}\n{expensive_values[i]:.0f}", 
                ha='center', va='bottom', fontsize=8, rotation=0)

        # Nota de conteo debajo de cada cluster
        ax.text(i, 0 - (top_val * 0.05 if top_val > 0 else 5), f"count: {extremes[site]['count']}",
                ha='center', va='top', fontsize=8, color='#616161')

    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_ylabel("Precio (DOP)")
    ax.set_title("Resumen por sitio: extremos (con nombres) y conteo")
    ax.legend()
    plt.tight_layout()
    plt.savefig(fig_path_summary)
    plt.close(fig)

    # ---- Gráfico 3: counts por sitio ----
    fig_path_counts = os.path.join(out_dir, "counts.png")
    counts = [extremes[k]["count"] for k in labels]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(labels, counts, color='#1976D2')
    for i, v in enumerate(counts):
        ax.text(i, v + max(counts) * 0.03 if max(counts) > 0 else v + 0.5, str(v), ha='center', fontsize=9)
    ax.set_ylabel("Cantidad de productos válidos")
    ax.set_title("Conteo de ítems analizados por sitio")
    plt.tight_layout()
    plt.savefig(fig_path_counts)
    plt.close(fig)

    # Resumen final
    summary = {
        "extremes": extremes,                # datos por sitio
        "charts": {
            "extremes": fig_path_extremes,   # min vs max (precios)
            "summary": fig_path_summary,     # min/max con nombres + conteos
            "counts": fig_path_counts        # solo conteos
        }
    }
    return summary
