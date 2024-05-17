import csv
import datetime
import faker
import random

from cryptography.fernet import Fernet
from faker import Faker
import psycopg2
from psycopg2 import Error


def conectar_postgresql(usuari:str, contrasenya:str):
    try:
        connexio = psycopg2.connect(user=usuari,
                                      password=contrasenya,
                                      host="192.168.56.107",
                                      port="5432",
                                      dbname="hospital")
        return connexio
    except (Exception, Error) as error:
        print("Error al conectar a Hospital:", error)
        return None

def generar_dades():
    medicamentos = ['paracetamol', 'ibuprofeno', 'amoxicilina', 'dalsy', 'apiretal', 'nolotil', 'voltaren', 'aspirina', 'loratadina', 'diazepam']
    especil = ['cirurgia', 'pediatria', 'urologia', 'oftalmologia', 'traumatologia', 'dermatologia', 'neurologia', 'cardiologia', 'ginecologia', 'oncologia']
    curru = ['Experiencia en cirurgia', 'Experiencia en pediatria', 'Experiencia en urologia', 'Experiencia en oftalmologia', 'Experiencia en traumatologia', 'Experiencia en dermatologia', 'Experiencia en neurologia', 'Experiencia en cardiologia', 'Experiencia en ginecologia', 'Experiencia en oncologia']
    estud = ['Lliçenciat en Infermeria', 'Lliçenciat en Medicina', 'Lliçenciat en Psicologia', 'Lliçenciat en Fisioterapia', 'Lliçenciat en dermatologia', 'Lliçenciat en neurologia', 'Lliçenciat en cardiologia', 'Lliçenciat en ginecologia', 'Lliçenciat en oncologia']
    diagnostics_comuns = ['grip', 'fractura', 'infeccio', 'cancer', 'diabetis', 'alergia', 'asma', 'anemia', 'artritis', 'bronquitis']
    estud_infermeria = ['Grau en pediatria', 'Grau en urologia', 'Grau en oftalmologia', 'Grau en traumatologia', 'Grau en dermatologia', 'Grau en neurologia', 'Grau en cardiologia', 'Grau en ginecologia', 'Grau en oncologia']
    especil_infermeria = ['Cirurgia', 'Traumatologia', 'Dermatologia', 'Neurologia', 'Cardiologia', 'Ginecologia', 'Oncologia']
    curru__infermeria = ['Experiencia en pediatria', 'Experiencia en urologia', 'Experiencia en oftalmologia', 'Experiencia en traumatologia', 'Experiencia en dermatologia', 'Experiencia en neurologia', 'Experiencia en cardiologia', 'Experiencia en ginecologia', 'Experiencia en oncologia']
    nom_aparell = ['Desfibril·lador', 'Monitor de signes vitals', 'Electrocardiograma', 'Raigs X', 'Tomografia computada', 'Ressonància magnètica', 'Ecògraf (ultrasons)', 'Endoscopi', 'Ventilador mecànic', "Màquina anestèsia"]

    connexio = conectar_postgresql("postgres", "12345")
    fake = Faker()
    cursor = connexio.cursor()
    fake = faker.Faker("es_ES")
    fake2 = faker.Faker("ru_RU")

    print("Generar dades personal...")
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
        connexio.commit()

    print("Generar dades pacients...")
    for pacient in range(0,55000):
        nom = fake.first_name()
        apellido = fake.last_name()
        cursor.execute(f"INSERT INTO pacient (nom, cognom) VALUES ('{nom}', '{apellido}')")
        connexio.commit()

    print("Generar dades personal vari...")
    neteja_count = 0
    administratiu_count = 0
    for personal_vari in range(1, 201):
        if neteja_count < 100:
            tipus_feina = 'neteja'
            neteja_count += 1
        elif administratiu_count < 100:
            tipus_feina = 'administratiu'
            administratiu_count += 1
        cursor.execute(f"INSERT INTO personal_vari (tipus_de_feina, id_personal) VALUES ('{tipus_feina}', {personal_vari})")
        connexio.commit()       

    print("Generar dades plantes...")
    for plantes in range(1,6):
        cursor.execute(f"INSERT INTO planta (num_plantes) VALUES ({plantes})")
        connexio.commit()

    print("Generar dades quirofans...")
    for quirofans in range(1, 10):
        nombre_quirofan = f"Q{100 + quirofans}"
        num_plantes = random.randint(1, 5)
        cursor.execute(f"INSERT INTO quirofan (nom_quirofan, num_plantes) VALUES ('{nombre_quirofan}', {num_plantes})")
        connexio.commit() 

    print("Generar dades medicaments...")
    for medicament in (medicamentos):
        nombre = random.choice(medicamentos)
        cursor.execute(f"INSERT INTO medicament (nom) VALUES ('{nombre}')")
        connexio.commit()

    print("Generar dades habitacions...")
    for habitacions in range (101):
        num_plantes = random.randint(1, 5)
        cursor.execute(f"INSERT INTO habitacio (num_plantes) VALUES ({num_plantes})")
        connexio.commit()

    print("Generar dades reserves...")
    for resr in range (101):
        dia_ingres = fake.date_time_between(start_date='-1y', end_date='now')
        dia_sortida = fake.date_time_between(start_date=dia_ingres, end_date=dia_ingres + datetime.timedelta(days=7))
        nombre_quirofan = f"Q{100 + random.randint(1, 4)}"
        cursor.execute(f"INSERT INTO reserva (dia_ingres, dia_sortida, nom_quirofan) VALUES ('{dia_ingres}', '{dia_sortida}', '{nombre_quirofan}')")
        connexio.commit()

    print("Generar dades personal medic...")
    for pers_medic in range(201, 500):
        especialitat = random.choice(especil)
        curriculum = random.choice(curru)
        estudis = random.choice(estud)
        cursor.execute(f"INSERT INTO personal_medic (especialitat, curriculum, estudis, id_personal) VALUES ('{especialitat}', '{curriculum}', '{estudis}' , {pers_medic})")
        connexio.commit()

    print("Generar dades visites...")
    for visit in range(0, 100100):
        data_hora = fake.date_time_between(start_date='-1y', end_date='now')
        diagnostic = random.choice(diagnostics_comuns)
        id_pacient = random.randint(1,50000)
        id_medic = random.randint(1,200)
        cursor.execute(f"INSERT INTO visita (data_hora, diagnostic, id_pacient , id_medic) VALUES ('{data_hora}', '{diagnostic}', {id_pacient}, {id_medic})")
        connexio.commit()

    print("Generar dades operacions...")
    for operacio in range(0,101):
        id_pacient = operacio+1
        id_medic = operacio+1
        id_reserva = operacio+1
        cursor.execute(f"INSERT INTO operacio (id_pacient, id_medic, id_reserva) VALUES ({id_pacient}, {id_medic}, {id_reserva})")
        connexio.commit()

    print("Generar dades personal infermeria...")
    for personal_infermeria in range (501, 1001):
        estudis_infermeria = random.choice(estud_infermeria)
        especialitat_infermeria = random.choice(especil_infermeria)
        curriculum_infermeria = random.choice(curru__infermeria)
        plantamedic = random.randint(0, 1)
        if plantamedic == 0:
            id_medic = random.randint(1, 299)
            cursor.execute(f"INSERT INTO personal_infermeria (estudis, especialitat, curriculum, id_personal , id_medic ) VALUES ('{estudis_infermeria}', '{especialitat_infermeria}', '{curriculum_infermeria}' , {personal_infermeria}, {id_medic})")
        else:
            num_plantes = random.randint(1, 5)
            cursor.execute(f"INSERT INTO personal_infermeria (estudis, especialitat, curriculum, id_personal , num_plantes ) VALUES ('{estudis_infermeria}', '{especialitat_infermeria}', '{curriculum_infermeria}' , {personal_infermeria}, {num_plantes})")
        connexio.commit()

    print("Generar dades aparells medics...")
    for aparell_medic in range (0, 101):
        tipus_de_aparell = random.choice(nom_aparell)
        cursor.execute(f"INSERT INTO aparell_medic (tipus_de_aparell) VALUES ('{tipus_de_aparell}')")
        connexio.commit()

    print("Generar dades quirofan aparell medic...")
    for quirofan_aparell_medic in range (0, 101):
        quantitat = random.randint(1, 10)
        nombre_quirofan = f"Q{100 + random.randint(1, 4)}"
        id_aparell_medic = quirofan_aparell_medic+1
        cursor.execute(f"INSERT INTO quirofan_aparell_medic (quantitat, nom_quirofan, id_aparell_medic) VALUES ({quantitat}, '{nombre_quirofan}', {id_aparell_medic})")
        connexio.commit()

    print("Generar dades visita medicament...")
    for visita_medicament in range (1, 60000):
        id_medicament = random.randint(1, 10)
        cursor.execute(f"INSERT INTO visita_medicament (id_visita, id_medicament) VALUES ({visita_medicament}, {id_medicament})")
        connexio.commit()

    print("Generar dades pacients ingressats...")
    
    for pacient_ingressat in range (0, 101):
        dia_ingres = fake.date_time_between(start_date='-1y', end_date='now')
        dia_sortida = fake.date_time_between(start_date=dia_ingres, end_date=dia_ingres + datetime.timedelta(days=7))
        id_pacient = pacient_ingressat+1
        num_habitacio = pacient_ingressat+1
        cursor.execute(f"INSERT INTO pacient_ingressat (dia_ingres, dia_sortida, id_pacient, num_habitacio) VALUES ('{dia_ingres}', '{dia_sortida}', {id_pacient}, {num_habitacio})")
        connexio.commit()
     
        
