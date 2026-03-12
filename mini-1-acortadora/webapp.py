#!/usr/bin/env python3
import socket


class webApp:
    def compute(self, request_analyzed):
        return ("200 OK", "<html><body><h1>Funciona!</h1></body></html>")

    def analyze(self, request):
        return request.split()[1]

    def __init__(self, port, host):
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((host, port))
        servidor.listen(5)

        while True:
            print("Esperando conexion...")
            cliente, addr = servidor.accept()
            print("Conexión establecida")

            request = cliente.recv(2048).decode("utf-8")

            if not request.strip():
                cliente.close()
                continue

            request_analyzed = self.analyze(request)
            codigo, request_computed = self.compute(request_analyzed)

            respuesta_final = "HTTP/1.1 " + codigo + "\r\n"
            respuesta_final += "Content-Type: text/html; charset=utf-8\r\n"
            respuesta_final += "Content-Length: " + str(len(request_computed.encode("utf-8"))) + "\r\n"
            respuesta_final += "\r\n"
            respuesta_final += request_computed

            cliente.send(respuesta_final.encode("utf-8"))
            print("Cerrando conexión del cliente")
            cliente.close()


if __name__ == '__main__':
    app = webApp(1233, "localhost")