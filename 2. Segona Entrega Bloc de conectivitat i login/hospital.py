import csv
import psycopg2
from psycopg2 import Error
from cryptography.fernet import Fernet
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


def conectar_postgresql(usuari:str,contrasenya:str):
    try:
        connection = psycopg2.connect(user=usuari,
                                      password=contrasenya,
                                      host="192.168.56.107",
                                      port="5432",
                                      dbname="hospital")
        return connection
    except (Exception, Error) as error:
        print("Error al conectar a Hospital:", error)
        return None

def crearUsuari(usuari:str,contrasenya:str, role:str):
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
        nou_usuari = {'Usuari': usuari_cifrat, 'Contrasenya': contrasenya_cifrada} 
        fitxer.append(nou_usuari)
        
        with open("usuaris.csv", 'w', newline='') as f:
            capcalera = ['Usuari', 'Contrasenya'] 
            writer = csv.DictWriter(f, fieldnames=capcalera, delimiter=';')
            writer.writeheader()
            writer.writerows(fitxer)
            
        
        connexio = conectar_postgresql("postgres","12345")
        if connexio is not None:
            cursor = connexio.cursor()
            cursor.execute(f"CREATE ROLE {usuari} LOGIN PASSWORD '{contrasenya}'")
            connexio.commit()
            
            cursor.execute(f"ALTER GROUP {role} ADD USER {usuari}")
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

def info_quirofan(nom_quirofan):
    connexio = conectar_postgresql("postgres","12345")
    if connexio is not None:
        try:
            cursor = connexio.cursor()
            consulta = """
            SELECT r.dia_ingres, r.dia_sortida, o.id_operacio, p.nom, pm.id_medic, pi.id_infermeria
            FROM reserva r
                INNER JOIN quirofan q ON q.id_reserva = r.id_reserva
                INNER JOIN operacio o ON o.id_reserva = r.id_reserva
                INNER JOIN pacient p ON p.id_reserva = r.id_reserva
                INNER JOIN personal_medic pm ON pm.id_reserva = r.id_reserva		
                INNER JOIN personal_infermeria pi ON pi.id_medic = pm.id_medic
            WHERE q.nom_quirofan = %s
            """
            cursor.execute(consulta, (nom_quirofan,))
            resultat = cursor.fetchone()
            
            if resultat:
                dia_ingres = resultat[0]
                dia_sortida = resultat[1]
                id_operacio = resultat[2]
                nom_pacient = resultat[3]
                id_medic = resultat[4]
                id_infermeria = resultat[5]
                print("Dia d'ingres:", dia_ingres)
                print("Dia de sortida:", dia_sortida)
                print("Id de l'operació:", id_operacio)
                print("Nom del pacient:", nom_pacient)
                print("Id del metge:", id_medic)
                print("Id de la infermeria:", id_infermeria)
            else:
                print("Nom de quirofan no existeix")
            
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
           SELECT EXTRACT(HOUR FROM v.data_hora) AS hora, 
                  EXTRACT(MINUTE FROM v.data_hora) AS minut,
                  pe.nom AS metge, 
                  p.nom AS pacient
            FROM visita v
            INNER JOIN pacient p ON p.id_pacient = v.id_pacient
            INNER JOIN personal_medic pm ON pm.id_visita = v.id_visita
            INNER JOIN personal pe ON pe.id_personal = pm.id_personal
            WHERE DATE(v.data_hora) = %s
            """
            cursor.execute(consulta, (dia_visita,))
            resultats = cursor.fetchall()
            
            if resultats:
                print("-" * 65)
                print("| Data        | Hora  |   Nom del Metge   |   Nom del Pacient   |")
                print("|-------------|-------|-------------------|---------------------|")
                for resultat in resultats:
                    hora = resultat[0]
                    minut = resultat[1]
                    nom_metge = resultat[2]
                    nom_pacient = resultat[3]
                    print("| 2024-04-18  | {:>2}:{:<2} | {:^17} | {:^19} |".format(hora, minut, nom_metge, nom_pacient))
                    print("|-------------|-------|-------------------|---------------------|")
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
            SELECT p.nom, r.dia_ingres, r.dia_sortida
                FROM reserva r
                INNER JOIN habitacio h ON h.id_reserva = r.id_reserva
                INNER JOIN pacient p ON p.id_reserva = r.id_reserva
            WHERE h.num_habitacio =  %s
            """
            cursor.execute(consulta, (id_habitacio,))
            resultat = cursor.fetchone()
            
            if resultat:
                nom_pacient = resultat[0]
                dia_ingres = resultat[1]
                dia_sortida = resultat[2]
                print("Nom del pacient:", nom_pacient)
                print("Dia d'ingres:", dia_ingres)
                print("Dia de sortida:", dia_sortida)
            else:
                print("No s'han trobat visites per a la data especificada.")
            
            cursor.close()
            connexio.close()
        except psycopg2.Error as e:
            print("Error al executar la consulta:", e)
    else:
        print("No s'ha pogut connectar a la base de dades.")

