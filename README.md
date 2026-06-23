# MY-SUPERIOR (reconstruida)

Versión reconstruida de la app con enfoque visual y emocional: rosa pastel, saludo personalizado ("Hola Maye 💖"), módulo Familia con tarjetas humanas, coach emocional y la mini-mascota "Morar".

Cómo ejecutar

1. Instala dependencias:

```bash
pip install -r requirements.txt
```

2. Ejecuta:

```bash
chmod +x streamlit_app.sh
PORT=8501 ./streamlit_app.sh
```

La app no crea bases de datos por defecto; el estado se mantiene en memoria para esta versión inicial.
# 🛍️ Inventory tracker template

A Streamlit app showing how to use `st.data_editor` to read and modify a database. Behind the scenes
this uses a simple SQLite database, but you can easily replace it with whatever your favorite DB is.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://inventory-tracker-template.streamlit.app/)

### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```
