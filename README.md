# MY-SUPERIOR

A Streamlit planner app for tracking mood, habits, family, expenses, goals, excuses, and notes.

This app saves the planner state locally using a simple SQLite database, so your entries remain available between sessions.

### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app (puerto por defecto: 8501)

   - Usando Streamlit directamente:

     ```
     $ streamlit run streamlit_app.py --server.port 8501
     ```

   - Usando el script incluido (permite cambiar el puerto con la variable `PORT`):

     ```
     $ chmod +x streamlit_app.sh
     $ PORT=8502 ./streamlit_app.sh
     ```

Si no especificas `PORT`, el script usará `8501` por defecto.
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
