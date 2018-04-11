# TbaneKart (WIP/Proof Of Concept)

Et kart som viser hvor togene i tbanen i Oslo er, beregnet basert på sanntidssystemet.

Fungerer ved at den sjekker neste avganger for alle stasjoner, og bruker de forventede avgangstidene til å beregne hva som er neste stasjon. Når systemet vet neste og forrige stasjon kan det beregne hvor langt det har kommet mellom disse stasjonene basert på tiden.

Kartet er et Work in Progress Proof of Concept, og vil ha bugs.

## Viktig

Kartet viser ikke nøyaktige posisjoner, og viser bare tog i rute. Kartet kan ikke brukes til å se når man kan ferdes langs eller krysse sporet o.l. Å ferdes i skinnegangen til tbanenettverket er livsfarlig, og forbudt.

## Teknisk

Kartet er kodet i Python 3.6, og benytter seg av Flask frameworket og Google Maps sin API.

## Oppsett

* Installer Python 3.6.
* Klon eller last ned en kopi av repoet..
* Kjør `server/setup.py install` for å installere dependencies..
* Kopier eller bytt navn på `client/init.example.js` til `client/init.js` og fyll ut informasjonen i filen.
* Sett opp en webserver til å vise `client/` og kjør `server/main.py`.
