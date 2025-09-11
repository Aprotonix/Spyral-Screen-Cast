# Spyral-Screen-Cast
A simple python project to cast your screen in your local network

### Usage
You have to run the python program and note ip written in the terminal then you can past it in any navigator of the devices in your local network and see your screen


You can start the program with :
`python main.py [args]`

#### Arguments : 

    `main.py [-h] [--port PORT] [--fps FPS] [--quality QUALITY] [--monitor MONITOR] [--cursor_color CURSOR_COLOR] [--cursor_size CURSOR_SIZE] [--resolution RESOLUTION] [--format FORMAT]`

  `--port PORT`           Port to run the server on
  `--fps FPS`         Frames per second
  `--quality QUALITY`   Image quality (1-100)
  `--monitor MONITOR`     Which monitor to capture (1 for primary, 2 for secondary, etc.)
  `--cursor_color CURSOR_COLOR`
                        Cursor color (e.g., red, blue, green)
  `--cursor_size CURSOR_SIZE`
                        Cursor size in pixels
  `--resolution RESOLUTION`
                        Resolution in WIDTHxHEIGHT format, e.g., 1280x720
  `--format FORMAT`       Image format: PNG,JPEG, WEBP.. etc