# <p align="center">  Backups local, i amb OneDrive </p>

Backup Local
-------------
Primer de tot haurem de crear la ruta en local, fet això creem el següent script, per tal de fer les còpies i comprimir-les.
<br>
![imatge1](Imatges/Backup1.jpg)<br>
<br>
Fet el script, configurem el crontab per tal que faci les còpies segons demana l'enunciat.
<br>
![imatge2](Imatges/Backup2.jpg)<br>
<br>
Finalment, haurem de crear un script per tal de restaurar les còpies en local.
![imatge3](Imatges/Backup3.jpg)<br>
<br>

Backup OneDrive
---------------
Una vegada feta les copies en local, passem a fer-les en el núvol. Per fer-ho en el meu cas ho sincronitza amb el OneDrive. <br>
<br>
Primer de tot creem un script com el següent:
<br>
![imatge4](Imatges/Backup4.jpg)<br>
<br>
Ara haurem de seguir les següents comandes:
```
sudo apt install onedrive
```
Fet això haurem de donar-li permisos al script, i executar-ho.
![imatge5](Imatges/Backup5.jpg)<br>
Ara reiniciem el servidor, i seguim les comandes:
![imatge5](Imatges/Backup5.1.jpg)<br>
Ara executem la següent comanda.
```
sudo apt install --no-install-recomends --no-install-suggests onedrive
```
Després haurem de posar la comanda.
```
onedrive
```
En la línia 3 i 4 després posar la comanda, ens dona un enllaç que haurem de posar al navegador.
![imatge5](Imatges/Backup5.2.jpg)<br>
<br>
Ens ha de sortir això, i iniciem sessió.
![imatge6](Imatges/Backup6.jpg)<br>

Una vegada fet, ens ha de sortir això per acceptar els permisos.
![imatge7](Imatges/Backup7.jpg)<br>
<br>
Ara haurem de tornar a modificar el script del principi, per tal de fer les  còpies i comprimir-les en el OneDrive.
<br>
![imatge8](Imatges/Backup8.jpg)<br>
Quan ja hem modificat el script, ho executem:
![imatge9](Imatges/OneDrive2.jpg)<br>
<br>
Per últim comprovem que en el OneDrive tenim les còpies fetes en local.
![imatge10](Imatges/OneDrive1.jpg)<br>
