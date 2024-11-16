# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],  # Entry script
    pathex=['C:\\Users\\Craig\\Documents\\Python\\Day 49 - Selenium - Stuff'],  # Include the project directory
    binaries=[],
    datas=[
        ('C:\\Users\\Craig\\Documents\\Python\\Day 49 - Selenium - Stuff\\Images', 'Images'),
    ],
    hiddenimports=[
        'selenium',
        'selenium.webdriver',
        'selenium.webdriver.common',
        'selenium.webdriver.support',
        'selenium.webdriver.common.keys',
        'selenium.common.exceptions',
        'dotenv',
        'requests',
        'SeleniumHelpers',
        'KahootBot',
        'QuizBot',
        'Logger'
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    console=True,  # Set to False for GUI apps
    icon=None  # Add path to an icon file if you want one
)
