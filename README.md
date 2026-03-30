# ilmaistapahtumat

Nykyiset toiminnot:
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään sovellukseen tapahtuma-ilmoituksia.
* Käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään ilmoituksia.
* Käyttäjä näkee sovellukseen lisätyt ilmoitukset. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät ilmoitukset.
* Käyttäjä pystyy etsimään tietokohteita hakusanalla. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä tietokohteita.
* Käyttäjä pystyy valitsemaan ilmoitukselle yhden tai useamman luokittelun (esim. sijainti, kellonaika, päivämäärä).

Tulevat toiminnot:
* Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja ja käyttäjän lisäämät ilmoitukset.
* Käyttäjä pystyy kommentoimaan omiin sekä muiden käyttäjien ilmoituksiin (esim. lisätietoa tapahtumasta, hype).

**Käynnistysohje:**

Näillä ohjeita voit ajaa sovelluksen omalla koneellasi. 

1. Esivaatimukset
Varmista, että koneellesi on asennettu **Python 3**.

2. Sovelluksen lataaminen
Kloonaa projekti tai lataa se ZIP-tiedostona ja mene projektikansioon linux komentotulkilla:
$ cd ilmaistapahtumat

3. Virtuaaliympäristön käynnistäminen
$ python3 -m venv venv
$ source venv/bin/activate

4. Python kirjastojen paikallinen asennus
$ pip install flask

5. Tietokannan alustus
$ sqlite3 database.db < schema.sql

6. Sovelluksen käynnistäminen:
$ flask run
