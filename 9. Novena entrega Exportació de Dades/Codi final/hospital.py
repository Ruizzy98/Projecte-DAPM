import csv
import psycopg2
from psycopg2 import Error
from cryptography.fernet import Fernet
from lxml import etree
from Duuuumyy import *


def carregar_clau():
    with open("clau.key", "rb") as arxiu_clau:
        return arxiu_clau.read()

def xifrar_dada(dada, clau):
    fernet = Fernet(clau)
    dada_xifrada = fernet.encrypt(dada.encode())
    return dada_xifrada.decode()

def desxifrar_dada(dada_xifrada, clau):
    fernet = Fernet(clau)
    dada_desxifrada = fernet.decrypt(dada_xifrada).decode()
    return dada_desxifrada


def conectar_postgresql(usuari:str, contrasenya:str):
        try:
            connection = psycopg2.connect(user=usuari,
                                          password=contrasenya,
                                          host="192.168.56.107",
                                          port="5432",
                                          dbname="hospital",
                                          connect_timeout=1)
            return connection
        except (Exception, Error) as error: 
            try:
                connection = psycopg2.connect(user=usuari,
                                            password=contrasenya,
                                            host="192.168.56.110",
                                            port="5432",
                                            dbname="hospital",
                                            connect_timeout=1)
                return connection
            except (Exception, Error) as error:
                return None

    
def crearUsuari(usuari:str,contrasenya:str):
    fitxer = []
    existeix = False
    clau = carregar_clau()
    usuari_cifrat = xifrar_dada(usuari, clau)
    contrasenya_cifrada = xifrar_dada(contrasenya, clau) 
    
    with open("usuaris.csv", 'r', newline='') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            fitxer.append(row)
    
    for credencial in fitxer:
        usuari_desxifrat = desxifrar_dada(credencial['Usuari'], clau)
        if  usuari == usuari_desxifrat:
            print("L'usuari ja existeix.")
            existeix = True 

    if existeix == False:
        connexio = conectar_postgresql("postgres","12345")
        print("Selecciona l'usuari a crear:")
        print("1. Metge ")
        print("2. Infermer/a ")
        print("3. Personal Vari")  
        opcio = input("Introdueix una opció: ")
        if opcio == "1":
            if connexio is not None:
                cursor = connexio.cursor()
                nom = input("Introdueix el nom del metge: ")
                cognom = input("Introdueix el cognom del metge: ")
                dni = usuari
                especialitat = input("Introdueix l'especialitat del metge: ")
                curriculum = input("Introdueix el currículum del metge: ")
                estudis = input("Introdueix els estudis del metge: ")
                
                insert_query_personal= """
                INSERT INTO personal (nom, cognom, dni)
                VALUES (%s, %s, %s) RETURNING id_personal;
                """        
                cursor.execute(insert_query_personal, (nom, cognom, dni))
                id_personal = cursor.fetchone()[0]
                
                insert_query_medic = """
                INSERT INTO personal_medic ( especialitat, curriculum, estudis, id_personal)
                VALUES (%s, %s, %s, %s);
                """
                cursor.execute(insert_query_medic, (especialitat, curriculum, estudis, id_personal))
                role = "metge"
        if opcio == "2":
            if connexio is not None:
                cursor = connexio.cursor()
                nom = input("Introdueix el nom de l'infermer/a: ")
                cognom = input("Introdueix el cognom de l'infermer/a: ")
                dni = usuari
                estudis = input("Introdueix els estudis de l'infermer/a: ")
                especialitat = input("Introdueix l'especialitat de l'infermer/a: ")
                curriculum = input("Introdueix el currículum de l'infermer/a: ")
                num_plantes = input("Introdueix el número de planta de l'infermer/a: ")
                if num_plantes:
                    id_medic = None
                else:
                    num_plantes = None
                    id_medic = input("Introdueix l'ID del metge: ")
                
                insert_query_personal= """
                INSERT INTO personal (nom, cognom, dni)
                VALUES (%s, %s, %s) RETURNING id_personal;
                """        
                cursor.execute(insert_query_personal, (nom, cognom, dni))
                id_personal = cursor.fetchone()[0]
                
                insert_query_infermeria = """
                INSERT INTO personal_infermeria (estudis, especialitat, curriculum, id_personal, num_plantes,id_medic)
                VALUES (%s, %s, %s,%s, %s, %s);
                """
                cursor.execute(insert_query_infermeria, (estudis, especialitat, curriculum, id_personal, num_plantes,id_medic))
                role = "enfermer"
        if opcio == "3":
            if connexio is not None:
                cursor = connexio.cursor()
                nom = input("Introdueix el nom del personal vari: ")
                cognom = input("Introdueix el cognom del personal vari: ")
                dni = usuari
                tipus_de_feina = input("Introdueix el tipus de feina del personal vari: ")
                
                insert_query_personal= """
                INSERT INTO personal (nom, cognom, dni)
                VALUES (%s, %s, %s) RETURNING id_personal;
                """        
                cursor.execute(insert_query_personal, (nom, cognom, dni))
                id_personal = cursor.fetchone()[0]
                
                insert_query_vari = """
                INSERT INTO personal_vari (tipus_de_feina, id_personal)
                VALUES (%s, %s);
                """
                cursor.execute(insert_query_vari, (tipus_de_feina, id_personal))
                role = "personal_vari"
                
        nou_usuari = {'Usuari': usuari_cifrat, 'Contrasenya': contrasenya_cifrada} 
        fitxer.append(nou_usuari)
        
        with open("usuaris.csv", 'w', newline='') as f:
            capcalera = ['Usuari', 'Contrasenya'] 
            writer = csv.DictWriter(f, fieldnames=capcalera, delimiter=';')
            writer.writeheader()
            writer.writerows(fitxer)
            
        if connexio is not None:
            cursor = connexio.cursor()
            cursor.execute(f"CREATE ROLE \"{usuari}\" LOGIN PASSWORD '{contrasenya}'")
            connexio.commit()
            
            cursor.execute(f"GRANT {role} TO \"{usuari}\"")
            connexio.commit()
            cursor.close()
            connexio.close()
        print("Usuari creat correctament.")    