def informacio_pacient(id_pacient):
    connexio = conectar_postgresql("postgres","12345")
    if connexio is not None:
        try:
            cursor = connexio.cursor()
            consulta = """
            SELECT  v.diagnostic, m.nom
                FROM visita v 
                INNER JOIN pacient p ON p.id_pacient = v.id_pacient
                INNER JOIN visita_medicament vm ON vm.id_visita = v.id_visita
                INNER JOIN medicament m ON m.id_medicament = vm.id_medicament
            WHERE p.id_pacient =  %s
            """
            cursor.execute(consulta, (id_pacient,))
            resultats = cursor.fetchall()
            visites_pacient = cursor.rowcount
            
            if resultats:
                print("Numero de visites:", visites_pacient)
                for resultat in resultats:
                    diagnostic = resultat[0]
                    nom_medicament = resultat[1]
                    print("Diagnostic del pacient:", diagnostic)
                    print("Nom del medicament:", nom_medicament)
            else:
                print("No s'han trobat visites per a la data especificada.")
            
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

def mostrar_menu_manteniments():
    print("-" * 92)
    print(" " * 28 + "Menú Manteniments")
    print("-" * 92)
    print("1.  Obtenir dependencia enfermeria")
    print("2.  Informació del quirofan")
    print("3.  Informació de les visites")
    print("4.  Informació reserves per habitació")
    print("5.  Informació del pacient")
    print("6.  Informació equip de tots els quirofans")
    print("0.  Tornar al menú principal")
    print("-" * 92)

def mostrar_menu():
    while True:
        print("-" * 92)
        print(" " * 33 + "Menú Login")
        print("-" * 92)
        print("1. Iniciar sessió")
        print("2. Registrar usuari")
        print("0. Sortir")
        numero = input("Introdueix una opció: ")

        if numero == "1":
            usuari = input("Introdueix el teu usuari: ")
            contrasenya = input("Introdueix la teva contrasenya: ")
            if iniciar_sesio(usuari, contrasenya):
                while True:
                    mostrar_menu_manteniments()
                    opcio_mantenimient = input("Introdueix una opció: ")
                    if opcio_mantenimient == "1":
                        print("-" * 92)
                        print(" " * 26 + "Informació Dependencia Enfermeria")
                        print("-" * 92)
                        id_infermeria = input("Introdueix l'ID de la infermeria: ")
                        obtenir_dependencia_enfermeria(id_infermeria)
                        input("Prem Enter per continuar...")
                    elif opcio_mantenimient == "2":
                        print("Informació del quirofan")
                        nom_quirofan = input("Introdueix el nom del quirofan: ")
                        info_quirofan(nom_quirofan)
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
                    elif opcio_mantenimient == "0":
                        # Volver al menú principal
                        print("Tornant al menú principal...")
                        break
                    else:
                        print("Opció invàlida. Si us plau, selecciona una opció vàlida.")
                                    
            else:
                print("Usuari o contrasenya incorrectes.")
        elif numero == "2":
            print("Selecciona el teu rol:")
            print("1.- Manteniment")
            print("2.- Infermers")
            print("3.- Personal Medic")
            print("4.- Administratius")
            print("5.- Pacients")
            role = input("Introdueix el número corresponent al rol: ")
            roles = ["manteniment", "infermers", "personal_medic", "administratius", "pacients"]
            if role.isdigit() and 1 <= int(role) <= len(roles):
                    role = roles[int(role) - 1]
                    usuari = input("Introdueix el teu nou usuari: ")
                    contrasenya = input("Introdueix la teva nova contrasenya: ")
                    crearUsuari(usuari, contrasenya, role)
            else:
                print("Opció invàlida. Si us plau, selecciona una opció vàlida.")
        elif numero == "0":
            print("Sortint del programa...")
            break
        else:
            print("Opció invàlida. Si us plau, selecciona una opció vàlida.")
    
    
    
    
