# <p align="center"> ESQUEMA DE SEGURETAT </p>

Creació de rols i grups
-----------------------
**ADMINS** (NOSALTRES)
-	Hauria de tenir accés complet a totes les taules i la capacitat de realitzar qualsevol operació en la base de dades, incloent-hi la creació, modificació i eliminació de taules i registres.
-	Pot crear, modificar i eliminar usuaris i assignar-los rols i permisos.

Crear un rol amb permisos de superUsuari
```
CREATE ROLE admins WITH SUPERUSER LOGIN PASSWORD '1234hola';
```
Donar permisos de accés complet a totes les taules:
```
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admins;
```
Donar accés complet a la base de dades:
```
GRANT ALL PRIVILEGES ON DATABASE "HOSPIAL ESPERO QUE EL FINAL" TO admins;
```
Donar permisos de creació de taules i roles:
```
ALTER ROLE admins CREATEDB CREATEROLE;
```

<br>

**ADMINISTRATIUS:** (PERSONAL VARI) (RAFA)
-	Accés a les taules de RESERVA, PACIENT, VISITA, OPERACIO, QUIROFAN, HABITACIO, i PERSONAL.
-	Pot realitzar operacions d'inserció, actualització i eliminació en aquestes taules per a gestionar reserves, pacients, visites, operacions quirúrgiques, quiròfans, habitacions i personal.
-	No hauria de tenir permisos per a modificar taules relacionades amb detalls mèdics específics , com els medicaments o els registres mèdics dels pacients.

Crear rols:
```
CREATE ROLE administratius;
```
Crear el usuari de administratius:
```
CREATE USER rafa_pacheco WITH PASSWORD 'rafita1234';
GRANT administratius TO rafa_pacheco;
```
Primer li triem tots els permisos per tenir mes seguretat: *(Llista negre)* 
```
REVOKE ALL PRIVILEGES ON aparell_medic, habitacio, medicament, operacio, pacient, personal, personal_infermeria, personal_medic, personal_vari, planta, quirofan, reserva, visita, visita_medicament FROM administratius;
```
I ara posem els permisos:
```
GRANT SELECT ON reserva, pacient, visita, operacio, quirofan, habitacio, personal TO administratius;
GRANT INSERT, UPDATE, DELETE ON reserva, pacient, visita, operacio, quirofan, habitacio, personal TO administratius;
```

<br>

**Personal_medic** (Anna Lopez):
-	Accés a les taules de PACIENT, VISITA, OPERACIO, HABITACIO, PERSONAL_MEDIC VISITA_MEDICAMENT.
-	Poden veure i actualitzar informació sobre pacients, visites mèdiques, operacions, assignació d'habitacions, assignació de personal mèdic i medicaments receptats.
-	No haurien de tenir permisos per a modificar informació administrativa general, com les taules de RESERVA o QUIROFAN.

Crear el rol:
```
CREATE ROLE personal_medic
```
Creem el usuari i assignem el rol:
```
CREATE USER anna_lopez WITH PASSWORD 'anna1234';
GRANT personal_medic TO anna_lopez;
```
Primer li triem tots els permisos per tenir mes seguretat: *(Llista negre)* 
```
REVOKE ALL PRIVILEGES ON aparell_medic , habitacio , medicament , operacio , pacient , personal , personal_infermeria , personal_medic , personal_vari , planta , quirofan , reserva , visita , visita_medicament FROM personal_medic;
```
Li donem permisos:
```
GRANT SELECT, UPDATE ON PACIENT, VISITA, OPERACIO, HABITACIO, PERSONAL_MEDIC, VISITA_MEDICAMENT TO personal_medic;
```

<br>

