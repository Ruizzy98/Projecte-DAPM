Documentacio per exportar les dades
-----------------------------------

Primer de tot haurem d'anar a aquesta web: https://www.postgresql.org/ftp/odbc/versions.old/msi/ i descarregar la versió corresponent  al nostre postgres, en el meu cas descarreguem  el postgresql 15, 

Instal·lar el controlador odbc per postgres que acabin de descarregar. <br>


![Imatge1](Imatges/Imagen1.png)
<br>

Crear la connexió PostgreSQL Unicode(x64)

![Imatge2](Imatges/Imagen2.png)

Cal afegir la connexió de postgres:

![Imatge2](Imatges/Imagen2.png)

Al Power Bi anar a “Obtener datos -> Otras”:

![Imatge3](Imatges/Imagen3.png)

Seleccionar la connexió creada anteriorment:

![Imatge4](Imatges/Imagen4.png)

Afegir les credencials:

![Imatge5](Imatges/Imagen5.png)

Dashboard
---------
Una vegadad ja esta exportada les dades, haurem de crear els grafics, per fer-ho hem anant fent les següents consultes:

```
WITH DiagnosticosPorMes AS (
    SELECT 
        TO_CHAR(data_hora, 'Month') AS Mes,
        diagnostic AS Enfermedad,
        COUNT(*) AS Frecuencia
    FROM 
        VISITA
    WHERE
        EXTRACT(YEAR FROM data_hora) = 2023
    GROUP BY 
        TO_CHAR(data_hora, 'Month'), 
        diagnostic
),
MaxFrecuenciaPorMes AS (
    SELECT
        Mes,
        MAX(Frecuencia) AS MaxFrecuencia
    FROM
        DiagnosticosPorMes
    GROUP BY
        Mes
)
SELECT 
    d.Mes,
    d.Enfermedad,
    d.Frecuencia
FROM 
    DiagnosticosPorMes d
JOIN 
    MaxFrecuenciaPorMes m
ON 
    d.Mes = m.Mes AND d.Frecuencia = m.MaxFrecuencia
ORDER BY 
    CASE
        WHEN d.Mes = 'January' THEN 1
        WHEN d.Mes = 'February' THEN 2
        WHEN d.Mes = 'March' THEN 3
        WHEN d.Mes = 'April' THEN 4
        WHEN d.Mes = 'May' THEN 5
        WHEN d.Mes = 'June' THEN 6
        WHEN d.Mes = 'July' THEN 7
        WHEN d.Mes = 'August' THEN 8
        WHEN d.Mes = 'September' THEN 9
        WHEN d.Mes = 'October' THEN 10
        WHEN d.Mes = 'November' THEN 11
        ELSE 12
    END;
```
![Imatge1](Imatges/1.png)

# Readme
#### [1.Primera Entrega Planificació del projecte ](https://github.com/Ruizzy98/Projecte-DAPM/tree/main/1.%20Primera%20Entrega%20Planificaci%C3%B3%20del%20projecte%20(BD%20%2B%20PRG))
#### [2. Segona Entrega Bloc de conectivitat i login](https://github.com/Ruizzy98/Projecte-DAPM/tree/main/2.%20Segona%20Entrega%20Bloc%20de%20conectivitat%20i%20login)
#### [3. Tercera Entrega Disseny ER-Model Relacional](https://github.com/Ruizzy98/Projecte-DAPM/tree/main/3.%20Tercera%20Entrega%20Disseny%20ER-Model%20Relacional)
#### [4. Quarta Entrega Esquema de seguretat](https://github.com/Ruizzy98/Projecte-DAPM/tree/main/4.%20Quarta%20Entrega%20Esquema%20de%20seguretat)
#### [5. Cinquena Entrega Esquema de seguretat](https://github.com/Ruizzy98/Projecte-DAPM/tree/main/5.%20Cinquena%20Entrega%20Bloc%20de%20manteniment)
#### [6. Sisena Entrega Esquema de seguretat](https://github.com/Ruizzy98/Projecte-DAPM/tree/main/6.%20Sisena%20Entrega%20Esquema%20d'alta%20disponibilitat)
#### [7. Setena Entrega Bloc de consultes](https://github.com/Ruizzy98/Projecte-DAPM/tree/main/7.%20Setena%20Entrega%20Bloc%20de%20consultes)
#### [8. Vuitena Entrega Dummy Data](https://github.com/Ruizzy98/Projecte-DAPM/tree/main/8.%20Vuitena%20Entrega%20Dummy%20Data)
#### [9. Novena entrega Exportació de Dades](https://github.com/Ruizzy98/Projecte-DAPM/tree/main/9.%20Novena%20entrega%20Exportaci%C3%B3%20de%20Dades)
