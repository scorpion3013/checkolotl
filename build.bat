rmdir /s /q build
pyinstaller -F -i "logo.ico" "main.py"
bash -i -c "/home/scorp/.local/bin/pyinstaller -F -i "logo.ico" "main.py""
cd dist
bash -i -c "zip ./builds/linux_release.zip combos.txt config.yml proxies.txt main"
bash -i -c "zip ./builds/windows_release.zip combos.txt config.yml proxies.txt main.exe"
cd ..
rmdir /s /q build
pause