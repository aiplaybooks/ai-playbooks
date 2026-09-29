@echo off
cd /d "%~dp0"
echo X girisi: acilan Chrome penceresinde YEDEK X hesabinla giris yap, ana sayfa gorununce Chrome penceresini KAPAT.
python xscout.py --login
pause
