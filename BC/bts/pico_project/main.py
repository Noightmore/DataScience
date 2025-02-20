import network
import time
import socket
from machine import Pin

led_pin = machine.Pin("LED", machine.Pin.OUT)  # Define the pin connected to the LED, GPIO 25

def web_page():
    html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
              <script>
              function toggleLed() {
                  var xhttp = new XMLHttpRequest();
                  xhttp.open("GET", "/toggle", true);
                  xhttp.send();
              }
              </script></head><body><h1>Hello World</h1>
              <button onclick="toggleLed()">Toggle LED</button></body></html>"""
    return html

def ap_mode(ssid, password):
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)

    while not ap.active():
        pass

    print(ap.isconnected())
    print('AP Mode Is Active, You can Now Connect')
    print('IP Address To Connect to:: ' + ap.ifconfig()[0])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        print('Content = %s' % str(request))

        if '/toggle' in request.decode('utf-8'):
            led_pin.value(not led_pin.value())  # Toggle the LED state

        response = web_page()
        conn.send(response)
        conn.close()

ap_mode('pico', 'gogogogo')

