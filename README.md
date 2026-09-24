# YARIS

A small Toyota Yaris desktop companion for Windows. YARIS displays an animated car on the desktop and plays its soundtrack in the background.

## Features

- Frameless, draggable animated Yaris window
- Right-click menu for volume controls and exit
- Standalone Windows executable build
- MIT licensed

## Run From Source

1. Install Python 3.10 or newer.
2. Install the dependencies:

	```powershell
	pip install PyQt5 pygame
	```

3. Start the app:

	```powershell
	python initalize.py
	```

Keep `yaris.gif` and `yaris.mp3` beside the Python files when running from source.

## Build The Windows App

Install PyInstaller and build the single-file executable:

```powershell
pip install pyinstaller
pyinstaller --clean --noconfirm --onefile --windowed --name YARIS --icon yaris.ico --add-data "yaris.gif;." --add-data "yaris.mp3;." initalize.py
```

The executable is created in `dist/YARIS.exe`.

## Links

- [Project source](https://github.com/G33K-dev/Yaris-G33K-v1)
- [Releases](https://github.com/G33K-dev/Yaris-G33K-v1/releases)
- [Issues](https://github.com/G33K-dev/Yaris-G33K-v1/issues)

## Credits

- Soundtrack: [Why's This Dealer?](https://soundcloud.com/user-820028958/niko-b-whys-this-dealer) by Niko B

## License

Released under the [MIT License](LICENSE).


<h2 align="center"><i>HAVE FUN</i></h1>

<p align="center">
	<img src="g33k-mark.svg" alt="G33K" width="680">
</p>
