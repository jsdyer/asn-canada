"""Exercise the built starter at a project subpath in Chromium."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import shutil
import tempfile
import threading
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def main():
    screenshots = ROOT / "browser-checks"
    screenshots.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as temporary:
        shutil.copytree(ROOT / "dist", Path(temporary) / "example-tool")
        server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=temporary))
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page(viewport={"width": 1280, "height": 1000})
                errors = []
                page.on("pageerror", lambda error: errors.append(str(error)))
                page.goto(f"http://127.0.0.1:{server.server_port}/example-tool/")
                page.wait_for_function("document.querySelector('#title').textContent.includes('AS852')")
                page.fill('#query','TELUS')
                assert page.locator('#network option').count() >= 1
                page.select_option('#family','v4')
                assert page.locator('#lengths').get_by_text('IPv4 /24',exact=True).count() == 1
                page.fill('#query','no-such-asn-name-here')
                assert page.locator('#title').inner_text() == 'No matching network'
                page.fill('#query','AS852')
                with page.expect_download() as out:
                    page.click('#export')
                assert out.value.suggested_filename.endswith('.csv')
                page.screenshot(path=str(screenshots / "desktop.png"), full_page=True)
                page.set_viewport_size({"width": 390, "height": 844})
                assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
                page.screenshot(path=str(screenshots / "mobile.png"), full_page=True)
                assert not errors, errors
                browser.close()
            print("Browser checks passed: source-backed interaction, CSV and mobile layout")
        finally:
            server.shutdown()


if __name__ == "__main__":
    main()
