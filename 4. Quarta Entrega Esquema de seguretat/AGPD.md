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
Copies de seguretat:
- Fem còpies de seguretat regularment, tant en local com en el núvol.

<br>

Control d'accés:
- Hem assignat rols a tots els usuaris i grups.
- Us de contrasenyes segures.

<br>

<h2> Mesures nivell mitj </h2>
Data Masking:
- Creació i assignació de tècniques de Data Masking, per tal de protegir les dades més sensibles.

<br>

Xifratge:
- Disposem d'un xifratge actiu, que xifra totes les dades del programa.

<h2> Mesures nivell alt </h2>

<h3>Seguretat física:</h3>
<ul>
    <li><b>Control d'accés estricte:</b> Implementació de controls biomètrics (empremta digital, reconeixement facial) per accedir a les àrees on es guarden les dades dels pacients.</li>
    <li><b>Vigilància 24/7:</b> Sistemes de vigilància amb càmeres de seguretat a les àrees de servidors i altres zones crítiques, amb enregistrament continu i monitorització activa.</li>
    <li><b>Dispositius de seguretat física:</b> Utilització de portes blindades, panys electrònics i sistemes d'alarma en les instal·lacions de TI.</li>
</ul>

<h3>Avaluacions d'impacte:</h3>
<ul>
    <li><b>Avaluacions d'impacte de protecció de dades (EIPD) periòdiques:</b> Realització d'EIPD periòdiques per identificar i mitigar riscos associats al tractament de dades personals.</li>
    <li><b>Integració d'eines d'avaluació automàtiques:</b> Ús d'eines automatitzades per avaluar l'impacte en la privacitat de nous projectes o canvis en els processos.</li>
    <li><b>Formació contínua:</b> Sessions de formació regulars per al personal sobre la importància i la realització d'avaluacions d'impacte.</li>
</ul>

<h3>Xifratge avançat:</h3>
<ul>
    <li><b>Xifratge de disc complet (FDE):</b> Implementació de xifratge de disc complet per a tots els dispositius que emmagatzemen dades sensibles.</li>
    <li><b>Xifratge d'extrem a extrem:</b> Utilització de xifratge d'extrem a extrem per a totes les comunicacions entre dispositius mèdics, servidors i aplicacions.</li>
    <li><b>Protocols de xifratge avançats:</b> Aplicació de protocols de xifratge avançats com AES-256 per protegir dades en trànsit i en repòs.</li>
</ul>


