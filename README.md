# YARIS

A small Toyota Yaris desktop companion for Windows. YARIS displays an animated car on the desktop and plays its soundtrack in the background.

## Features

- Frameless, draggable animated Yaris window
- Right-click menu for volume controls and exit
- Standalone Windows executable build

## Run From Source

1. Install Python 3.10 or newer.
2. Install the dependencies:

	```powershell
	pip install PyQt5 pygame
	```

3. Start the app from the repository root:

	```powershell
	python ToyotAPP\initalize.py
	```

The Python files and runtime assets live together in `ToyotAPP`.

## Build The Windows App

Install PyInstaller and build the single-file executable into `downloads`:

```powershell
pip install pyinstaller
pyinstaller --clean --noconfirm --onefile --windowed --name YARIS --distpath downloads --workpath build --specpath build --icon ToyotAPP\yaris.ico --add-data "ToyotAPP\yaris.gif;." --add-data "ToyotAPP\yaris.mp3;." ToyotAPP\initalize.py
```

The executable is created in `downloads/YARIS.exe`.

## Links

- [Project source](https://github.com/G33K-dev/Yaris-G33K-v1)
- [Releases](https://github.com/G33K-dev/Yaris-G33K-v1/releases)
- [Issues](https://github.com/G33K-dev/Yaris-G33K-v1/issues)

## Credits

- Soundtrack: [Why's This Dealer?](https://soundcloud.com/user-820028958/niko-b-whys-this-dealer) by Niko B
- Gif : [Yaris Gif](https://tenor.com/pl/view/toyota-yaris-gif-159930250860655829) on Tenor 

