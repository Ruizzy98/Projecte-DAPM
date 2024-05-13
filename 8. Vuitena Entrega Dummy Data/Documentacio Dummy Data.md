# <p align="center">  Dummy Data  </p>
Faker
-------------
En aquest cas hem utilitzat el faker

Faker és una eina en Python que permet generar dades fictícies. Amb aquesta llibreria, pots crear qualsevol dada fictícia.
<br>
Això és útil quan necessites omplir una base de dades amb dades de prova o realitzar proves en el teu codi sense utilitzar informació real, i també per protegir la privadesa de les persones en el procés de desenvolupament de software. 



Com l'hem utilitzat?
-----
Per començar vam fer el pip install al cmd

![i1](fotos/pip.jpg)

Seguidament al utilitzar un arxiu python cal posar aquests imports

![i2](fotos/imports.jpg)


Creació d'Index
---------------
Índex per a la taula RESERVA en la columna nom_quirofan:
- CREATE INDEX index_reserva_nom_quirofan ON RESERVA (nom_quirofan);
Índex per a la taula VISITA en la columna id_pacient:
- CREATE INDEX index_visita_id_pacient ON VISITA (id_pacient);
Índex per a la taula VISITA en la columna id_medic:
- CREATE INDEX index_visita_id_medic ON VISITA (id_medic);
Índex per a la taula OPERACIO en la columna id_pacient:
- CREATE INDEX index_operacio_id_pacient ON OPERACIO (id_pacient);
Índex per a la taula OPERACIO en la columna id_medic:
- CREATE INDEX index_operacio_id_medic ON OPERACIO (id_medic);
Índex per a la taula PACIENT_INGRESSAT en la columna num_habitacio:
- CREATE INDEX index_pacient_ingressat_num_habitacio ON PACIENT_INGRESSAT (num_habitacio);