def iniciar_sesio(usuari:str, contrasenya:str):
    fitxer = []
    clau = carregar_clau()
    with open("usuaris.csv", 'r', newline='') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            fitxer.append(row)
    
    for credencial in fitxer:
        usuari_desxifrat = desxifrar_dada(credencial['Usuari'], clau)
        contrasenya_desxifrada = desxifrar_dada(credencial['Contrasenya'], clau)
        if usuari == usuari_desxifrat and contrasenya == contrasenya_desxifrada:
            connexio = conectar_postgresql(usuari,contrasenya)
            if connexio is not None:
                cursor = connexio.cursor()
                cursor.execute("SELECT CURRENT_USER;")
                print(f"estas conectat amb l'usuari {usuari} ")
                cursor.close()
                connexio.close()
            return True
    return False        

def obtenir_dependencia_enfermeria(id_infermeria):
    connexio = conectar_postgresql("postgres","12345")
    if connexio is not None:
        try:
            cursor = connexio.cursor()
            consulta = """
            SELECT p.nom AS nom_metge, pi.id_infermeria AS id_infermeria, pi.num_plantes                   
                FROM PERSONAL_MEDIC pm
                INNER JOIN PERSONAL p ON p.id_personal = pm.id_personal
                RIGHT JOIN PERSONAL_INFERMERIA pi ON pi.id_medic = pm.id_medic
            WHERE pi.id_infermeria = %s
            """
            cursor.execute(consulta, (id_infermeria,))
            resultat = cursor.fetchone()
            if resultat:
                nom_metge = resultat[0]
                id_infermeria = resultat[1]
                num_plantes = resultat[2]
               
                print("Id de la infermeria:", id_infermeria)
                if nom_metge:
                    print("Depen del metge:", nom_metge)
                if num_plantes:
                    print("Número de planta:", num_plantes)
            else:
                print("ID incorrecte")
            cursor.close()
            connexio.close()
        except psycopg2.Error as e:
            print("Error al ejecutar la consulta:", e)
    else:
        print("No s'ha pogut connectar a la base de dades.")     


def obtenir_noms_infermeria(id_medic):
    connexio = conectar_postgresql("postgres", "12345")
    if connexio is not None:
        try:
            cursor = connexio.cursor()
            consulta = """
            SELECT CONCAT(p.nom, ' ', p.cognom) AS nom_personal_infermeria
            FROM personal_infermeria pi
            INNER JOIN personal p ON p.id_personal = pi.id_personal
            WHERE pi.id_medic = %s
            """
            cursor.execute(consulta, (id_medic,))
            resultats = cursor.fetchall()
            nom_infermeria = [resultat[0] for resultat in resultats]
            return nom_infermeria
        except psycopg2.Error as e:
            print("Error al executar la consulta:", e)
        finally:
            cursor.close()
            connexio.close()
    else:
        print("No s'ha pogut connectar a la base de dades.")


