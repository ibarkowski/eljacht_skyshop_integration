#Eljacht Optima -> Sky-Shop integration

Skrypt wykonuje aktualizację cen, oraz ilości artykułów w podanym sklepie Sky-Shop. Dane źródłowe pobierane są z pliku źródłowego wygenerowanego w systemie Optima, wg poniższej struktury:

    0001-00000-73135|29,27|10005|36,12|8|0|
    ^                ^     ^     ^     ^ ^ 
    |                |     |     |     | |   
    |                |     |     |     | +---- Ilość zarezerwowana  
    |                |     |     |     |
    |                |     |     |     +------ Ilość na magazynie
    |                |     |     |
    |                |     |     +------------ Cena brutto
    |                |     |
    |                |     +------------------ "jakaś" stała :)
    |                |
    |                +------------------------ Cena netto
    |
    +----------------------------------------- Symbol z Optima

## Założenia

* 