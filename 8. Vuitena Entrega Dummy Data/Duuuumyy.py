import csv
import datetime
import faker
import random

from cryptography.fernet import Fernet
from faker import Faker
import psycopg2
from psycopg2 import Error

medicamentos = ['paracetamol', 'ibuprofeno', 'amoxicilina', 'dalsy', 'apiretal', 'nolotil', 'voltaren', 'aspirina', 'loratadina', 'diazepam']
especil = ['cirurgia', 'pediatria', 'urologia', 'oftalmologia', 'traumatologia', 'dermatologia', 'neurologia', 'cardiologia', 'ginecologia', 'oncologia']
curru = ['Experiencia en cirurgia', 'Experiencia en pediatria', 'Experiencia en urologia', 'Experiencia en oftalmologia', 'Experiencia en traumatologia', 'Experiencia en dermatologia', 'Experiencia en neurologia', 'Experiencia en cardiologia', 'Experiencia en ginecologia', 'Experiencia en oncologia']
estud = ['Lliçenciat en Infermeria', 'Lliçenciat en Medicina', 'Lliçenciat en Psicologia', 'Lliçenciat en Fisioterapia', 'Lliçenciat en dermatologia', 'Lliçenciat en neurologia', 'Lliçenciat en cardiologia', 'Lliçenciat en ginecologia', 'Lliçenciat en oncologia']
diagnostics_comuns = ['grip', 'fractura', 'infeccio', 'cancer', 'diabetis', 'alergia', 'asma', 'anemia', 'artritis', 'bronquitis']
estud_infermeria = ['Grau en pediatria', 'Grau en urologia', 'Grau en oftalmologia', 'Grau en traumatologia', 'Grau en dermatologia', 'Grau en neurologia', 'Grau en cardiologia', 'Grau en ginecologia', 'Grau en oncologia']
especil_infermeria = ['Cirurgia', 'Traumatologia', 'Dermatologia', 'Neurologia', 'Cardiologia', 'Ginecologia', 'Oncologia']
curru__infermeria = ['Experiencia en pediatria', 'Experiencia en urologia', 'Experiencia en oftalmologia', 'Experiencia en traumatologia', 'Experiencia en dermatologia', 'Experiencia en neurologia', 'Experiencia en cardiologia', 'Experiencia en ginecologia', 'Experiencia en oncologia']
nom_aparell = ['Desfibril·lador', 'Monitor de signes vitals', 'Electrocardiograma', 'Raigs X', 'Tomografia computada', 'Ressonància magnètica', 'Ecògraf (ultrasons)', 'Endoscopi', 'Ventilador mecànic', "Màquina anestèsia"]

def carregar_clau():
    with open("clau.key", "rb") as archivo_clau:
        clau = archivo_clau.read()
    return clau

def generar_clau():
    clave = Fernet.generate_key()
    with open("clau.key", "wb") as archivo_clau:
        archivo_clau.write(clave)


def xifrar_dada(dada, clau):
    fernet = Fernet(clau)
    dada_xifrada = fernet.encrypt(dada.encode())
    return dada_xifrada.decode()

def desxifrar_dada(dada_xifrada, clau):
    fernet = Fernet(clau)
    dada_desxifrada = fernet.decrypt(dada_xifrada.encode()).decode()
    return dada_desxifrada

def conectar_postgresql(usuari:str, contrasenya:str):
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

def crearUsuari(usuari:str, contrasenya:str, role:str):
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
        if usuari == usuari_desxifrat:
            print("L'usuari ja existeix.")
            existeix = True 

    if not existeix:
        nou_usuari = {'Usuari': usuari_cifrat, 'Contrasenya': contrasenya_cifrada} 
        fitxer.append(nou_usuari)
        
        with open("usuaris.csv", 'w', newline='') as f:
            capcalera = ['Usuari', 'Contrasenya'] 
            writer = csv.DictWriter(f, fieldnames=capcalera, delimiter=';')
            writer.writeheader()
            writer.writerows(fitxer)
            
        connexio = conectar_postgresql("postgres", "12345")
        if connexio is not None:
            cursor = connexio.cursor()
            cursor.execute(f"CREATE ROLE {usuari} LOGIN PASSWORD '{contrasenya}'")
            connexio.commit()
            
            cursor.execute(f"ALTER GROUP {role} ADD USER {usuari}")
            connexio.commit()
            cursor.close()
            connexio.close()
        print("Usuari creat correctament.")    



connection = psycopg2.connect(user="postgres",
                                      password="P@ssw0rd",
                                      host="192.168.56.107",
                                      port="5432",
                                      dbname="hospital")
fake = Faker()
cursor = connection.cursor()
fake = faker.Faker("es_ES")
fake2 = faker.Faker("ru_RU")
vari = ['administratiu', 'neteja']


for personal in range(0,1000):
    nom1 = fake.first_name()
    nom2 = fake2.first_name()
    nom = random.choice([nom1, nom2])
    apellido1 = fake.last_name()
    apellido2 = fake2.last_name()
    apellido = apellido1 if nom == nom1 else apellido2
    dni_numeros = random.randint(10000000, 99999999)
    dni_letra = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    dni = f"{dni_numeros}{dni_letra}"
    cursor.execute(f"INSERT INTO personal (nom, cognom, dni) VALUES ('{nom}', '{apellido}', '{dni}')")
    connection.commit()


for pacient in range(0,60000):
    nom = fake.first_name()
    apellido = fake.last_name()
    cursor.execute(f"INSERT INTO pacient (nom, cognom) VALUES ('{nom}', '{apellido}')")
    connection.commit()


