from flask import Flask, Response, render_template_string
import mss
from PIL import Image, ImageDraw
import io
import time
import pyautogui
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int, default=5000, help='Port to run the server on')
parser.add_argument('--fps', type=int, default=30, help='Frames per second')
parser.add_argument('--quality', type=int, default=40, help='Image quality (1-100)')
parser.add_argument('--monitor', type=int, default=1, help='Which monitor to capture (1 for primary, 2 for secondary, etc.)')
parser.add_argument('--cursor_color', type=str, default='red', help='Cursor color (e.g., red, blue, green)')
parser.add_argument('--cursor_size', type=int, default=12, help='Cursor size in pixels')
parser.add_argument("--resolution", type=str, default="Default", help="Resolution in WIDTHxHEIGHT format, e.g., 1280x720")
parser.add_argument("--format", type=str, default="JPEG", help="Image format: PNG,JPEG, WEBP.. etc")
args = parser.parse_args()

TPF = 1/args.fps
QUALITY = args.quality
PORT = args.port
MONITOR = args.monitor
CURSOR_SIZE = args.cursor_size
CURSOR_COLOR = args.cursor_color
FORMAT = args.format
RESIZE = True if args.resolution != "Default" else False
if RESIZE:
    try:
        WIDTH, HEIGHT = map(int, args.resolution.lower().split('x'))
        if WIDTH <= 0 or HEIGHT <= 0:
            raise ValueError
    except ValueError:
        print("Invalid resolution format. Use WIDTHxHEIGHT with positive integers.")
        exit(1)

print(f"Starting server on port {PORT}, capturing monitor {MONITOR} at {args.fps} FPS, quality {QUALITY}, cursor color {CURSOR_COLOR}, cursor size {CURSOR_SIZE}, format {FORMAT}, resolution {'Default' if not RESIZE else args.resolution}")
app = Flask(__name__)

def generate_frames():
    with mss.mss() as sct:
        monitor = sct.monitors[MONITOR]  # 1 = écran principal
        while True:
            #Screenshot
            img = sct.grab(monitor)
            image = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")

            

            # Cursor position
            x, y = pyautogui.position()
            x -= monitor["left"]
            y -= monitor["top"]

            # DRAW CURSOR
            draw = ImageDraw.Draw(image)



            draw.polygon([
                (x, y), 
                (x + CURSOR_SIZE, y + CURSOR_SIZE * 2), 
                (x, y + CURSOR_SIZE * 2)
            ], fill=CURSOR_COLOR)

            if RESIZE:
              target_size = (WIDTH, HEIGHT)  # largeur, hauteur
              image = image.resize(target_size)

            # Convert to JPEG
            buf = io.BytesIO()
            image.save(buf, format=FORMAT, quality=QUALITY)
            frame = buf.getvalue()

            # Flux MJPEG
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            time.sleep(TPF)

@app.route('/')
def index():
    return render_template_string("""
    <html>
      <head>
        <!-- MADE BY APROTONIX -->
       
        <title>Screencast</title>
        <style>
          body, html {
            margin: 0;
            padding: 0;
            height: 100%;
            width: 100%;
            background: black;
          }
          #screen {
            display: block;
            width: 100%;
            height: 100%;
            object-fit: cover;
          }
          #fullscreenBtn {
            position: fixed;
            top: 10px;
            right: 10px;
            padding: 10px 15px;
            background: rgba(0,0,0,0.6);
            color: white;
            border: none;
            border-radius: 100px;
            cursor: pointer;
            bold: true;
            font-weight: 900;
          }
        </style>
      </head>
      <body>
        <button id="fullscreenBtn">⛶</button>
  <img id="screen" src="/video_feed">

  <script>
    const btn = document.getElementById("fullscreenBtn");
    const screen = document.getElementById("screen");

    btn.onclick = async () => {
      if (!document.fullscreenElement) {
        await screen.requestFullscreen();

        // Essayer de verrouiller l'orientation en paysage
        if (screen.orientation && screen.orientation.lock) {
          try {
            await screen.orientation.lock("landscape");
          } catch (e) {
            console.log("Impossible de forcer le paysage :", e);
          }
        }
      } else {
        document.exitFullscreen();
      }
    };
  </script>

      </body>
    </html>
    """)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True, threaded=True, host="0.0.0.0", port=PORT)
