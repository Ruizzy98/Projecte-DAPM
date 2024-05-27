# <p align="center"> Agencia de Protecció de Dades AGPD</p>

Classificació de dades
----------------------
Nosaltres hem classificat la informació de manera que les dades més sensibles estiguin tan protegits com sigui possible, i els que no són tan sensibles protegir-los, però amb menys seguretat, per a fer-ho primer classifiquem la informació. 
<h2> Nivel Baix </h2>

Taula Personal
- nom
- cognom
- tipus_de_feina

<br>

Taula Pacient
- nom
- cognom

<br>

Taula Planta
- num_planta

<br>

Taula Habitacio
- numero_habitacio


<br>
<h2> Nivel Mitj </h2>

Taula Personal
- especialitat
- estudis
- curriculum

<br>

Taula Aparell
- id_aparell
- tipus_de_aparell

<br>
  
Taula Medicament
- nom
- id_medicament

<br>

<h2> Nivel Alt </h2>

Taula Personal
- dni
- id_personal
- id_vari
- id_infermeria
- id_medic

<br>

Taula Pacient
- id_pacient

<br>

Taula Visita
- diagnostic
- data_hora
- id_visita

<br>

Taula Reserva
- id_reserva
- dia_sortida
- dia_ingres


<h2> Mesures de dades </h2>

Després creem unes mesures necessàries a les dades, per a fer-ho també les classifiquem en tres nivells.

<h2> Mesures nivell baix </h2>
Copies de seguretat: <br>

<br>

- Fem còpies de seguretat regularment, tant en local com en el núvol.

<br>

Control d'accés:
- Hem assignat rols a tots els usuaris i grups.
- Us de contrasenyes segures.

<br>

<h2> Mesures nivell mitj </h2>

Data Masking: <br>
- Creació i assignació de tècniques de Data Masking, per tal de protegir les dades més sensibles.

<br>

Xifratge:
- Disposem d'un xifratge actiu, que xifra totes les dades del programa.

<h2> Mesures nivell alt </h2>

Seguretat física:

- Control d'accés estricte amb Implementació de controls biomètrics per accedir a les àrees on es guarden les dades dels pacients.

- Dispositius de seguretat física amb utilització de portes blindades

Xifratge avançat:

- Xifratge de disc complet: Implementació de xifratge de disc complet per a tots els dispositius que emmagatzemen dades sensibles.




