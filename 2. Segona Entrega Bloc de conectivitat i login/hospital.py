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
                                      dbname="postgres")
        return connection
    except (Exception, Error) as error:
        print("Error al conectar a PostgreSQL:", error)
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
         
def mostrar_menu():
    print("Inserció exitosa")
    print("-" * 40)
    print("Menú Login")
    print("-" * 40)
    numero = 0
    while numero == 0:
        print("1.- Iniciar sessió")
        print("2.- Registrar usuari")
        print("0.- Sortir")
        numero = input("Introdueix una opció: ")
        if numero == "1":
            usuari = input("Introdueix el teu usuari: ")
            contrasenya = input("Introdueix la teva contrasenya: ")
            if iniciar_sesio(usuari, contrasenya):
                print("Inici de sessió exitós.")
            else:
                print("Usuari o contrasenya incorrectes.")
        elif numero == "2":
            usuari = input("Introdueix el teu nou usuari: ")
            contrasenya = input("Introdueix la teva nova contrasenya: ")
            crearUsuari(usuari, contrasenya)
        else:
            numero=9
            print("Sortint del programa...")

    
    
    
    