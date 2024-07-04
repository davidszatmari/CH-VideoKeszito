# CH-VideoKeszito

pyinstaller command:
```
pyinstaller --onefile --add-data "static_files/background.mp4;static_files" --add-data "static_files/last_image.png;static_files" --add-data "user_images/;user_images" --icon="icon.ico" --version-file=version_info.txt guij2.py
```

## Built With

* [Python 3.12.1](https://www.python.org/) - Core language for development.
* [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Used for GUI
* [MoviePy](https://github.com/Zulko/moviepy) - Used for video creating and image editing
* [PyInstaller](https://pyinstaller.org/en/stable/) - Used for converting Python scripts to .exe.
