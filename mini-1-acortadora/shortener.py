#!/usr/bin/env python3
from urllib.parse import parse_qs
import shelve
import os

from webapp import webApp # fichero webapp.py con la clase webapp

class ShortenerApp(webApp): # hereda de la clase webapp
    def existe_shelve(self, nombre):
        extensiones = ["", ".db", ".dat", ".dir", ".bak"]
        for ext in extensiones:
            if os.path.exists(nombre + ext):
                return True
        return False

    def listar_urls(self):
        if not self.existe_shelve("acortador"):
            return "<ul></ul>"

        lista_urls = "<ul>"
        with shelve.open("acortador") as db:
            for alias in db:
                lista_urls += f"<li>http://localhost:1233/{alias} -&gt; {db[alias]['url']}</li>"
        lista_urls += "</ul>"
        return lista_urls

    def handle_getbarra(self, respuesta):
        return ("200 OK", respuesta.format(
            mensaje="",
            lista_urls=self.listar_urls()
        ))

    def handle_postbarra(self, respuesta, body):
        parametros = parse_qs(body)
        url = parametros.get("url", [""])[0].strip()
        alias = parametros.get("alias", [""])[0].strip()

        if alias == "":
            return ("400 Bad Request", respuesta.format(
                mensaje="ERROR: alias no proporcionado",
                lista_urls=self.listar_urls()
            ))
        if alias == "stats":
            return ("400 Bad Request", respuesta.format(
                mensaje="ERROR: alias 'stats' no permitido",
                lista_urls=self.listar_urls()
            ))
        with shelve.open("acortador") as db:
            db[alias] = {
                "url": url,
                "contador": 0
            }

        return ("200 OK", respuesta.format(
            mensaje="URL guardada correctamente",
            lista_urls=self.listar_urls()
        ))

    def handle_getalias(self, recurso):
        alias = recurso[1:]

        with shelve.open("acortador", writeback=True) as db:
            if alias in db:
                url_original_fich = db[alias]["url"]
                db[alias]["contador"] += 1

                respuesta_redireccion = f"""
                <html>
                  <head>
                    <meta charset="utf-8">
                    <meta http-equiv="refresh" content="0; url={url_original_fich}">
                    <title>Redirigiendo...</title>
                  </head>
                  <body>
                    <p>Redirigiendo a la URL original...</p>
                  </body>
                </html>
                """
                return ("302 Found", respuesta_redireccion)

        return ("404 Not Found", "<html><body><h1>Alias no encontrado</h1></body></html>")

    def handle_getstats(self, recurso):
        alias = recurso.split("/")[2]

        with shelve.open("acortador") as db:
            if alias in db:
                contador = db[alias]["contador"]
                respuesta_contador = f"""
                <html>
                  <body>
                    <h1>Numero de veces que se ha redireccionado: {contador}</h1>
                  </body>
                </html>
                """
                return ("200 OK", respuesta_contador)

        return ("404 Not Found", "<html><body><h1>Alias no encontrado</h1></body></html>")

    def analyze(self, request):
        primera_linea = request.split("\r\n")[0]
        partes = primera_linea.split()

        if len(partes) < 2:
            return "", "", ""

        metodo = partes[0]
        recurso = partes[1]

        print(metodo, recurso)

        body = ""
        if "\r\n\r\n" in request:
            body = request.split("\r\n\r\n", 1)[1]

        return metodo, recurso, body

    def compute(self, request_analyzed):
        respuesta = """
        <html>
          <body>
            <h1>Acortador de URLs</h1>
            <form action="/" method="POST">
              <label>URL:</label>
              <input type="text" name="url"><br><br>
              <label>Alias:</label>
              <input type="text" name="alias"><br><br>
              <input type="submit" value="Enviar">
            </form>
            <p>{mensaje}</p>
            <h2>URLs acortadas</h2>
            {lista_urls}
          </body>
        </html>
        """

        metodo, recurso, body = request_analyzed

        if metodo == "GET" and recurso == "/":
            return self.handle_getbarra(respuesta)

        elif metodo == "POST" and recurso == "/":
            return self.handle_postbarra(respuesta, body)

        elif metodo == "GET" and recurso.startswith("/stats/"):
            return self.handle_getstats(recurso)

        elif metodo == "GET" and recurso.startswith("/") and recurso != "/":
            return self.handle_getalias(recurso)

        return ("404 Not Found", "<html><body><h1>Error 404</h1></body></html>")


if __name__ == '__main__':
    app = ShortenerApp(1233, "localhost")