**INFERMERS** (Cristiano_Ronaldo):
-	Accés a les taules de PACIENT, OPERACIO, HABITACIO, PERSONAL_INFERMERIA.
-	Poden veure i actualitzar informació sobre pacients, assignació d'habitacions, assignació de personal d'infermeri i detalls de les operacions quirúrgiques.
-	No haurien de tenir permisos per a modificar informació administrativa general o detalls mèdics específics, com les taules de RESERVA o MEDICAMENT.
Crear rol:
```
CREATE ROLE infermers:
```
Crear el usuari i assignar el rol:
```
CREATE USER cristiano_ronaldo WITH PASSWORD 'CR7';
GRANT infermers TO cristiano_ronaldo;
```
Primer li triem tots els permisos per tenir mes seguretat: *(Llista negre)* 
```
REVOKE ALL PRIVILEGES ON aparell_medic , habitacio , medicament , operacio , pacient , personal , personal_infermeria , personal_medic , personal_vari , planta , quirofan , reserva , visita , visita_medicament FROM infermers;
```
Permisos:
```
GRANT SELECT, UPDATE ON PACIENT, OPERACIO, HABITACIO, PERSONAL_INFERMERIA TO infermers;
```

<br>

**MANTENIMENT** (PERSONAL VARI):
-	Accés limitat a les taules necessàries per a realitzar les seves funcions específiques, com HABITACIO i PERSONAL_VARI.
-	Poden veure i actualitzar informació sobre les habitacions assignades i les tasques assigna-dones a ells.
-	No haurien de tenir accés a informació confidencial de pacients o detalls mèdics.

Crear rol:
```
CREATE ROLE manteniment
```
Crear el usuari i assignar el rol:
```
CREATE USER monica_paredes WITH PASSWORD ‘monica1234’;
GRANT manteniment TO monica_paredes;
```
Primer li triem tots els permisos per tenir mes seguretat: *(Llista negre)* 
```
REVOKE ALL PRIVILEGES ON aparell_medic , habitacio , medicament , operacio , pacient , personal , personal_infermeria , personal_medic , personal_vari , planta , quirofan , reserva , visita , visita_medicament FROM manteniment;
```
Permisos:
```
GRANT SELECT, UPDATE ON HABITACIO, PERSONAL_VARI TO manteniment;
```

<br>

Data Masking
------------
Instalem pgxclient 

<br>

![Imatge1](Imatges/DataMasking.jpg)

<br>

Aqui instalem l'anonymizer

<br>

![Imatge2](Imatges/DataMasking1.jpg)

<br>

Creem la extensió ANNON i li posem les seves llibreries

<br>

![Imatge3](Imatges/DataMasking2.jpg)

<br>

Reiniciem el servei 

<br>

![Imatge4](Imatges/DataMasking3.jpg)

<br>

Xifrem la columna DNI

<br>

![Imatge5](Imatges/DataMasking4.jpg)

<br>

# Readme
#### [1.Primera Entrega Planificació del projecte (BD + PRG) ](https://github.com/Ruizzy98/Projecte-DAPM/tree/main/1.%20Primera%20Entrega%20Planificaci%C3%B3%20del%20projecte%20(BD%20%2B%20PRG))
#### [2. Segona Entrega Bloc de conectivitat i login](https://github.com/Ruizzy98/Projecte-DAPM/tree/main/2.%20Segona%20Entrega%20Bloc%20de%20conectivitat%20i%20login)
#### [3. Tercera Entrega Disseny ER-Model Relacional](https://github.com/Ruizzy98/Projecte-DAPM/tree/main/3.%20Tercera%20Entrega%20Disseny%20ER-Model%20Relacional)
#### [4. Quarta Entrega Esquema de seguretat](https://github.com/Ruizzy98/Projecte-DAPM/tree/main/4.%20Quarta%20Entrega%20Esquema%20de%20seguretat)
#### [5. Cinquena Entrega Esquema de seguretat](https://github.com/Ruizzy98/Projecte-DAPM/tree/main/5.%20Cinquena%20Entrega%20Bloc%20de%20manteniment)
#### [6. Sisena Entrega Esquema de seguretat](https://github.com/Ruizzy98/Projecte-DAPM/tree/main/6.%20Sisena%20Entrega%20Esquema%20d'alta%20disponibilitat) 