def info_operacions(dia):
    connexio = conectar_postgresql("postgres", "12345")
    if connexio is not None:
        try:
            cursor = connexio.cursor()
            consulta = """
            SELECT r.nom_quirofan,
                CONCAT(TO_CHAR(EXTRACT(HOUR FROM r.dia_ingres), 'FM00'), ':', TO_CHAR(EXTRACT(MINUTE FROM r.dia_ingres), 'FM00')) AS hora_ingres_minut,
                CONCAT(pe.nom, ' ', pe.cognom) AS nom_metge,
                CONCAT(p.nom, ' ', p.cognom) AS nom_pacient,
                o.id_medic
            FROM RESERVA r
            INNER JOIN OPERACIO o ON r.id_reserva = o.id_reserva
            INNER JOIN PACIENT p ON o.id_pacient = p.id_pacient
            INNER JOIN PERSONAL_MEDIC pm ON pm.id_medic = o.id_medic
            INNER JOIN PERSONAL pe ON pm.id_personal = pe.id_personal
            WHERE DATE(r.dia_ingres) = %s
            ORDER BY r.nom_quirofan;
            """
            
            cursor.execute(consulta, (dia,))
            resultats = cursor.fetchall()
            
            if resultats:
                print("-" * 100)
                print("| Quirofan    | Hora  |   Nom del Metge   |   Nom del Pacient   | Noms Infermers/as ")
                print("|-------------|-------|-------------------|---------------------|-----------------------------------")
                for resultat in resultats:
                    quirofan = resultat[0]
                    hora_ingres_minut = resultat[1]
                    nom_metge = resultat[2]
                    nom_pacient = resultat[3]
                    id_medic = resultat[4]
                    noms_infermeria = obtenir_noms_infermeria(id_medic)
                    nom_infermeria_str = ", ".join(noms_infermeria)
                    print("| {:<11} | {:>5} | {:^17} | {:^19} | {:<30} ".format(quirofan, hora_ingres_minut, nom_metge, nom_pacient, nom_infermeria_str))
                print("-" * 100)
            else:
                print("No hi ha resultats per a aquest dia.")
            
            cursor.close()
            connexio.close()
        except psycopg2.Error as e:
            print("Error al executar la consulta:", e)
    else:
        print("No s'ha pogut connectar a la base de dades.")
        
def info_visita(dia_visita):
    connexio = conectar_postgresql("postgres","12345")
    if connexio is not None:
        try:
            cursor = connexio.cursor()
            consulta = """
           SELECT CONCAT(TO_CHAR(EXTRACT(HOUR FROM v.data_hora), 'FM00'), ':', TO_CHAR(EXTRACT(MINUTE FROM v.data_hora), 'FM00')) AS hora_minut,
                CONCAT(pe.nom, ' ', pe.cognom) AS nom_metge,
		        CONCAT(p.nom, ' ', p.cognom) AS nom_pacient
            FROM visita v
            INNER JOIN pacient p ON p.id_pacient = v.id_pacient
            INNER JOIN personal_medic pm ON pm.id_medic = v.id_medic
            INNER JOIN personal pe ON pe.id_personal = pm.id_personal
            WHERE DATE(v.data_hora) = %s
            ORDER BY v.data_hora;
            """
            cursor.execute(consulta, (dia_visita,))
            resultats = cursor.fetchall()
            print("Visites del dia", dia_visita)
            if resultats:
                print("-" * 51)
                print("| Hora  |   Nom del Metge   |   Nom del Pacient   |")
                print("|-------|-------------------|---------------------|")
                for resultat in resultats:
                    hora = resultat[0]
                    nom_metge = resultat[1]
                    nom_pacient = resultat[2]
                    print("| {:>2} | {:^17} | {:^19} |".format(hora, nom_metge, nom_pacient))
                    print("|-------|-------------------|---------------------|")
            else:
                print("No s'han trobat visites per a la data especificada.")
            
            print("\n")
            cursor.close()
            connexio.close()
        except psycopg2.Error as e:
            print("Error al executar la consulta:", e)
    else:
        print("No s'ha pogut connectar a la base de dades.")

