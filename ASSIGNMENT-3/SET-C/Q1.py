from flask import Flask
import platform

app = Flask(__name__)

@app.route("/system_info")
def system_info():
    info = {
        "System": platform.system(),
        "Node Name": platform.node(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor()
    }
    return str(info)

if __name__ == "__main__":
    app.run(debug=True)