def eliminar_dades():
    connexio = conectar_postgresql("postgres", "12345")
    cursor = connexio.cursor()
    print("Eliminant pacients...")
    cursor.execute("DELETE FROM pacient_ingressat")
    cursor.execute("ALTER SEQUENCE pacient_ingressat_id_ingressat_seq RESTART WITH 1")
    connexio.commit()
    print("Eliminant dades visites medicament...")
    cursor.execute("DELETE FROM visita_medicament")
    print("Eliminant dades aparells medicament...")
    cursor.execute("DELETE FROM quirofan_aparell_medic")
    connexio.commit()
    print("Eliminant aparells medics...")
    cursor.execute("DELETE FROM aparell_medic")
    cursor.execute("ALTER SEQUENCE aparell_medic_id_aparell_medic_seq RESTART WITH 1")
    connexio.commit()
    print("Eliminant personal infermeria...") 
    cursor.execute("DELETE FROM personal_infermeria")
    cursor.execute("ALTER SEQUENCE personal_infermeria_id_infermeria_seq RESTART WITH 1")
    connexio.commit()
    print("Eliminant operacions...")
    cursor.execute("DELETE FROM operacio")
    cursor.execute("ALTER SEQUENCE operacio_id_operacio_seq RESTART WITH 1")
    connexio.commit()
    print("Eliminant visites...")
    cursor.execute("DELETE FROM visita")
    cursor.execute("ALTER SEQUENCE visita_id_visita_seq RESTART WITH 1")
    connexio.commit()
    print("Eliminant personal vari...")
    cursor.execute("DELETE FROM personal_medic")
    cursor.execute("ALTER SEQUENCE personal_medic_id_medic_seq RESTART WITH 1")
    connexio.commit()
    print("Eliminant reserves...")
    cursor.execute("DELETE FROM reserva")
    cursor.execute("ALTER SEQUENCE reserva_id_reserva_seq RESTART WITH 1")
    connexio.commit()
    print("Eliminant habitacions...")
    cursor.execute("DELETE FROM habitacio")
    cursor.execute("ALTER SEQUENCE habitacio_num_habitacio_seq RESTART WITH 1")
    connexio.commit()
    print("Eliminant medicaments...")
    cursor.execute("DELETE FROM medicament")
    cursor.execute("ALTER SEQUENCE medicament_id_medicament_seq RESTART WITH 1")
    connexio.commit()
    print("Eliminant quirofans...")
    cursor.execute("DELETE FROM quirofan")
    connexio.commit()
    print("Eliminant plantes...")
    cursor.execute("DELETE FROM planta")
    cursor.execute("ALTER SEQUENCE planta_num_plantes_seq RESTART WITH 1")
    connexio.commit()
    print("Eliminant personal vari...")
    cursor.execute("DELETE FROM personal_vari")
    cursor.execute("ALTER SEQUENCE personal_vari_id_vari_seq RESTART WITH 1")
    connexio.commit()
    print("Eliminant pacients...")
    cursor.execute("DELETE FROM pacient")
    cursor.execute("ALTER SEQUENCE pacient_id_pacient_seq RESTART WITH 1")    
    connexio.commit()
    print("Eliminant personal...")
    cursor.execute("DELETE FROM personal")
    cursor.execute("ALTER SEQUENCE personal_id_personal_seq RESTART WITH 1")
    connexio.commit()
    