import serial
import time
from flask import Flask, render_template, jsonify
import threading

app = Flask(__name__)

current_distance = 0

def read_bluetooth():
    global current_distance
    ser = serial.Serial('COM4', 9600, timeout=1)
    
    while True:
        if ser.in_waiting:
            try:
                data = ser.readline().decode().strip()
                if "cm" in data:
                    current_distance = float(data.replace("cm", ""))
            except:
                pass
        time.sleep(0.1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_distance')
def get_distance():
    return jsonify({'distance': current_distance})

if __name__ == '__main__':
    bluetooth_thread = threading.Thread(target=read_bluetooth)
    bluetooth_thread.daemon = True
    bluetooth_thread.start()
    
    app.run(host='127.0.0.1', port=8100)