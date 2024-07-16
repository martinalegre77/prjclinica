Descarga o clonación del proyecto🤖

Con entorno virtual:

1. Ingresar los siguiente comandos en consola:

   python3 -m venv [nombreDelEntornoVirtual]

- este comando creara un entorno virtual donde se instalaran posteriormente los paquetes.

2. Para activarlo se emplea el siguiente comando:

   source nombreDelEntornoVirtual/bin/activate

- NOTA: en caso de trabajar con Windows, para activar el entorno virtual se ingresa el siguiente comando:

  nombreDelEntornoVirtual\Scripts\activate.bat

3. Para apagarlo (en ambos casos):

  deactivate

  Sin entorno virtual comenzar desde acá:

4. Después correr el siguiente comando para obtener los paquetes empleados en la App:

   pip install -r requirements.txt

5. Clonar el repositorio:

   git clone https://github.com/martinalegre77/prjclinica.git

6. Hacer migraciones:

   python manage.py makemigrations
   python manage.py migrate

7. Arrancar el servidor Django:

   python manage.py runserver

8. Las urls principales del proyecto son:

   http://127.0.0.1:8000/clinica/
   http://127.0.0.1:8000/municipalidad/
   http://127.0.0.1:8000/admin/login/?next=/admin/
   

   