def reserves_habitacio(id_habitacio):
    connexio = conectar_postgresql("postgres","12345")  
    if connexio is not None:
        try:
            cursor = connexio.cursor()
            consulta = """
            SELECT pi.dia_ingres, pi.dia_sortida, CONCAT(p.nom, ' ', p.cognom) AS nom_pacient
                FROM pacient_ingressat pi
            INNER JOIN pacient p ON p.id_pacient = pi.id_pacient
            WHERE pi.num_habitacio = %s AND pi.dia_ingres > CURRENT_DATE
            ORDER BY pi.dia_ingres
            """
            cursor.execute(consulta, (id_habitacio,))
            resultat = cursor.fetchall()
            
            if resultat:
                print("Reserves de la habitació", id_habitacio)
                print("-" * 67)
                print("|  Data d'ingrés      |  Data de sortida    | Nom del pacient     |")
                print("|---------------------|---------------------|---------------------|")
                for resultat in resultat:
                    data_ingres = resultat[0]
                    data_sortida = resultat[1]
                    nom_pacient = resultat[2]
                    print("| {:>19} | {:^19} | {:<19} |".format(data_ingres.strftime('%Y-%m-%d %H:%M:%S'), data_sortida.strftime('%Y-%m-%d %H:%M:%S'), nom_pacient))
                    print("|---------------------|---------------------|---------------------|")
            else:
                print("No s'han trobat visites previstes per l'habitació especificada.")
            
            cursor.close()
            connexio.close()
        except psycopg2.Error as e:
            print("Error al executar la consulta:", e)
    else:
        print("No s'ha pogut connectar a la base de dades.")


def obtenir_medicaments(id_visita):
    connexio = conectar_postgresql("postgres","12345")
    if connexio is not None:
        try:
            cursor = connexio.cursor()
            consulta = """
            SELECT m.nom
              FROM medicament m
            INNER JOIN visita_medicament vm ON vm.id_medicament = m.id_medicament
            WHERE vm.id_visita = %s
            """
            cursor.execute(consulta, (id_visita,))
            resultats = cursor.fetchall()
            if resultats:
                medicaments = [resultat[0] for resultat in resultats]
                return medicaments
            else:
                return ("No es van receptar medicaments en aquesta visita.")    
    
        except psycopg2.Error as e:
            print("Error al executar la consulta:", e)
        
        finally:               
            cursor.close()          
            connexio.close()
    else:
        print("No s'ha pogut connectar a la base de dades.")


def informacio_pacient(id_pacient):
    connexio = conectar_postgresql("postgres","12345")
    if connexio is not None:
        try:
            cursor = connexio.cursor()
            consulta = """
            SELECT v.data_hora,CONCAT(p.nom, ' ', p.cognom) AS nom_pacient,v.diagnostic,v.id_visita
                FROM pacient p
            INNER JOIN visita v ON v.id_pacient = p.id_pacient
            WHERE p.id_pacient = %s;
            """
            consulta_cops_ingressat = """
            SELECT COUNT(id_pacient)
                FROM pacient_ingressat 
            WHERE id_pacient =  %s;
            """
            consulta_cops_operat = """
            SELECT COUNT(id_pacient)
                FROM operacio
            WHERE id_pacient =  %s;
            """
            cursor.execute(consulta_cops_ingressat, (id_pacient,))
            cops_ingressat = cursor.fetchone()[0]
            
            cursor.execute(consulta_cops_operat, (id_pacient,))
            cops_operat = cursor.fetchone()[0]
            
            cursor.execute(consulta, (id_pacient,))
            resultats = cursor.fetchall()
            visites_pacient = cursor.rowcount
            
            print("Cops Ingressat:", cops_ingressat)
            print("Cops Operat:", cops_operat)
            if resultats:
                print("Numero de visites:", visites_pacient)
                print("-" * 92)
                print("|  Data Visita        |    Nom Pacient      |   Diagnostic        |   Medicaments receptats ")
                print("|---------------------|---------------------|---------------------|-------------------------")
                for resultat in resultats:
                    data = resultat[0]
                    nom_pacient = resultat[1]
                    diagnoctic = resultat[2]
                    id_visita = resultat[3]
                    medicaments_visites = obtenir_medicaments(id_visita)
                    if medicaments_visites != "No es van receptar medicaments en aquesta visita.":
                        medicaments = ", ".join(medicaments_visites)
                    else:
                        medicaments = medicaments_visites
                      
                    print("| {:>19} | {:^19} | {:<19} | {:<19} ".format(data.strftime('%Y-%m-%d %H:%M:%S'), nom_pacient, diagnoctic, medicaments))
                    print("|---------------------|---------------------|---------------------|------------------------")
            else:
                print("No s'han trobat visites del pacient")
            
            cursor.close()
            connexio.close()
        except psycopg2.Error as e:
            print("Error al executar la consulta:", e)
    else:
        print("No s'ha pogut connectar a la base de dades.")


