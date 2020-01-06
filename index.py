from http.server import HTTPServer, BaseHTTPRequestHandler
from selenium import webdriver
import cgi
from screen_capture import ScreenCapture
from datetime import datetime
from PIL import Image
import io
import requests
import urllib.parse as urlparse
from urllib.parse import parse_qs
import re
from fpdf import FPDF

browser = webdriver.Chrome('chromedriver.exe')
browser.set_window_size(1280,1000)
class Serv(BaseHTTPRequestHandler):
    specialCount = 0
    def do_GET(self):
        
        parsed = urlparse.urlparse(self.path)
        get = parse_qs(parsed.query)
        if parsed.path == '/count/':
            self.specialCount+=1
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes('COUNT '+str(self.specialCount),'utf-8'))
        elif parsed.path == '/get-capture/':
            url = get['url'][0]
            if(self.checkValidUrl(url) == False):
                return self.response(404,'Invalid url')

            
            browser.get(url)
            fileName = 'output/file'+datetime.now().strftime("%H%M%S")+'.jpg'
            ScreenCapture.fullpage_screenshot(browser,fileName, False)

            # image = Image.open(fileName,mode='r')

            streamFile = io.BytesIO()
            # image.save(streamFile, format='PNG')

            pdf = FPDF()
            pdf.add_page()
            pdf.image(fileName)
            pdf.output(streamFile, "F")
            pdf.close()

            self.send_response(200)
            self.send_header('Content-Type','application/pdf')
            self.send_header('Content-Disposition','attachment')
            self.send_header('filename','screenshot.pdf')
            self.end_headers()
            self.wfile.write(streamFile.getvalue())
        else:
            if parsed.path == '/':
                self.path = '/index.html'
            try:
                file_to_open = open(self.path[1:]).read()
                self.send_response(200)
            except:
                file_to_open = "File not found"
                self.send_response(404)

            self.end_headers()
            self.wfile.write(bytes(file_to_open, 'utf-8'))

    @staticmethod
    def checkValidUrl(url):
        regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(regex, url) is not None

    def response(code,msg):
        self.send_response(code)
        self.end_headers()
        self.wfile.write(bytes(msg, 'utf-8'))
           

    def do_POST(self):
        if self.path == '/':
            self.path = '/index.html'
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
            self.wfile.write(bytes(file_to_open, 'utf-8'))

        elif self.path == '/get-capture':
            url = 'http://freelancerviet.net/vi/hoi-va-dap/'
            browser = webdriver.Chrome('chromedriver.exe')
            browser.set_window_size(1280,1000)

            browser.get(url)
            fileName = 'output/file'+datetime.now().strftime("%Y%M%D%H%M%S")+'.jpg'
            ScreenCapture.fullpage_screenshot(browser,fileName, False)

            browser.quit()
            file_to_open = open(fileName).read()
            self.send_response(200)
            self.wfile.write(bytes(file_to_open))
        else:
            file_to_open = "File not found"
            self.send_response(404)
        self.end_headers()
# print('server start')
httpd = HTTPServer(('localhost', 8080), Serv)
httpd.serve_forever()