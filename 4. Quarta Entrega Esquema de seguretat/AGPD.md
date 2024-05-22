# <p align="center"> Agencia de Protecció de Dades AGPD</p>

Classificació de dades
----------------------
Nosaltres hem fet una classificacio de dades 
<h2> Nivel Baix </h2>
<br>

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
Taula Aparell
- id_aparell
- tipus_de_aparell
Taula Medicament
- nom
- id_medicament

<h2> Nivel Alt </h2>
Taula Personal
- dni
- id_personal
- id_vari
- id_infermeria
- id_medic
Taula Pacient
- id_pacient

Mesures de dades
-----------------


Nivell mitjà
Taula pacientes:

fecha_nacimiento
direccion
num_telefono
Taula personal:

correo
num_telefono
direccion
Taula diagnósticos:

fecha_entrada
fecha_salida
Taula operaciones:

en_id
fecha_entrada
fecha_salida
ha_sido_operado
q_id
Taula reservas:

h_id
diaentrada
diaprevistosalida
Nivell alt
Taula pacientes:

id_tarjeta_sanitaria
contacto_emergencia
condiciones_paciente
Taula personal:

p_id
DNI
Taula diagnósticos:

p_id
id_tarjeta_sanitaria
tiene_receta
medicamentos
Taula operaciones:

Id_tarjeta_sanitaria
p_id
Taula reservas:

id_tarjeta_sanitaria
