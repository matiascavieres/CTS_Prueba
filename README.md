# Proyecto PRUEBA_CTS
Este proyecto es una aplicación web que combina un backend hecho en Django con un frontend en Vue.js. Utiliza Redis para tareas asíncronas con Celery. A continuación, se detallan los pasos para configurar y ejecutar el proyecto en un entorno de desarrollo local.

### Requisitos
- Python 3.x y pip
- Node.js y npm
- Redis (puedes ejecutarlo en un entorno WSL si estás en Windows)

### Instalación
```
git clone https://github.com/matiascavieres/CTS_Prueba
```

### Crear una maquina virtual
```
python -m venv venv
```
### Activar la máquina virtual y instalar dependencias
```
.\venv\Scripts\activate  # En Windows
source venv/bin/activate  # En MacOS/Linux

```

### Instalar dependencias para el backend:
```
pip install -r requirements.txt
```
# Ejecución del Proyecto
## Backend (Django)
Desde el directorio raíz del proyecto, ejecuta el backend de Django:
```
cd backend
python manage.py runserver
```
## Frontend (Vue)
Abre una nueva terminal y dirígete a la carpeta frontend:
```
cd frontend
npm install  # Ejecuta esto solo la primera vez para instalar dependencias
npm run serve
```

## Redis
En un entorno WSL o terminal compatible con Redis, ejecuta el servidor Redis:
```
redis-server
```

## Tareas Asíncronas (Celery)
Abre una nueva terminal y dirígete al directorio backend para ejecutar el worker de Celery:
```
cd backend
celery -A backend worker --pool=solo --loglevel=info
```
# Acceso al Superusuario
Para administrar el proyecto, puedes utilizar el siguiente superusuario predeterminado (o crear uno nuevo si prefieres):

- Usuario: CTS_Admin
- Contraseña: 1234
Si necesitas crear un superusuario, puedes hacerlo con el siguiente comando:

```
python manage.py createsuperuser
```

# Notas Adicionales

- Backend: Accede al backend en http://localhost:8000.
- Frontend: Accede al frontend en http://localhost:8080.
- Redis se utiliza para manejar tareas asíncronas con Celery.
- Celery se ejecuta como worker para gestionar las tareas de fondo definidas en el backend.

Autor: Matias Cavieres