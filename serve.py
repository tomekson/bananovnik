#!/usr/bin/env python3
"""Lokální dev server pro Banánovník s SPA fallbackem.

Statický `python3 -m http.server` vrací na klientské routy (např.
/manazerska-ekonomie/) 404, protože k nim neexistuje soubor. Tenhle server
každou neznámou cestu (která není reálný soubor) podá jako index.html, takže
refresh i přímé otevření URL testu funguje stejně jako na produkci.

Použití:
    python3 serve.py                 # 0.0.0.0:8000
    python3 serve.py 8080            # vlastní port
    python3 serve.py 8080 127.0.0.1  # vlastní port + host
"""
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))


class SPAHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def send_head(self):
        path = self.translate_path(self.path)
        # Pokud cesta neukazuje na existující soubor (a není to adresář
        # s vlastním index.html), spadni na kořenový index.html.
        if not os.path.isfile(path):
            if not (os.path.isdir(path) and os.path.isfile(os.path.join(path, "index.html"))):
                self.path = "/index.html"
        return super().send_head()


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    host = sys.argv[2] if len(sys.argv) > 2 else "0.0.0.0"
    httpd = ThreadingHTTPServer((host, port), SPAHandler)
    shown = "localhost" if host in ("0.0.0.0", "") else host
    print(f"Banánovník dev server běží na http://{shown}:{port}/  (Ctrl+C ukončí)")
    if host == "0.0.0.0":
        print(f"  z jiného zařízení na síti: http://<IP-mac>:{port}/")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nKonec.")


if __name__ == "__main__":
    main()
