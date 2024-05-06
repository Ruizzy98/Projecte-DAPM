# <p align="center">  Backups local, i amb OneDrive </p>

Backup Local
-------------
Primer de tot haurem de crear la ruta en local, fet això creem el següent script, per tal de fer les copies i comprimirles
<br>
![imatge1](Imatges/Backup1.jpg)<br>
<br>
Fet el script, configurem el crontab per tal de que faci les copies segons demana el enunciat
<br>
![imatge2](Imatges/Backup2.jpg)<br>
<br>
Per útlim haurem de crear un script per tal de restaurar les copies en local
![imatge3](Imatges/Backup3.jpg)<br>
<br>

Backup OneDrive
---------------
Una vegada feta les copies en local, pasem a fer-les en el nuvol. Per fer-ho en el meu cas ho sincronitza amb el OneDrive. <br>
<br>
Primer de tot creem un script com el següent:
<br>
![imatge4](Imatges/Backup4.jpg)<br>
<br>
Ahora haurem de seguir les següents comandes:
```
sudo apt install onedrive
```
Fet aixo haurem de donar-li permisos al script, i executarlo
![imatge5](Imatges/Backup5.jpg)<br>
Ara reiniciem el servidor, i seguim les comandes:
![imatge5](Imatges/Backup5.1.jpg)<br>
Ara executem la següent comanda
```
sudo apt install --no-install-recomends --no-install-suggests onedrive
```
![imatge5](Imatges/Backup5.2.jpg)<br>