def informacio_quirofan():
    connexio = conectar_postgresql("postgres","12345")
    if connexio is not None:
        try:
            cursor = connexio.cursor()
            consulta = """
            SELECT q.nom_quirofan, qa.quantitat, am.tipus_de_aparell
                FROM QUIROFAN q
                INNER JOIN QUIROFAN_APARELL_MEDIC qa ON q.nom_quirofan = qa.nom_quirofan
                INNER JOIN aparell_medic am ON am.id_aparell_medic = qa.id_aparell_medic
                ORDER BY q.nom_quirofan;
            """
            cursor.execute(consulta)
            resultats = cursor.fetchall()
            if resultats:
                quirofan_anterior = None
                for quirofan in resultats:
                    if quirofan[0] != quirofan_anterior:
                        print(f"El quirofan {quirofan[0]} te assignat:")
                        quirofan_anterior = quirofan[0]
                    print(f"- {quirofan[2]} x {quirofan[1]}")
            
            cursor.close()
            connexio.close()
        except psycopg2.Error as e:
            print("Error al executar la consulta:", e)
    else:
        print("No s'ha pogut connectar a la base de dades.")
        
def crear_pacient(nom, cognom):
    connexio = conectar_postgresql("postgres","12345")
    if connexio is not None:
        try:
            cursor = connexio.cursor()
            insert_query_pacient = """
            INSERT INTO pacient (nom, cognom)
            VALUES (%s, %s)
            """
            cursor.execute(insert_query_pacient, (nom, cognom))
            connexio.commit()
            print("Pacient creat correctament.")
            cursor.close()
            connexio.close()
        except psycopg2.Error as e:
            print("Error al executar la consulta:", e)  
        
        
def informacio_plantes(num_plantes):
    connexio = conectar_postgresql("postgres", "12345")
    if connexio is not None:
        try:
            cursor = connexio.cursor()
            consulta_habitacions = """
            SELECT count(num_habitacio)
            FROM habitacio
            WHERE num_plantes = %s
            """
            consulta_quirofans = """
            SELECT count(nom_quirofan)
            FROM quirofan
            WHERE num_plantes = %s
            """
            consulta_enfermeria = """
            SELECT count(id_infermeria)
            FROM personal_infermeria
            WHERE num_plantes = %s
            """
            
            cursor.execute(consulta_habitacions, (num_plantes,))
            resultats_habitacions = cursor.fetchone()[0]
            
            cursor.execute(consulta_quirofans, (num_plantes,))
            resultats_quirofans = cursor.fetchone()[0]
            
            cursor.execute(consulta_enfermeria, (num_plantes,))
            resultats_enfermeria = cursor.fetchone()[0]
            
            print("Nombre d'habitacions:", resultats_habitacions)
            print("Nombre de quirofans:", resultats_quirofans)
            print("Nombre de personal d'infermeria:", resultats_enfermeria)
            
            cursor.close()
            connexio.close()
        except psycopg2.Error as e:
            print("Error al executar la consulta:", e)
    else:
        print("No s'ha pogut connectar a la base de dades.")
        
def informe_visites(dia_visita):
    connexio = conectar_postgresql("postgres","12345")
    if connexio is not None:
        try:
            cursor = connexio.cursor()
            consulta = """
           SELECT CONCAT(TO_CHAR(EXTRACT(HOUR FROM v.data_hora), 'FM00'), ':', TO_CHAR(EXTRACT(MINUTE FROM v.data_hora), 'FM00')) AS hora_minut,
                CONCAT(pe.nom, ' ', pe.cognom) AS nom_metge,
		        CONCAT(p.nom, ' ', p.cognom) AS nom_pacient,
				v.diagnostic,
                v.id_visita
            FROM visita v
            INNER JOIN pacient p ON p.id_pacient = v.id_pacient
            INNER JOIN personal_medic pm ON pm.id_medic = v.id_medic
            INNER JOIN personal pe ON pe.id_personal = pm.id_personal
            WHERE DATE(v.data_hora) = %s
            ORDER BY v.data_hora;
            """
            cursor.execute(consulta, (dia_visita,))
            resultats = cursor.fetchall()
            print("Visites del dia", dia_visita)
            if resultats:
                print("-" * 98)
                print("| Hora  |   Nom del Metge   |   Nom del Pacient   |      Diagnostic     |      Medicament         ")
                print("|-------|-------------------|---------------------|---------------------|-------------------------")
                for resultat in resultats:
                    hora = resultat[0]
                    nom_metge = resultat[1]
                    nom_pacient = resultat[2]
                    diagnostic = resultat[3]
                    id_visita = resultat[4]
                    medicaments_visites = obtenir_medicaments(id_visita)
                    if medicaments_visites != "No es van receptar medicaments en aquesta visita.":
                        medicaments = ", ".join(medicaments_visites)
                    else:
                        medicaments = medicaments_visites
                        
                    print("| {:>2} | {:^17} | {:^19} |{:^21}| {:^21}".format(hora, nom_metge, nom_pacient, diagnostic, medicaments))
                    print("|-------|-------------------|---------------------|---------------------|-------------------------")
            else:
                print("No s'han trobat visites per a la data especificada.")
            
            print("\n")
            cursor.close()
            connexio.close()
        except psycopg2.Error as e:
            print("Error al executar la consulta:", e)
    else:
        print("No s'ha pogut connectar a la base de dades.")

