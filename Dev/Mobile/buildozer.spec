[app]

title = JPPocket
package.name = jppocket
package.domain = org.example

version = 1.0

source.dir = .
source.main = JPPocket.py

source.include_exts = py,png,kv,xlsx

requirements = python3,kivy,openpyxl

icon.filename = logo.png

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,INTERNET

android.minapi = 21
android.api = 33

orientation = portrait
android.enable_androidx = True

[buildozer]
log_level = 2
warn_on_root = 1
