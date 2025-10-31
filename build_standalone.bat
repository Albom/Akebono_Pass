call conda activate base
python --version
python -m nuitka ^
  --standalone ^
  --onefile ^
  --windows-console-mode=disable ^
  --enable-plugin=pyside6 ^
  --assume-yes-for-downloads ^
  --include-data-dir=images=images ^
  --windows-icon-from-ico=images/icon.png ^
  --windows-company-name=IION ^
  --windows-product-name=akebono_pass ^
  --windows-product-version=0.2.0 ^
  akebono_pass.py

rmdir /q /s akebono_pass.build
rmdir /q /s akebono_pass.dist
rmdir /q /s akebono_pass.onefile-build
