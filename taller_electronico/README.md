# Sistema de Gestión para Taller Electrónico (Flask)

Aplicación web MVC para administrar clientes, equipos, órdenes de reparación, diagnósticos, mediciones, inventario, autenticación y generación de código de barras.

## Requisitos
- Python 3.10+
- pip

## Ejecución local paso a paso
1. Entrar al proyecto:
   ```bash
   cd taller_electronico
   ```
2. Crear entorno virtual (opcional):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Inicializar base de datos:
   ```bash
   python init_db.py
   ```
5. Ejecutar servidor:
   ```bash
   python app.py
   ```
6. Abrir en navegador:
   - http://localhost:5000

## Credenciales iniciales
- Usuario: `admin`
- Contraseña: `admin123`

## Funcionalidades nuevas
- Login y cierre de sesión con sesión segura.
- Generador de código de barras Code39 en dashboard.
- Códigos de barra por orden en listado y detalle de orden.
- Rediseño visual (tema moderno, tarjetas, badges, tablas mejoradas y layout responsive).

## Estructura
- `app.py`: punto de entrada, seguridad de rutas y endpoint de código de barras.
- `models/`: acceso a datos y lógica de dominio.
- `routes/`: controladores Flask.
- `templates/`: vistas HTML.
- `static/`: CSS y JS.
- `utils/barcode.py`: generador SVG Code39 sin dependencias externas.

## Escalabilidad futura
- La capa de datos está aislada para migrar a PostgreSQL.
- Arquitectura preparada para notificaciones, WhatsApp e integración móvil.
