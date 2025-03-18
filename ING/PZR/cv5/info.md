# zapis

- upravit k-spektralnich priznaku na nerovnomerna okna, podobne jak funguje lidske ucho
- od 0 do 100 Hz -- linearni zalezitost (melova stupnice)
- od 100 do 2000 Hz -- logaritmicka zalezitost (melova stupnice) 
- vetsi a vetsi zplosteni  cim vyssi Hz
- Mel(f) = 2595 * log10(1 + f/700) 
- pasma se mohou prekryvat
- MEL spektralni priznaky, program na elearningu
- Kepstralni priznaky jsou lepsi nez MEL priznaky MFCC

- jak zrychlit DTW:
  - maticove, vektorove operace misto for cyklu
  - optimalizovat nejcasteji opakovane operace
  - funkce norm pro euklidovskou vzdalenost