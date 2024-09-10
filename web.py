from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime

class WebRequestHandler(BaseHTTPRequestHandler):
    contenido = {
        '/proyecto/web-uno': """<html><h1>Proyecto: web-uno</h1></html>""",
        '/proyecto/web-dos': """<html><h1>Proyecto: web-dos</h1></html>""",
        '/proyecto/web-tres': """<html><h1>Proyecto: web-tres</h1></html>"""
    }

    def parse_path(self):
        # Separar la ruta del query string
        if '?' in self.path:
            ruta, query = self.path.split('?', 1)
        else:
            ruta, query = self.path, ''
        return ruta, query

    def query_data(self, query):
        # Procesar los datos del query string
        params = {}
        if query:
            pairs = query.split('&')
            for pair in pairs:
                key, value = pair.split('=')
                params[key] = value
        return params

    def do_GET(self):
        # Obtener la ruta y el query string
        ruta, query_string = self.parse_path()
        query = self.query_data(query_string)

        if ruta == "/":
            # Servir el archivo 'home.html' para la ruta /
            self.serve_home_page()
        elif ruta in self.contenido:
            # Servir el contenido HTML en base a la ruta y el query string
            autor = query.get("autor", "desconocido")
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            html_content = f"<h1>{self.contenido[ruta]} Autor: {autor}</h1>"
            self.wfile.write(html_content.encode("utf-8"))
        else:
            # Manejar error 404 para rutas no existentes
            self.send_response(404)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>Error 404: Pagina no encontrada</h1>")

        # Mostrar la información del request y response
        self.log_request_info()

    def serve_home_page(self):
        # Servir el contenido de 'home.html'
        try:
            with open("home.html", "r") as file:
                home_content = file.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(home_content.encode("utf-8"))
        except FileNotFoundError:
            self.send_response(500)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>Error 500: No se pudo encontrar home.html</h1>")

    def log_request_info(self):
        # Imprimir información del request y response en consola
        print(f"Request Info:")
        print(f"Host: {self.headers['Host']}")
        print(f"User-Agent: {self.headers['User-Agent']}")
        print(f"Ruta solicitada: {self.path}")

        print(f"Response Info:")
        print(f"Content-Type: text/html")
        print(f"Server: CustomPythonServer/1.0")
        print(f"Date: {datetime.now()}")

if __name__ == "__main__":
    port = 8000
    print(f"Iniciando servidor en el puerto {port}")
    server = HTTPServer(("localhost", port), WebRequestHandler)
    server.serve_forever()
