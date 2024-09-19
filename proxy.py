from http.server import BaseHTTPRequestHandler, HTTPServer
import http.client
import urllib.parse

class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the request URL
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query = parsed_url.query

        # Forward the request to localhost:8443
        conn = http.client.HTTPConnection('localhost', 8443)
        conn.request('GET', f'{path}?{query}')

        # Get the response from the target server
        response = conn.getresponse()
        data = response.read()

        # Send the response headers to the client
        self.send_response(response.status)
        for header in response.getheaders():
            self.send_header(header[0], header[1])
        self.end_headers()

        # Send the response data to the client
        self.wfile.write(data)

    def do_POST(self):
        # Handle POST requests in a similar manner
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query = parsed_url.query

        conn = http.client.HTTPConnection('localhost', 8443)
        conn.request('POST', f'{path}?{query}', body=post_data, headers=self.headers)

        response = conn.getresponse()
        data = response.read()

        self.send_response(response.status)
        for header in response.getheaders():
            self.send_header(header[0], header[1])
        self.end_headers()

        self.wfile.write(data)

def run(server_class=HTTPServer, handler_class=ProxyHandler, port=3000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting proxy server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
