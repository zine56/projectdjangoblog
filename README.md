# Blog hecho en Django

blog para la clase de coderhouse, hecho con python , django, sqlite, html y javascript

## Uso

para iniciar el servidor local

#bajar proyecto
git clone https://github.com/zine56/projectdjangoblog.git

#entrar a proyecto
cd projectdjangoblog

#instalar dependencias
pip install -r requirements.txt 
#si instalas en windows la unica dependencia que dio problemas fue la pillow, solo pude instalarla usando easy_install Pillow
#crear la bd
python manage.py migrate 


#crear un usuario admin
python manage.py createsuperuser


#correr el servidor local
python manage.py runserver

