# <p align="center">  Creació de Logs </p>

Fem una creació de logs de tots els usuaris per tal de veure els usuaris que han accedit a les dades dels pacients, amb l'objectiu d'identificar usos incorrectes del sistema.

Per fer-ho hem creat aquesta taula, que fa de registre dels usuaris que han modificat les dades dels pacients.
```
CREATE TABLE pacient_audit (
    audit_id SERIAL PRIMARY KEY,
    action_type VARCHAR(10),
    id_pacient INT,
    nom VARCHAR(255),
    cognom VARCHAR(255),
    action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    username VARCHAR(255)
);
```
Seguidament, hem creat aquesta funció, per indicar els detalls de les insercions.
```
CREATE OR REPLACE FUNCTION trg_pacient_insert_func()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO pacient_audit (action_type, id_pacient, nom, cognom, username)
    VALUES ('INSERT', NEW.id_pacient, NEW.nom, NEW.cognom, current_user);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```
Després d'inserir, es crea un registre en l'anterior taula amb la informació detallada convenient.
```
CREATE TRIGGER trg_pacient_insert
AFTER INSERT ON pacient
FOR EACH ROW
EXECUTE FUNCTION trg_pacient_insert_func();
```
Amb aquest trigger, indiquem que s'ha realitzat un canvi.
```
CREATE OR REPLACE FUNCTION trg_pacient_update_func()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO pacient_audit (action_type, id_pacient, nom, cognom, username)
    VALUES ('UPDATE', NEW.id_pacient, NEW.nom, NEW.cognom, current_user);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```
Ara creem aquest trigger, després de cada actualització d'un registre en la taula pacient, executa la funció anterior.
```
CREATE TRIGGER trg_pacient_update
AFTER UPDATE ON pacient
FOR EACH ROW
EXECUTE FUNCTION trg_pacient_update_func();
```
Fa el mateix amb els usuaris que són eliminats.
```
CREATE OR REPLACE FUNCTION trg_pacient_delete_func()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO pacient_audit (action_type, id_pacient, nom, cognom, username)
    VALUES ('DELETE', OLD.id_pacient, OLD.nom, OLD.cognom, current_user);
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;
```
Crea un registre de les dades eliminades de la taula pacients.
```
CREATE TRIGGER trg_pacient_delete
AFTER DELETE ON pacient
FOR EACH ROW
EXECUTE FUNCTION trg_pacient_delete_func();
```
