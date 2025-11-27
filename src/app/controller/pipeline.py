
from service.consultHTTP import consult_page1, consult_page2, consult_page3
from service.transformerData import diff_price

from typing import Any, Dict, List, Optional


# -------------------- Función principal del pipeline --------------------
async def run_pipeline(usd_to_dop: float = 63.0) -> Dict[str, Any]:
    """
    Orquesta la consulta de datos y el análisis completo:
    1. Consulta las tres páginas.
    2. Procesa los precios y genera estadísticas.
    3. Devuelve un resumen con extremos y gráficos.
    """
    page1_data = await consult_page1()  
    page2_data = await consult_page2()  
    page3_data = await consult_page3()  

    summary = await diff_price(page1_data, page2_data, page3_data, usd_to_dop)
    return summary


