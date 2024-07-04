# CH-VideoKeszito

pyinstaller command:
```
pyinstaller --onefile --add-data "static_files/background.mp4;static_files" --add-data "static_files/last_image.png;static_files" --add-data "user_images/;user_images" --icon="icon.ico" --version-file=version_info.txt guij2.py
```