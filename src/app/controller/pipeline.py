from service.consultHTTP import consult_page1, consult_page2, consult_page3
import os

async def run_pipeline():
    page1_data = await consult_page1()
    page2_data = await consult_page2()
    page3_data = await consult_page3()

    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'logs', 'html'))
    os.makedirs(out_dir, exist_ok=True)

    def _save_html(name, content):
        path = os.path.join(out_dir, f"{name}.html")
        if isinstance(content, (bytes, bytearray)):
            with open(path, 'wb') as f:
                f.write(content)
        else:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(str(content))
        return path

    p1_path = _save_html('page1', page1_data)
    p2_path = _save_html('page2', page2_data)
    p3_path = _save_html('page3', page3_data)

    return p1_path, p2_path, p3_path