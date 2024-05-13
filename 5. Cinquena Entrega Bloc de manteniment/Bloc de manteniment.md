Això fa un llistat dels pacients que hem inserit
```
CREATE OR REPLACE FUNCTION deus(
    num_plantes_input INT
)
RETURNS TABLE (
    id_pacient INT,
    nom VARCHAR(25),
    cognom VARCHAR(50),
    id_reserva INT,
    num_plantes INT
) AS $$
BEGIN
    RETURN QUERY
    SELECT p.id_pacient, p.nom, p.cognom, r.id_reserva, h.num_plantes
    FROM pacient p
    INNER JOIN reserva r ON p.id_reserva = r.id_reserva
    INNER JOIN habitacio h ON r.id_reserva = h.id_reserva
    WHERE h.num_plantes = num_plantes_input;
END;
$$ LANGUAGE plpgsql;
```
Per confirmar que tot està correcte, haurem de fer la següent sentencia:
```
SELECT * FROM deus(4);
```
![imatge1](Imatges/image.png)<br>

Creem una funció per la consulta
```
CREATE OR REPLACE FUNCTION data_consulta(
    fecha_consulta DATE
)
RETURNS TABLE (
    nom_quirofan CHAR(4),
    operacion_prevista TEXT,
    dia_ingres DATE,
    medico_ssa TEXT,
    personal_infermeria TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT q.nom_quirofan,
           'Operación de ' || pm.especialitat || ' al paciente ' || p.nom || ' ' || p.cognom AS operacion_prevista,
           r.dia_ingres,
           CONCAT(med.nom, ' ', med.cognom) AS medico,
           CONCAT(p.nom, ' ', p.cognom) AS pacient
    FROM quirofan q
    INNER JOIN operacio o ON q.nom_quirofan = o.nom_quirofan
    INNER JOIN personal_medic pm ON o.id_operacio = pm.id_operacio
    INNER JOIN personal med ON pm.id_personal = med.id_personal
    INNER JOIN personal_infermeria pi ON pm.id_infermeria = pi.id_infermeria
    INNER JOIN reserva r ON o.id_reserva = r.id_reserva
    INNER JOIN pacient p ON r.id_reserva = p.id_reserva
    WHERE DATE(r.dia_ingres) = fecha_consulta;
END;
$$ LANGUAGE plpgsql;
```
Per confirmar que tot està correcte, haurem de fer la següent sentencia:
```
SELECT * FROM data_consulta('2024-04-21');
````
![imatge2](Imatges/image2.png)<br>

# Readme
#### [1.Primera Entrega Planificació del projecte ](https://github.com/Ruizzy98/Projecte-DAPM/tree/main/1.%20Primera%20Entrega%20Planificaci%C3%B3%20del%20projecte%20(BD%20%2B%20PRG))
#### [2. Segona Entrega Bloc de conectivitat i login](https://github.com/Ruizzy98/Projecte-DAPM/tree/main/2.%20Segona%20Entrega%20Bloc%20de%20conectivitat%20i%20login)
#### [3. Tercera Entrega Disseny ER-Model Relacional](https://github.com/Ruizzy98/Projecte-DAPM/tree/main/3.%20Tercera%20Entrega%20Disseny%20ER-Model%20Relacional)
#### [4. Quarta Entrega Esquema de seguretat](https://github.com/Ruizzy98/Projecte-DAPM/tree/main/4.%20Quarta%20Entrega%20Esquema%20de%20seguretat)
#### [5. Cinquena Entrega Esquema de seguretat](https://github.com/Ruizzy98/Projecte-DAPM/tree/main/5.%20Cinquena%20Entrega%20Bloc%20de%20manteniment)
#### [6. Sisena Entrega Esquema de seguretat](https://github.com/Ruizzy98/Projecte-DAPM/tree/main/6.%20Sisena%20Entrega%20Esquema%20d'alta%20disponibilitat)
#### [7. Setena Entrega Bloc de consultes](https://github.com/Ruizzy98/Projecte-DAPM/tree/main/7.%20Setena%20Entrega%20Bloc%20de%20consultes)
#### [8. Vuitena Entrega Dummy Data](https://github.com/Ruizzy98/Projecte-DAPM/tree/main/8.%20Vuitena%20Entrega%20Dummy%20Data)
