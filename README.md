# PruebaOsa — Automatización de Recaudo, Visibilidad y Proyección de Cartera

Prueba técnica que automatiza el proceso de cartera B2B: los clientes consultan su
estado de cuenta en línea, el analista recibe un tablero de gestión y se envían
recordatorios de facturas por correo con su estado de cuenta en PDF.

## Estructura del repositorio

```
├── backend/                  # API y lógica (Django + Django REST Ninja)
│   ├── Cliente/              # Clientes y portal del cliente (estado de cuenta)
│   ├── Factura/              # Modelo y CRUD de facturas
│   ├── Recaudo/              # Abonos / recaudos
│   ├── Usuario/              # Usuarios del sistema y login del analista
│   ├── Dashboard/            # Resumen para el analista
│   ├── Notificaciones/       # Envío de correos con el PDF adjunto
│   │   └── management/commands/
│   │       ├── seed_demo.py          # Carga datos de ejemplo
│   │       └── enviar_recordatorio.py # Envía recordatorios por correo
│   └── PruebaOsa/            # Configuración del proyecto Django
├── frontend/                 # Cliente web (Angular)
│   └── src/app/
│       ├── dashboard/        # Tablero del analista
│       ├── login/            # Login del analista
│       └── estado-cuenta/    # Portal del cliente
└── Prueba Tecnica Líder de Tecnología.pdf  # Enunciado de la prueba
```

## Tecnologías

- **Backend:** Python 3.14, Django 6.1, Django Ninja, ReportLab
- **Frontend:** Angular 22, TypeScript, Vitest
- **Base de datos:** SQLite (`backend/db.sqlite3`)

## Puesta en marcha

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt   # o: pip install django django-cors-headers django-ninja reportlab
python manage.py migrate
python manage.py seed_demo        # carga 5 clientes, 5 facturas y el usuario analista
python manage.py runserver        # API en http://localhost:8000
```

Documentación interactiva de la API (Swagger Django Ninja): `http://localhost:8000/api/docs`

### Frontend

```bash
cd frontend
npm install
npm start                        # aplicación en http://localhost:4200
```

## Accesos de prueba (después de `seed_demo`)

- **Analista:** `analista@pruebaosa.com` / `admin123` — login en `/login`
- **Portal cliente:** se imprime una URL por cliente con su token, por ejemplo
  `http://localhost:4200/estado-cuenta/<token>` (pide el NIT del cliente).

## Envío de correos

Por defecto los correos se "envían" a consola (`console.EmailBackend`). Para envío real
por Gmail SMTP, definí las variables de entorno al ejecutar el comando:

```bash
cd backend
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend \
EMAIL_HOST=smtp.gmail.com \
EMAIL_PORT=587 \
EMAIL_HOST_USER=andreygonzalez9726@gmail.com \
EMAIL_HOST_PASSWORD='<contraseña de aplicación>' \
python manage.py enviar_recordatorio
```

Cada correo incluye el **estado de cuenta en PDF** (`estado-cuenta.pdf`) con las
facturas pendientes del cliente.

>  Usá una [contraseña de aplicación de Google](https://myaccount.google.com/apppasswords);
> nunca guardes la contraseña en el repositorio. La plantilla de configuración está en
> `backend/PruebaOsa/settings.py` bajo las variables `EMAIL_*`.

## API

Base: `http://localhost:8000/api`

| Método | Ruta | Descripción |
| ------ | ---- | ----------- |
| POST | `/usuario/login` | Login del analista |
| GET | `/usuario/usuarios` | Listar usuarios |
| GET | `/dashboard/resumen` | Resumen de cartera para el analista |
| GET | `/cliente/clientes` | Listar clientes |
| POST | `/cliente/cliente` | Crear cliente |
| PUT | `/cliente/clientes/{cliente_id}` | Actualizar cliente |
| DELETE | `/cliente/cliente/{cliente_id}` | Eliminar cliente |
| GET | `/factura/facturas` | Listar facturas |
| POST | `/factura/factura` | Crear factura |
| PUT | `/factura/factura/{factura_id}` | Actualizar factura |
| DELETE | `/factura/factura/{factura_id}` | Eliminar factura |
| GET | `/recaudo/recaudos` | Listar recaudos |
| POST | `/recaudo/recaudo` | Crear recaudo |
| PUT | `/recaudo/recaudo/{recaudo_id}` | Actualizar recaudo |
| DELETE | `/recaudo/recaudo/{recaudo_id}` | Eliminar recaudo |
| POST | `/portal-cliente/estado-cuenta/{token}` | Consultar estado de cuenta del cliente (body: `{"nit": "..."}`) |

## Comandos útiles

```bash
# Reiniciar la base de datos desde cero
python manage.py flush
python manage.py seed_demo

# Enviar recordatorios solo a consola (sin SMTP)
python manage.py enviar_recordatorio
```