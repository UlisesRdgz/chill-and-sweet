# Proyecto Django "Chill & Sweet"

## Descripción de la App
Chill & Sweet es una plataforma de pedidos que permite a los clientes personalizar postres a su gusto de manera intuitiva y segura, brindando una experiencia fluida para seleccionar ingredientes, estilos y tamaños, y ofreciendo postres predefinidos para quienes prefieran opciones ya probadas. Diseñada para optimizar el proceso de pedido en el local, los usuarios pueden hacer pedidos desde una terminal física o mediante la app en el celular, eligiendo un horario para recoger el pedido o consumirlo en el lugar, garantizando así rapidez y practicidad sin necesidad de atención personalizada.

## Autores
- **Zurisadai Uribe García** 
- **Ulises Rodríguez García**
- **David Jonathan Lázaro Pérez**
- **David Pérez Jacome** 
- **Alexys Gómez Elizalde** 

## Instalación
Sigue estos pasos para clonar el repositorio e instalar las dependencias necesarias:

1. Clona el repositorio:
   ```bash
   git clone https://github.com/usuario/chill-and-sweet.git
   cd chill-and-sweet
   ```

2. Crea un entorno virtual:
   ```bash
   python3 -m venv env
   ```

3. Activa el entorno virtual:
   - **En Windows**:
     ```bash
     .\env\Scripts\activate
     ```
   - **En macOS/Linux**:
     ```bash
     source env/bin/activate
     ```

4. Instala las dependencias desde `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución
Sigue estos pasos para ejecutar el proyecto localmente:

1. Realiza las migraciones de la base de datos:
   ```bash
   python manage.py migrate
   ```

2. Inicia el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```

3. Accede a la app en tu navegador en `http://127.0.0.1:8000/`.

## Notas Adicionales
- Asegúrate de tener Python 3.7 o superior.
  
## Licencia
Este proyecto está bajo la licencia [Nombre de la Licencia].

