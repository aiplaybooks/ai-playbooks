# AgentDaily — AI araçları Instagram sayfası otomasyonu

Her gün AI araçları (ChatGPT, Claude, Claude Code, Codex, Grok, Gemini...) hakkında carousel ve Reel üreten, tamamen ücretsiz bir sistem.

## Kurulum (Windows, bir kere)
1. Python 3.10+ kurulu olmalı.
2. Bu klasörde terminal aç ve çalıştır:
   ```
   pip install -r requirements.txt
   python -m playwright install chromium
   winget install ffmpeg
   ```
3. VS Code'da bu klasörü aç ve Claude Code'u başlat. Claude Code `CLAUDE.md` dosyasını okuyarak projeyi ve kaldığımız yeri öğrenir.

## Kullanım
Carousel (PNG slaytlar):
```
python carousel.py content/2026-09-24_claude-tradingview.json
```
Reel (MP4 video, yaklaşık 2-3 dakika sürer):
```
python reel.py content/2026-09-24_claude-tradingview.json
```
Çıktılar `output/<içerik-adı>/` klasörüne gider. `contact.png` tüm slaytların toplu önizlemesidir.

Başka bir tasarımla denemek için: `--theme neon` veya `--theme ledger`.

Seslendirme: slaytlarda `voiceover` alanı varsa Reel otomatik olarak Kokoro ile seslendirilir ve altyazı eklenir
(Kokoro, Pinokio'daki Ultimate-TTS-Studio kurulumundan kullanılır). Her gönderiye ses havuzundan (Sarah, Jessica, Liam, Fenrir, Puck, Eric, Adam) sırayla farklı bir ses atanır;
tek seferlik başka ses için `--voice am_liam`,
seslendirmesiz için `--no-voice`.

## Yeni içerik
`content/` klasörüne yeni bir JSON dosyası eklemen yeterli. Örnek olarak mevcut iki dosyaya bak. Claude Code'a "bugünün içeriğini hazırla" demen de yeterli.

## Klasörler
- `themes/`: tasarımlar (her biri ayrı bir görünüm)
- `content/`: her gönderinin metni (tek kaynak)
- `samples/`: ilk oturumda üretilen örnek çıktılar
- `fonts/`: açık kaynak fontlar ve lisansları
