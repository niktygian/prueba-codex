# Sistema de Gestión para Taller Electrónico (Flask)

Aplicación web MVC para administrar clientes, equipos, órdenes de reparación, diagnósticos, mediciones, inventario y operación **centrada en código de barras**.

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

## Flujo “todo por código”
1. Crear orden en `Órdenes`.
2. El sistema genera barcode único automático (`ORD-000001`, etc.).
3. Imprimir sticker térmico desde la orden.
4. Pegar sticker en el equipo físico.
5. Para trabajar, escanear en el campo **“Abrir orden”** (sidebar).
6. El sistema abre la orden vinculada al código escaneado.

## Lector de códigos de barras
- Compatible con lectores USB tipo teclado (keyboard wedge).
- Recomendado activar sufijo `ENTER` en el lector para confirmar automáticamente.
- El campo de escaneo queda enfocado para operación rápida.

## Impresora térmica
- Impresión vía navegador en vista de etiqueta (`/ordenes/<id>/label`).
- Formato pensado para 58mm (ajustable a 80mm desde diálogo de impresión).
- Para impresoras térmicas de red/USB, usar el driver del sistema operativo y seleccionar esa impresora al imprimir.

## Funcionalidades principales
- Login y cierre de sesión.
- Dashboard con KPIs del taller.
- Gestión de clientes, equipos, órdenes, diagnósticos y mediciones.
- Inventario y descuento automático de componentes usados.
- Búsqueda por texto y por barcode.
- Generación y uso operativo de barcode por orden.

## Estructura
- `app.py`: punto de entrada, seguridad de rutas y endpoint de barcode SVG.
- `models/`: acceso a datos y lógica de dominio.
- `routes/`: controladores Flask.
- `templates/`: vistas HTML.
- `static/`: CSS y JS.
- `utils/barcode.py`: generador SVG Code39 sin dependencias externas.

## Escalabilidad futura
- La capa de datos está aislada para migrar a PostgreSQL.
- Arquitectura preparada para notificaciones, WhatsApp e integración móvil.


## WhatsApp al cliente
- En el detalle de cada orden hay botón **Enviar WhatsApp al cliente**.
- Genera mensaje prearmado con código de orden, equipo y estado actual.
- Usa `whatsapp` del cliente y, si está vacío, toma `telefono`.
- Abre `wa.me` para que confirmes y envíes desde WhatsApp Web/Desktop.

## Atajos de teclado y numpad
- `Ctrl + K`: foco directo al escáner global (sidebar).
- `Ctrl + N`: foco en formulario de nueva orden.
- `Ctrl + B`: foco en buscador de órdenes.
- En campos de precio/cantidad/valor (`numpad`), `Enter` pasa al siguiente campo numérico.
- Recomendado lector con sufijo `ENTER` para abrir orden apenas escanea.
