# Optima -> Sky-Shop integration

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
    +----------------------------------------- Symbol produktu z Optima

## Założenia

* Z pliku źródłowego do zmiany kwalifikujemy tylko produkty dla których cena w Optima > 0
* Jako cenę do zmiany pobieramy cenę brutto z Optima (cena netto przeliczy się automatycznie w sklepie na podstawie wprowadzonej stawki vat)
* Ilość do zmiany pobieramy jako różnicę ilości na stanie i ilości zarezerwowanej
* Ze sklepu Sky-Shop pobieramy do aktualizacji tylko produkty, które mają uzupełniony symbol produktu z systemu Optima
* Symbol produktu w Sky-Shop **musi być unikalny**
* Jeżeli w nazwie symbolu w pliku z Optima znajdują się spacje (z przodu lub z tyłu) to je obcinamy przed porónaniem ze sklepem

## Wymagania

* Program napisany jest w języku Python. Wymagana wersja >= 3
    https://www.geeksforgeeks.org/how-to-download-and-install-python-latest-version-on-windows/
* Do wykonywania zapytań z wykorzystaniem API wykorzystywana jest biblioteka Requests
https://www.geeksforgeeks.org/how-to-install-requests-in-python-for-windows-linux-mac/

## Sposób użycia

Program uruchamiamy z wykorzystaniem interpretera języka python wraz z podaniem wymaganych parametrów. Wywołanie programu bez parametrów spowoduje wyświetlenie pomocy dotyczącej wywołania polecenia

    $python updatePricesAndAmount.py

    usage: updatePricesAndAmount.py [-h] -f OPTIMAFILE -d DOMAIN -k WEBAPIKEY
    updatePricesAndAmount.py: error: the following arguments are required: -f/--optimaFile, -d/--domain, -k/--webApiKey

| parametr         | opis |
| ---------------  | ----------- |
|**-f / --optimaFile**|ścieżka do lokalnego pliku źródłowego z systemu Optima|
|**-d / --domain**|domena skleu Sky-Shop, np. marine-mobile.pl|
|**-k / --webApiKey**|klucz API sklepu dostępny z poziomu panelu administarcyjnego (Integracje -> Web Api Sklepu)|

Po poprawnym wywołaniu programu log z wykonania aktualizacji cen i ilości magazynowych zapisywany jest w pliku w podkatalogu /log