def informe_personal():
    connexio = conectar_postgresql("postgres", "12345")
    if connexio is not None:
        try:
            cursor = connexio.cursor()
            consulta_personal_vari = """
            SELECT CONCAT(p.nom, ' ', p.cognom) AS nom_personal, p.dni, pv.tipus_de_feina
                FROM personal p 
            INNER JOIN personal_vari pv ON pv.id_personal = p.id_personal
            """
            consulta_personal_personal_enfermeria = """
            SELECT CONCAT(p.nom, ' ', p.cognom) AS nom_personal, p.dni, pi.especialitat
                FROM personal p 
                INNER JOIN personal_infermeria pi ON pi.id_personal = p.id_personal;
            """
            consulta_personal_medic = """
            SELECT CONCAT(p.nom, ' ', p.cognom) AS nom_personal, p.dni, pm.especialitat
                FROM personal p 
                INNER JOIN personal_medic pm ON pm.id_personal = p.id_personal;
            """
            cursor.execute(consulta_personal_vari)
            dades_personal_vari = cursor.fetchall()
            
            cursor.execute(consulta_personal_personal_enfermeria)
            dades_personal_infermeria = cursor.fetchall()
            
            cursor.execute(consulta_personal_medic)
            dades_personal_medic = cursor.fetchall()
            
            if dades_personal_vari:
                print("Personal Vari")
                print("-" * 62)
                print("|  Nom del personal   |       DNI       |    Tipus de feina   |")
                print("|---------------------|-----------------|---------------------|")
                for personal_vari in dades_personal_vari:
                    nom_personal = personal_vari[0]
                    dni = personal_vari[1]
                    tipus_feina = personal_vari[2]
                    print("| {:<19} | {:<15} | {:<19} | ".format(nom_personal, dni, tipus_feina))
                    print("|---------------------|-----------------|---------------------|")
            else:
                print("No s'han trobat resultats.")
                
            if dades_personal_infermeria:
                print("Personal Infermeria")
                print("-" * 62)
                print("|  Nom del personal   |       DNI       |    Especialitat     |")
                print("|---------------------|-----------------|---------------------|")
                for personal_infermeria in dades_personal_infermeria:
                    nom_personal = personal_infermeria[0]
                    dni = personal_infermeria[1]
                    especialitat = personal_infermeria[2]
                    print("| {:<19} | {:<15} | {:<19} | ".format(nom_personal, dni, especialitat))
                    print("|---------------------|-----------------|---------------------|")
            else:
                print("No s'han trobat resultats.")
                
            if dades_personal_medic:
                print("Personal Medic")
                print("-" * 62)
                print("|  Nom del personal   |       DNI       |    Especialitat     |")
                print("|---------------------|-----------------|---------------------|")
                for personal_medic in dades_personal_medic:
                    nom_personal = personal_medic[0]
                    dni = personal_medic[1]
                    especialitat = personal_medic[2]
                    print("| {:<19} | {:<15} | {:<19} | ".format(nom_personal, dni, especialitat))
                    print("|---------------------|-----------------|---------------------|")
            else:
                print("No s'han trobat resultats.")
                  
            cursor.close()
            connexio.close()
        except psycopg2.Error as e:
            print("Error al executar la consulta:", e)
    else:
        print("No s'ha pogut connectar a la base de dades.") 
   
def ranking_metges():
    connexio = conectar_postgresql("postgres", "12345")
    if connexio is not None:
        cursor = connexio.cursor()
        consulta_top_visites = """
        SELECT CONCAT(p.nom, ' ', p.cognom), COUNT(v.id_visita)
            FROM personal p
        INNER JOIN personal_medic pm ON p.id_personal = pm.id_personal
        INNER JOIN visita v ON v.id_medic = pm.id_medic
        GROUP BY CONCAT(p.nom, ' ', p.cognom)
        ORDER BY COUNT(v.id_visita) DESC, CONCAT(p.nom, ' ', p.cognom) ASC;
        """
        cursor.execute(consulta_top_visites)
        resultats = cursor.fetchall()
        cursor.close()
        for nom, quantitat in resultats:
            print(f"Nom Metge: {nom}, Visites: {quantitat}")
    else:
        print("No s'ha pogut connectar a la base de dades.")
    cursor.close()
    connexio.close()

