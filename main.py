import os
import uvicorn
import socket
import qrcode
import shutil
from tkinter import filedialog, Tk
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from typing import List
from colorama import Fore, Style, init

init(autoreset=True)
app = FastAPI()

CONFIG = {"target_dir": "", "ip": ""}


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


def generate_qr(url):
    qr = qrcode.QRCode(version=1, box_size=1, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    print(f"\n{Fore.MAGENTA}SCAN TO ACCESS THE LUNANOVA PORTAL:")
    qr.print_ascii(invert=True)


@app.get("/", response_class=HTMLResponse)
async def portal_home():
    return f"""
    <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ background: #050505; color: #f8fafc; font-family: 'Segoe UI', sans-serif; text-align: center; padding: 20px; }}
                .box {{ border: 1px solid #c084fc; padding: 30px; border-radius: 24px; background: #0f172a; max-width: 400px; margin: auto; box-shadow: 0 0 30px rgba(192, 132, 252, 0.2); }}
                h2 {{ color: #c084fc; letter-spacing: 4px; margin-top: 0; font-weight: 300; }}
                .section {{ margin-bottom: 25px; padding: 15px; border: 1px dashed #334155; border-radius: 15px; background: #0f172a; }}
                .mode-title {{ font-size: 0.75em; color: #94a3b8; display: block; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 2px; }}
                input[type="file"] {{ background: #1e293b; padding: 10px; border-radius: 8px; width: 100%; color: white; border: 1px solid #334155; font-size: 0.9em; box-sizing: border-box; }}
                .btn {{ background: linear-gradient(135deg, #c084fc 0%, #818cf8 100%); color: white; padding: 12px; border: none; border-radius: 12px; font-weight: 600; width: 100%; cursor: pointer; margin-top: 10px; transition: 0.3s; font-size: 0.9em; }}
                #status-text {{ font-size: 0.8em; margin: 10px 0; min-height: 1.2em; }}

                /* --- LOADER STYLES --- */
                #loader-container {{ display: none; justify-content: center; margin-top: 20px; }}
                .loader {{ width: 4em; height: 4em; }}
                .loader__eye1, .loader__eye2, .loader__mouth1, .loader__mouth2 {{ 
                    animation: eye1 3s ease-in-out infinite; stroke: #c084fc; fill: none; stroke-width: 12; stroke-linecap: round; stroke-linejoin: round;
                }}
                .loader__eye1, .loader__eye2 {{ transform-origin: 64px 64px; }}
                .loader__eye2 {{ animation-name: eye2; }}
                .loader__mouth1 {{ animation-name: mouth1; }}
                .loader__mouth2 {{ animation-name: mouth2; visibility: hidden; }}
                @keyframes eye1 {{ from {{ transform: rotate(-260deg) translate(0, -56px); }} 50%, 60% {{ animation-timing-function: cubic-bezier(0.17, 0, 0.58, 1); transform: rotate(-40deg) translate(0, -56px) scale(1); }} to {{ transform: rotate(225deg) translate(0, -56px) scale(0.35); }} }}
                @keyframes eye2 {{ from {{ transform: rotate(-260deg) translate(0, -56px); }} 50% {{ transform: rotate(40deg) translate(0, -56px) rotate(-40deg) scale(1); }} 52.5% {{ transform: rotate(40deg) translate(0, -56px) rotate(-40deg) scale(1, 0); }} 55%, 70% {{ animation-timing-function: cubic-bezier(0, 0, 0.28, 1); transform: rotate(40deg) translate(0, -56px) rotate(-40deg) scale(1); }} to {{ transform: rotate(150deg) translate(0, -56px) scale(0.4); }} }}
                @keyframes mouth1 {{ from {{ stroke-dasharray: 0 351.86; stroke-dashoffset: 0; }} 25% {{ stroke-dasharray: 175.93 351.86; stroke-dashoffset: 0; }} 50% {{ stroke-dasharray: 175.93 351.86; stroke-dashoffset: -175.93; visibility: visible; }} 75%, to {{ visibility: hidden; }} }}
                @keyframes mouth2 {{ from {{ visibility: hidden; }} 50% {{ visibility: visible; stroke-dashoffset: 0; }} to {{ stroke-dashoffset: -351.86; }} }}
            </style>
        </head>
        <body>
            <div class="box">
                <h2>LUNANOVA</h2>
                <p id="status-text" style="color: #94a3b8;">Portal Active</p>
                <hr style="border: 0.5px solid #334155; margin: 20px 0;">

                <div class="section">
                    <span class="mode-title">Select Specific Files</span>
                    <input type="file" id="fileInput" multiple>
                    <button onclick="uploadFiles('fileInput')" class="btn">BEAM FILES</button>
                </div>

                <div class="section">
                    <span class="mode-title">Select Entire Folder</span>
                    <input type="file" id="folderInput" webkitdirectory directory>
                    <button onclick="uploadFiles('folderInput')" class="btn" style="background: #1e293b; border: 1px solid #c084fc; color: #c084fc;">BEAM FOLDER</button>
                </div>

                <div id="loader-container">
                    <svg class="loader" viewBox="0 0 128 128">
                        <g><circle class="loader__eye1" r="7" cx="64" cy="64"></circle></g>
                        <g><circle class="loader__eye2" r="7" cx="64" cy="64"></circle></g>
                        <g><path class="loader__mouth1" d="M64,88 C50,88 38,76 38,62"></path></g>
                        <g><path class="loader__mouth2" d="M64,88 C78,88 90,76 90,62"></path></g>
                    </svg>
                </div>
            </div>

            <script>
                async function uploadFiles(inputId) {{
                    const input = document.getElementById(inputId);
                    const files = Array.from(input.files);
                    if (files.length === 0) return alert("Nothing selected.");

                    const status = document.getElementById('status-text');
                    const loader = document.getElementById('loader-container');

                    status.style.color = "#c084fc";
                    loader.style.display = "flex";

                    for (let i = 0; i < files.length; i++) {{
                        status.innerText = `BEAMING [${{i + 1}}/${{files.length}}]: ${{files[i].name.substring(0,15)}}...`;
                        const formData = new FormData();
                        formData.append("files", files[i]);

                        try {{
                            await fetch('/upload', {{ method: 'POST', body: formData, cache: 'no-cache' }});
                            await new Promise(r => setTimeout(r, 100));
                        }} catch (e) {{
                            status.innerText = "LINK INTERRUPTED";
                            loader.style.display = "none";
                            return;
                        }}
                    }}

                    status.innerText = "BEAM COMPLETE";
                    status.style.color = "#4ade80";
                    loader.style.display = "none";
                    setTimeout(() => {{ status.innerText = "Portal Active"; status.style.color = "#94a3b8"; }}, 3000);
                    input.value = ""; 
                }}
            </script>
        </body>
    </html>
    """


@app.post("/upload")
async def handle_upload(files: List[UploadFile] = File(...)):
    for file in files:
        save_path = os.path.join(CONFIG["target_dir"], file.filename)
        file_dir = os.path.dirname(save_path)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        print(f"{Fore.MAGENTA}[BEAMED] {Fore.WHITE}{file.filename}")
    return {"status": "success"}


def initialize_engine():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Fore.MAGENTA}{Style.BRIGHT}==================================================")
    print(f"{Fore.MAGENTA}            LUNANOVA PORTAL: ASCENDED")
    print(f"{Fore.MAGENTA}==================================================\n")
    root = Tk();
    root.withdraw();
    root.attributes("-topmost", True)
    path = filedialog.askdirectory(title="Select LunaNova Landing Zone")
    root.destroy()
    if not path: return False
    CONFIG["target_dir"] = path
    CONFIG["ip"] = get_local_ip()
    url = f"http://{CONFIG['ip']}:8000"
    print(f"{Fore.WHITE}LANDING ZONE: {Fore.YELLOW}{path}")
    print(f"{Fore.WHITE}PORTAL URL:   {Fore.GREEN}{url}")
    generate_qr(url)
    return True


if __name__ == "__main__":
    if initialize_engine():
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="error")