# 🌌 LunaNova Portal: Ascended

**LunaNova** is a lightweight, high-performance file transfer utility designed to bridge the gap between mobile devices and desktops over a local network. It replaces clunky cloud uploads with a direct, "stellar" transmission link.

## 🚀 Key Features
- **Dual-Mode Beaming:** Choose between specific file selection or entire folder uploads.
- **Sequential Transmission:** Custom JavaScript engine beams files one-by-one to prevent network timeouts, even for files exceeding 1GB.
- **Auto-Zone Creation:** Automatically builds directory structures on the host machine during folder uploads.
- **Instant Connectivity:** Generates a local IP QR code in the terminal for immediate mobile access.
- **LunaNova Aesthetic:** A dark-mode, neon-accented UI featuring the "Uiverse" animated loader for visual feedback during large transfers.

## 🛠️ Built With
- **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (Python) for high-concurrency handling.
- **Server:** [Uvicorn](https://www.uvicorn.org/) ASGI server.
- **Frontend:** HTML5, CSS3 (Flexbox/Animations), and Vanilla JavaScript (Async/Await Fetch API).
- **CLI:** [Colorama](https://pypi.org/project/colorama/) for terminal branding and [QRcode](https://pypi.org/project/qrcode/) for link generation.
- **System:** Tkinter for native OS directory selection.

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/LunaNova.git](https://github.com/YOUR_USERNAME/LunaNova.git)
   cd LunaNova
