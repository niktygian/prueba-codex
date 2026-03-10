# Sistema de Gestión para Taller Electrónico (Flask)

Aplicación web MVC para administrar clientes, equipos, órdenes de reparación, diagnósticos, mediciones e inventario.

## Requisitos
- Python 3.10+
- pip

## Ejecución local paso a paso
1. Entrar al proyecto:
   ```bash
   cd taller_electronico
   ```
2. Crear entorno virtual (opcional pero recomendado):
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

## Estructura
- `app.py`: punto de entrada y registro de blueprints.
- `models/`: acceso a datos y lógica de dominio.
- `routes/`: controladores Flask (MVC).
- `templates/`: vistas HTML.
- `static/`: CSS y JS.

## Notas de escalabilidad
- La capa de acceso a datos está aislada en `models/`, facilitando migración a PostgreSQL con cambios mínimos de conexión.
- El proyecto está preparado para extenderse con autenticación, notificaciones e integraciones externas.
