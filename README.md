# Labirent Ajanı

Fareyle duvar çizdiğin bir grid labirentte, başlangıç noktasından hedefe en kısa yolu
BFS ve A* algoritmalarını birlikte (hibrit) kullanarak bulan ve animasyonla gösteren proje.

## Nasıl çalışıyor?
1. **Aşama 1 - BFS:** Hedefe ulaşılabilir mi diye kontrol eder (açık mavi kareler).
2. **Aşama 2 - A\*:** Manhattan mesafesi sezgisiyle en kısa yolu bulur (turuncu kareler).
3. Bulunan yol sarı renkle gösterilir.

## Nasıl çalıştırılır?
1. Python'u kur (python.org)
2. `pip install pygame` (Python'un yeni sürümlerinde çalışmazsa `pip install pygame-ce`)
3. `python main.py`

## Kullanım
| Tuş / fare | Ne yapar |
|---|---|
| Sol tık (basılı tutup gezdir) | Duvar ekler |
| Sağ tık | Duvarı siler |
| S + sol tık | Başlangıç noktasını taşır |
| G + sol tık | Hedef noktasını taşır |
| SPACE | Aramayı başlatır (en az 8 duvar gerekir) |
| C | Her şeyi temizler |

Labirent boyutu 25x50 karedir.

## Ekran görüntüleri
### Boş grid
![Boş grid](screenshots/bos-grid.png.jpg)

### Arama sırasında
![Arama](screenshots/arama.png.jpg)

### Bulunan yol
![Yol](screenshots/yol.png.jpg)
## Sonuçlar
| Senaryo | BFS gezilen | A* gezilen | Yol uzunluğu |
|---|---|---|---|
| Açık alan | 1048 | 93 | 47 |
| Dar koridor | 1017 | 90 | 42 |
| Hedefe doğru duvar | 1221 | 929 | 65 |
| Ulaşılamaz | - | - | - |



## Veri seti
Bu projede harici veri seti kullanılmamıştır, labirent kullanıcı tarafından çizilmektedir.