for personal_vari in range(0,500):
    tipus_feina = random.choice(vari)
    id_personal = personal_vari+1
    cursor.execute(f"INSERT INTO personal_vari (tipus_de_feina, id_personal) VALUES ('{tipus_feina}' , {id_personal})")
    connection.commit() 


for plantes in range(1,6):
    cursor.execute(f"INSERT INTO planta (num_plantes) VALUES ({plantes})")
    connection.commit()


for quirofans in range(1, 5):
    nombre_quirofan = f"Q{100 + quirofans}"
    num_plantes = random.randint(1, 5)
    cursor.execute(f"INSERT INTO quirofan (nom_quirofan, num_plantes) VALUES ('{nombre_quirofan}', {num_plantes})")
    connection.commit() 


for medicame in (medicamentos):
    nombre = random.choice(medicamentos)
    cursor.execute(f"INSERT INTO medicament (nom) VALUES ('{nombre}')")
    connection.commit()


for habitacions in range (101):
    num_plantes = random.randint(1, 5)
    cursor.execute(f"INSERT INTO habitacio (num_plantes) VALUES ({num_plantes})")
    connection.commit()


for resr in range (101):
    dia_ingres = fake.date_time_between(start_date='-1y', end_date='now')
    dia_sortida = fake.date_time_between(start_date=dia_ingres, end_date=dia_ingres + datetime.timedelta(days=7))
    nombre_quirofan = f"Q{100 + random.randint(1, 4)}"
    cursor.execute(f"INSERT INTO reserva (dia_ingres, dia_sortida, nom_quirofan) VALUES ('{dia_ingres}', '{dia_sortida}', '{nombre_quirofan}')")
    connection.commit()


for pers_medic in range(0, 200):
    especialitat = random.choice(especil)
    curriculum = random.choice(curru)
    estudis = random.choice(estud)
    id_personal = pers_medic+1
    cursor.execute(f"INSERT INTO personal_medic (especialitat, curriculum, estudis, id_personal) VALUES ('{especialitat}', '{curriculum}', '{estudis}' , {id_personal})")
    connection.commit()


for visit in range(0, 100100):
    data_hora = fake.date_time_between(start_date='-1y', end_date='now')
    diagnostic = random.choice(diagnostics_comuns)
    id_pacient = random.randint(1,5000)
    id_medic = random.randint(1,200)
    cursor.execute(f"INSERT INTO visita (data_hora, diagnostic, id_pacient , id_medic) VALUES ('{data_hora}', '{diagnostic}', {id_pacient}, {id_medic})")
    connection.commit()


for operacio in range(0,101):
    id_pacient = operacio+1
    id_medic = operacio+1
    id_reserva = operacio+1
    cursor.execute(f"INSERT INTO operacio (id_pacient, id_medic, id_reserva) VALUES ({id_pacient}, {id_medic}, {id_reserva})")
    connection.commit()


for personal_infermeria in range (0, 300):
    estudis_infermeria = random.choice(estud_infermeria)
    especialitat_infermeria = random.choice(especil_infermeria)
    curriculum_infermeria = random.choice(curru__infermeria)
    id_personal = personal_infermeria+1
    plantamedic = random.randint(0, 1)
    if plantamedic == 0:
        id_medic = random.randint(1, 200)
        cursor.execute(f"INSERT INTO personal_infermeria (estudis, especialitat, curriculum, id_personal , id_medic ) VALUES ('{estudis_infermeria}', '{especialitat_infermeria}', '{curriculum_infermeria}' , {id_personal}, {id_medic})")
    else:
        num_plantes = random.randint(1, 5)
        cursor.execute(f"INSERT INTO personal_infermeria (estudis, especialitat, curriculum, id_personal , num_plantes ) VALUES ('{estudis_infermeria}', '{especialitat_infermeria}', '{curriculum_infermeria}' , {id_personal}, {num_plantes})")
    connection.commit()


for aparell_medic in range (0, 101):
    tipus_de_aparell = random.choice(nom_aparell)
    cursor.execute(f"INSERT INTO aparell_medic (tipus_de_aparell) VALUES ('{tipus_de_aparell}')")
    connection.commit()


for quirofan_aparell_medic in range (0, 101):
    quantitat = random.randint(1, 10)
    nombre_quirofan = f"Q{100 + random.randint(1, 4)}"
    id_aparell_medic = quirofan_aparell_medic+1
    cursor.execute(f"INSERT INTO quirofan_aparell_medic (quantitat, nom_quirofan, id_aparell_medic) VALUES ({quantitat}, '{nombre_quirofan}', {id_aparell_medic})")
    connection.commit()

for visita_medicament in range (0, 10):
    id_visita = visita_medicament+1
    id_medicament = visita_medicament+1
    cursor.execute(f"INSERT INTO visita_medicament (id_visita, id_medicament) VALUES ({id_visita}, {id_medicament})")
    connection.commit()


for pacient_ingressat in range (0, 101):
    dia_ingres = fake.date_time_between(start_date='-1y', end_date='now')
    dia_sortida = fake.date_time_between(start_date=dia_ingres, end_date=dia_ingres + datetime.timedelta(days=7))
    id_pacient = pacient_ingressat+1
    num_habitacio = pacient_ingressat+1
    cursor.execute(f"INSERT INTO pacient_ingressat (dia_ingres, dia_sortida, id_pacient, num_habitacio) VALUES ('{dia_ingres}', '{dia_sortida}', {id_pacient}, {num_habitacio})")
    connection.commit()