def ranking_malaltia():
    connexio = conectar_postgresql("postgres", "12345")
    if connexio is not None:
        cursor = connexio.cursor()
        consulta_top_malalties = """
        SELECT v.diagnostic, COUNT (v.id_visita)
            FROM visita v
        GROUP BY v.diagnostic
        ORDER BY COUNT (v.id_visita) DESC;
        """
        cursor.execute(consulta_top_malalties)
        resultats = cursor.fetchall()
        cursor.close()
        for malaltia, quantitat in resultats:
            print(f"Malaltia: {malaltia}, Quantitat: {quantitat}")
    else:
        print("No s'ha pogut connectar a la base de dades.")
    cursor.close()
    connexio.close()
    
def generar_xml(data_inici, data_fi):
    directori = input("Introdueix el directori on vols guardar el fitxer XML:")
    connexio = conectar_postgresql("postgres", "12345")
    if connexio is not None:
        cursor = connexio.cursor()
        consulta_xml = f"""
        SELECT xmlserialize(
            content xmlelement(
                name "hospital",
                XMLAGG(xml_resultats)
            ) 
            as text
        ) AS xml_output
        FROM (
            SELECT XMLELEMENT(
                    NAME "visita",
                    XMLFOREST(
                        v.id_visita,
                        p.nom AS "Nom",
                        p.cognom AS "Cognom",
                        v.data_hora AS "Data",
                        CONCAT(pe.nom, ' ', pe.cognom) AS "Metge"
                    )
                ) AS xml_resultats
            FROM visita v 
            INNER JOIN pacient p ON p.id_pacient = v.id_pacient
            INNER JOIN personal_medic pm ON pm.id_medic = v.id_medic
            INNER JOIN personal pe ON pe.id_personal = pm.id_personal
            WHERE v.data_hora BETWEEN '{data_inici}' AND '{data_fi}'
            ORDER BY v.data_hora
        ) AS visites_xml;
        """
        cursor.execute(consulta_xml)
        resultat_xml = cursor.fetchone()[0]

        xml_visitas = etree.fromstring(resultat_xml)
        print(etree.tostring(xml_visitas, encoding='utf-8', pretty_print=True).decode())
        
        with open(directori+"/visites_pacients.xml", "wb") as xml_file:
            xml_file.write(etree.tostring(xml_visitas, encoding='utf-8', pretty_print=True))

        print("XML generat correctament.")

        cursor.close()
        connexio.close()

    else:
        print("No s'ha pogut connectar a la base de dades.")
    
def mostrar_menu_manteniments():
    while True:
        print("-" * 92)
        print(" " * 28 + "Menú Manteniments")
        print("-" * 92)
        print("1.  Obtenir dependencia enfermeria")
        print("2.  Informació del quirofan")
        print("3.  Informació de les visites")
        print("4.  Informació reserves per habitació")
        print("5.  Informació del pacient")
        print("6.  Informació equip de tots els quirofans")
        print("7.  Crear un nou usuari (metge, infermer/a o personal vari)")
        print("8.  Crear un nou pacient")
        print("0.  Tornar al menú principal")
        print("-" * 92)
        opcio_mantenimient = input("Introdueix una opció: ")
        if opcio_mantenimient == "1":
            print("-" * 92)
            print(" " * 26 + "Informació Dependencia Enfermeria")
            print("-" * 92)
            id_infermeria = input("Introdueix l'ID de la infermeria: ")
            obtenir_dependencia_enfermeria(id_infermeria)
            input("Prem Enter per continuar...")
        elif opcio_mantenimient == "2":
            print("Informació de les operacions")
            data_operacios = input("Introdueix la data: ")
            info_operacions(data_operacios)
            input("Prem Enter per continuar...")
        elif opcio_mantenimient == "3":
            print("Informació de les visites")
            dia_visita = input("Introdueix la data de la visita (YYYY-MM-DD): ")
            info_visita(dia_visita)
            input("Prem Enter per continuar...")
        elif opcio_mantenimient == "4":
            print("Informació reserves per habitació")
            id_habitacio = input("Introdueix l'ID de la habitació: ")
            reserves_habitacio(id_habitacio)
            input("Prem Enter per continuar...")
        elif opcio_mantenimient == "5":
            print("Informació del pacient")
            id_pacient = input("Introdueix l'ID del pacient: ")
            informacio_pacient(id_pacient)
            input("Prem Enter per continuar...")
        elif opcio_mantenimient == "6":
            print("Informació equip de tots els quirofans")
            informacio_quirofan()
            input("Prem Enter per continuar...")
        if opcio_mantenimient == "7":
            print("Crear un nou usuari")
            dni = input("Introdueix el teu DNI: ")
            contrasenya = input("Introdueix la contrasenya: ")
            crearUsuari(dni,contrasenya)
            input("Prem Enter per continuar...")
        if opcio_mantenimient == "8":
            print("Crear un nou pacient")
            nom = input("Introdueix el nom del pacient: ")
            cognom = input("Introdueix el cognom del pacient: ")
            crear_pacient(nom, cognom)
            input("Prem Enter per continuar...")    
        elif opcio_mantenimient == "0":
            print("Tornant al menú principal...")
            break  

