# inventory_management – Backend para Empresas, Productos e Inventario

Este proyecto es una API REST desarrollada con **Django**, **Django REST Framework** y **PostgreSQL**, orientada a la gestión de empresas, productos e inventario. Incorpora autenticación basada en JWT, estructura modular limpia, roles de usuario (Administrador y Externo) y exportación de inventario en PDF. El sistema está preparado para extenderse con módulos de **IA**, **Blockchain** u otras tecnologías emergentes.

> [!IMPORTANT]
> Este backend funciona junto con un frontend desarrollado en React y TypeScript, siguiendo los principios de Atomic Design y Arquitectura Limpia. Incluye un flujo de autenticación seguro, estructura modular e integración en tiempo real entre la API y la interfaz de usuario.


---

## 🚀 Funcionalidades Principales

1. **Gestión de Empresas**
   - Formulario para registrar empresas.

2. **Gestión de Productos**
   - Formulario para registrar productos.

3. **Autenticación y Seguridad**
   - Inicio de sesión con email y contraseña.
   - Contraseña encriptada mediante el sistema de autenticación de Django.
   - Autenticación mediante JWT (`rest_framework_simplejwt`).
   - Roles:
     - `Administrador`: puede crear, editar, eliminar empresas y productos.
     - `Externo`: solo puede visualizar.

4. **Inventario**
   - Permite exportar a PDF los productos registrados.

5. **Extensibilidad con IA y Blockchain**
   - Arquitectura preparada para incluir funcionalidades innovadoras en IA, Blockchain.

6. **Documentación API**
   - Swagger/OpenAPI con `drf-spectacular`.

7. **Estructura modular y limpia**
   - Separación por `apps`, capas de `services`, `use_cases`, `serializers`, `permissions`, etc.

---

## 🛠️ Instalación y configuración

### Pre-requisitos

- Python 3.11
- PostgreSQL
- Git

### Variables de entorno `.env`

Crea un archivo `.env` con las siguientes variables:

```dotenv
SECRET_KEY=tu_clave_secreta
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=inventory_db
DB_USER=inventory_user
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432
```
### Instalación paso a paso

```dotenv
# Clona el repositorio
git clone https://github.com/inesmariao/inventory_management.git
cd inventory_management

# Crea entorno virtual
python -m venv venv_inventory
.\venv_inventory\Scripts\activate   # En Windows

# Instala dependencias
pip install -r requirements.txt

# Migraciones y superusuario
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# Carga los datos geográficos de países, departamentos y municipios
python manage.py import_countries
python manage.py import_departments
python manage.py import_municipalities

# Corre el servidor
python manage.py runserver
```

> [!TIP]
>Puedes crear nuevos módulos reutilizables en la carpeta apps/ manteniendo el enfoque modular por responsabilidad.

**📄 Contribuciones**
> [!NOTE]
>Si quieres aportar ideas o código, puedes escribirme a inesmaoh@gmail.com para sumarte como colaborador. Por favor sigue buenas prácticas y realiza tus Pull Requests en ramas específicas.

> [!TIP]
>¡Si este proyecto te parece útil o interesante, considera dejarme una estrella en el repositorio! ⭐


## Desarrollado por:
* Ing. Inés María Oliveros Hernández

## 📜 Licencia
Este proyecto está licenciado bajo la Licencia ISC. Consulta el archivo LICENSE para más detalles.

>[!IMPORTANT]
>Copyright 2025. Ing. Inés María Oliveros

Por la presente se concede permiso para utilizar, copiar, modificar y/o distribuir este software para cualquier fin, con o sin cargo, siempre que el aviso de copyright anterior y este aviso de permiso aparezcan en todas las copias.

EL SOFTWARE SE PROPORCIONA "TAL CUAL" Y EL AUTOR RECHAZA TODA GARANTÍA CON RESPECTO A ESTE SOFTWARE, INCLUIDAS TODAS LAS GARANTÍAS IMPLÍCITAS DE COMERCIABILIDAD E IDONEIDAD. EN NINGÚN CASO EL AUTOR SERÁ RESPONSABLE DE NINGÚN DAÑO ESPECIAL, DIRECTO, INDIRECTO O CONSECUENTE, NI DE NINGÚN DAÑO DERIVADO DE LA PÉRDIDA DE USO, DATOS O BENEFICIOS, YA SEA EN UNA ACCIÓN CONTRACTUAL, NEGLIGENCIA U OTRA ACCIÓN ILÍCITA, QUE SURJA DE O EN RELACIÓN CON EL USO O RENDIMIENTO DE ESTE SOFTWARE.

**License**
>[!IMPORTANT]
>Copyright 2025. Ing. Inés María Oliveros Hernández

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED “AS IS” AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.