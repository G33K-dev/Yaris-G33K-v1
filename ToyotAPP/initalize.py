import threading
import music
import gif

print('YARIS')

threading.Thread(target=music.start, daemon=True).start()
gif.start()