def mostrar_menu_dummy_data():
    while True:
        print("-" * 92)
        print(" " * 28 + "Dummy Data")
        print("-" * 92)
        print("1.  Generar les dades ")
        print("2.  Eliminar dades")
        print("0.  Tornar al menú principal")
        print("-" * 92)
        opcio_dummy_data = input("Introdueix una opció: ")
        if opcio_dummy_data == "1":
            print("Generant dades...")
            generar_dades()
            input("Prem Enter per continuar...")
        elif opcio_dummy_data == "2":
            print("Eliminant dades...")
            eliminar_dades()
            input("Prem Enter per continuar...")
        elif opcio_dummy_data == "0":   
            print("Tornant al menú principal...")
            break
 
def mostrar_menu_informes():
    while True:
        print("-" * 92)
        print(" " * 28 + "Menú de consultes i informes")
        print("-" * 92)
        print("1.  Obtenir informacio d'una planta")
        print("2.  Informe del personal de l'hospital")
        print("3.  Informe de les visites")
        print ("4.  Ranking metges")
        print ("5.  Ranking malalties")
        print("0.  Tornar al menú principal")
        print("-" * 92)
        opcio_informes_consultes = input("Introdueix una opció: ")
        if opcio_informes_consultes == "1":
            print("-" * 92)
            print(" " * 26 + "Informació d'una planta")
            print("-" * 92)
            id_planta = input("Introdueix la planta: ")
            informacio_plantes(id_planta)
            input("Prem Enter per continuar...")
        elif opcio_informes_consultes == "2":
            print("Informació del personal de l'hospital")
            informe_personal()
            input("Prem Enter per continuar...")
        elif opcio_informes_consultes == "3":
            print("Informe de les visites")
            dia_visita = input("Introdueix la data de la visita (YYYY-MM-DD): ")
            informe_visites(dia_visita)
            input("Prem Enter per continuar...")
        elif opcio_informes_consultes == "4":
            print("Ranking metges")
            ranking_metges()
            input("Prem Enter per continuar...")
        elif opcio_informes_consultes == "5":
            print("Ranking malalties")
            ranking_malaltia()
            input("Prem Enter per continuar...")
        elif opcio_informes_consultes == "0":
            print("Tornant al menú principal...")
            break  
        
def mostrar_menu():
    while True:
        print("-" * 92)
        print(" " * 33 + "Menú Login")
        print("-" * 92)
        print("1. Iniciar sessió")
        print("0. Sortir")
        numero = input("Introdueix una opció: ")
        if numero == "1":
            usuari = input("Introdueix el teu usuari: ")
            contrasenya = input("Introdueix la teva contrasenya: ")
            if iniciar_sesio(usuari, contrasenya):
                while True:
                    print("-" * 92)
                    print(" " * 28 + "Menú Gestió Hospital")
                    print("-" * 92)
                    print("1.  Manteniments")
                    print("2.  Consultes i informes")
                    print("3.  Exportació de dades")
                    print("4.  Dummy Data")
                    print("0.  Sortir")
                    opcio = input("Introdueix una opció: ")
                    if opcio == "1":
                        mostrar_menu_manteniments()
                    elif opcio == "2":
                        mostrar_menu_informes()
                    elif opcio == "3":
                        print("Exportació de dades de les visites a un fitxer XML")
                        data_inici = input("Introdueix la data d'inici (YYYY-MM-DD): ")
                        data_fi = input("Introdueix la data de fi (YYYY-MM-DD): ")
                        generar_xml(data_inici, data_fi)
                    elif opcio == "4":
                        mostrar_menu_dummy_data()
                    elif opcio == "0":
                        break 
                    else:
                        print("Opció invàlida. Si us plau, selecciona una opció vàlida.")
            else:
                print("Usuari o contrasenya incorrectes.")
        elif numero == "0":
            print("Sortint del programa...")
            break
        else:
            print("Opció invàlida. Si us plau, selecciona una opció vàlida.")
    
    
