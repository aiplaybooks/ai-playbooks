@echo off
cd /d "%~dp0"
echo X girisi: acilan pencerede YEDEK X hesabinla giris yap. Ana sayfa acilinca pencere kendiligindan kapanir.
python xscout.py --login
pause
