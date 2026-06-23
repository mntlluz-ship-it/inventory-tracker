"""
MY-SUPERIOR — nueva versión minimalista y emocional

Esta implementación es una versión inicial reconstruida con enfoque visual:
"""

from datetime import date
import streamlit as st


USER_NAME = "Maye"
FAMILY_MEMBERS = [
    {"name": "Papá Wilson", "icon": "👨"},
    {"name": "Hermana Mercy", "icon": "👩"},
    {"name": "Hermano Wilson", "icon": "👦"},
    {"name": "Hermana Liceth", "icon": "👩"},
    {"name": "Amigos", "icon": "🧑👩‍🧑"},
]

MORAR_MESSAGES = [
    "¡Hola, Maye! Hoy estás brillante 🌸",
    "Respira, sigue y sonríe 💗",
    "Un abrazo virtual y energía positiva para ti 💫",
]


def inject_styles():
    st.markdown(
        """
        <style>
            :root{--pink-100:#fff0f6;--pink-200:#ffe4f2;--accent:#ff8bb2}
            .stApp { background: linear-gradient(180deg, var(--pink-200) 0%, #fff 40%); }
            .hero { padding:18px; border-radius:20px; background:linear-gradient(135deg, #fff0f6, #ffe4f2); border:1px solid rgba(255,147,191,0.4); box-shadow:0 8px 24px rgba(255,150,185,0.12); }
            .greeting { font-size:28px; color:#8f074a; margin:0; }
            .sub { color:#7d1f50; margin-top:6px; }
            .morar { padding:10px 14px; border-radius:16px; background:rgba(255,236,245,0.9); color:#6c173e; margin:12px 0; }
            .family-card { display:flex; gap:14px; align-items:center; padding:12px; border-radius:16px; background:#fff; border:1px solid rgba(255,177,202,0.6); box-shadow:0 8px 20px rgba(255,157,198,0.08); }
            .icon { width:56px; height:56px; display:flex; align-items:center; justify-content:center; font-size:28px; background:#ffdeea; border-radius:12px; color:#a2185f; }
            .name { font-weight:600; color:#54143e; margin:0; }
            .last { color:#8d326c; margin:2px 0 0 0; }
            .register { background:var(--accent); color:white; padding:8px 14px; border-radius:14px; border:none; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def get_morar():
    return MORAR_MESSAGES[date.today().day % len(MORAR_MESSAGES)]


def main():
    st.set_page_config(page_title="MY-SUPERIOR", page_icon=":sparkles:")
    inject_styles()

    st.markdown(f"<div class='hero'><p class='greeting'>Hola {USER_NAME} 💖</p><p class='sub'>Bienvenida a MY-SUPERIOR — tu coach personal.</p></div>", unsafe_allow_html=True)

    st.markdown(f"<div class='morar'><strong>Morar:</strong> {get_morar()}</div>", unsafe_allow_html=True)

    st.header("👨‍👩‍👧‍👦 Familia")
    st.write("Registra interacciones rápidas y mantén el cariño en orden.")

    for person in FAMILY_MEMBERS:
        col1, col2, col3 = st.columns([1, 6, 2])
        with col1:
            st.markdown(f"<div class='icon'>{person['icon']}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<p class='name'>{person['name']}</p><p class='last'>Último contacto: —</p>", unsafe_allow_html=True)
        with col3:
            if st.button('Registrar', key=person['name']):
                st.success(f"Interacción registrada: {person['name']}")

    st.sidebar.header("Estado emocional")
    mood = st.sidebar.selectbox("¿Cómo te sientes?", ["Excelente", "Bien", "Difícil"])
    phrase = "Hoy vas bien 💪" if mood == "Excelente" else ("No te rindas, Maye 🌸" if mood == "Difícil" else "Vamos a mejorar juntos")
    st.sidebar.info(phrase)


if __name__ == '__main__':
    main()
from datetime import date, datetime, timedelta
from pathlib import Path
import sqlite3
import json

import pandas as pd
import streamlit as st


DB_FILENAME = Path(__file__).parent / "my_superior.db"
HABITS = ["Oración", "Gym", "Natación"]
FAMILY_MEMBERS = ["Papá Wilson", "Hermana Mercy", "Hermano Wilson", "Hermana Liceth", "Amigos"]
EXPENSE_CATEGORIES = ["Moto", "Comida", "Casa", "Outfit", "Otros"]
WARDROBE_CATEGORIES = ["Camisas", "Pantalones", "Zapatos", "Accesorios", "Deportiva"]
MONTHLY_BUDGET = {"Moto": 250, "Comida": 200, "Casa": 300, "Outfit": 120, "Otros": 150}
USER_NAME = "Maye"
FAMILY_ICONS = {
    "Papá Wilson": "👨",
    "Hermana Mercy": "👩",
    "Hermano Wilson": "👦",
    "Hermana Liceth": "👩",
    "Amigos": "🧑👩‍🧑",
}
MORAR_MESSAGES = [
    "Morar dice: ¡Hola, Maye! Hoy estás brillante 🌸",
    "Morar te acompaña: Respira, sigue y sonríe 💗",
    "Morar: Un abrazo virtual y energía positiva para ti 💫",
]


def connect_db():
    db_already_exists = DB_FILENAME.exists()
    conn = sqlite3.connect(DB_FILENAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn, db_already_exists


def initialize_db(conn):
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            created_at TEXT
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            category TEXT,
            created_at TEXT
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS daily_habits (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            date TEXT,
            habit_name TEXT,
            is_done INTEGER,
            UNIQUE(user_id, date, habit_name)
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS mood_log (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            date TEXT UNIQUE,
            mood TEXT
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS motivation (
            date TEXT PRIMARY KEY,
            message TEXT,
            food_suggestion TEXT,
            tip TEXT
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS family_contacts (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            created_at TEXT
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS family_interactions (
            id INTEGER PRIMARY KEY,
            contact_id INTEGER,
            date TEXT,
            note TEXT
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            date TEXT,
            category TEXT,
            amount REAL,
            note TEXT
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS wardrobe_items (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            name TEXT,
            category TEXT,
            brand TEXT,
            price REAL,
            is_favorite INTEGER,
            use_count INTEGER,
            last_used_date TEXT,
            added_at TEXT
        )
        """
    )
    cursor.execute(
        "INSERT OR IGNORE INTO users (id, name, created_at) VALUES (1, 'Usuario', ?)'" , (datetime.utcnow().isoformat(),)
    )
    for habit in HABITS:
        cursor.execute(
            "INSERT OR IGNORE INTO habits (name, category, created_at) VALUES (?, ?, ?)",
            (habit, "Diario", datetime.utcnow().isoformat()),
        )
    for contact in FAMILY_MEMBERS:
        cursor.execute(
            "INSERT OR IGNORE INTO family_contacts (name, created_at) VALUES (?, ?)",
            (contact, datetime.utcnow().isoformat()),
        )
    conn.commit()


def load_daily_habits(conn, target_date):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT habit_name, is_done FROM daily_habits WHERE user_id = 1 AND date = ?",
        (target_date,),
    )
    rows = {row["habit_name"]: bool(row["is_done"]) for row in cursor.fetchall()}
    for habit in HABITS:
        if habit not in rows:
            cursor.execute(
                "INSERT OR IGNORE INTO daily_habits (user_id, date, habit_name, is_done) VALUES (1, ?, ?, 0)",
                (target_date, habit),
            )
            rows[habit] = False
    conn.commit()
    return rows


def save_daily_habits(conn, target_date, status):
    cursor = conn.cursor()
    for habit, done in status.items():
        cursor.execute(
            "INSERT OR REPLACE INTO daily_habits (user_id, date, habit_name, is_done) VALUES (1, ?, ?, ?)",
            (target_date, habit, int(done)),
        )
    conn.commit()


def load_mood(conn, target_date):
    cursor = conn.cursor()
    cursor.execute("SELECT mood FROM mood_log WHERE user_id = 1 AND date = ?", (target_date,))
    row = cursor.fetchone()
    return row["mood"] if row else "Excelente"


def save_mood(conn, target_date, mood):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO mood_log (user_id, date, mood) VALUES (1, ?, ?)",
        (target_date, mood),
    )
    conn.commit()


def get_week_dates(reference_date):
    return [(reference_date - timedelta(days=i)).isoformat() for i in range(6, -1, -1)]


def load_habit_history(conn):
    dates = get_week_dates(date.today())
    cursor = conn.cursor()
    history = []
    for day in dates:
        cursor.execute(
            "SELECT COUNT(*) AS total, SUM(is_done) AS done FROM daily_habits WHERE user_id = 1 AND date = ?",
            (day,),
        )
        row = cursor.fetchone()
        total = row["total"] or len(HABITS)
        done = row["done"] or 0
        history.append({"date": day, "done": done, "total": total, "percent": int(done / total * 100) if total else 0})
    return history


def load_mood_stats(conn):
    month_ago = (date.today() - timedelta(days=30)).isoformat()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT mood, COUNT(*) AS count FROM mood_log WHERE user_id = 1 AND date >= ? GROUP BY mood ORDER BY count DESC",
        (month_ago,),
    )
    return cursor.fetchall()


def load_habit_vs_mood(conn):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT m.mood, AVG(d.is_done) AS compliance FROM mood_log m JOIN daily_habits d ON m.user_id = d.user_id AND m.date = d.date WHERE m.user_id = 1 AND m.date >= ? GROUP BY m.mood",
        ((date.today() - timedelta(days=30)).isoformat(),),
    )
    return cursor.fetchall()


def get_or_generate_motivation(conn, target_date, mood, compliance):
    cursor = conn.cursor()
    cursor.execute("SELECT message, food_suggestion, tip FROM motivation WHERE date = ?", (target_date,))
    row = cursor.fetchone()
    if row:
        return row["message"], row["food_suggestion"], row["tip"]
    day_name = date.fromisoformat(target_date).strftime("%A")
    food_map = {
        "Monday": "Un batido proteico con frutas.",
        "Tuesday": "Ensalada fresca con semillas.",
        "Wednesday": "Avena con frutas y nueces.",
        "Thursday": "Pescado a la plancha con verduras.",
        "Friday": "Yogur natural con miel y frutas.",
        "Saturday": "Agua de coco y una fruta ligera.",
        "Sunday": "Huevos revueltos con espinacas.",
    }
    message = (
        "¡Hoy es un gran día para avanzar!"
        if compliance >= 0.7
        else "Vamos paso a paso, lo importante es la constancia."
        if compliance >= 0.4
        else "No te preocupes, hoy puedes reconectar con tus objetivos."
    )
    tip = (
        "Mantén tu energía con respiraciones profundas antes de comenzar."
        if mood == "Excelente"
        else "Un pequeño descanso te ayudará a retomar el enfoque."
        if mood == "Bien"
        else "Habla con alguien cercano y haz algo que te relaje."
    )
    food_suggestion = food_map.get(day_name, "Come algo ligero y nutritivo.")
    cursor.execute(
        "INSERT OR REPLACE INTO motivation (date, message, food_suggestion, tip) VALUES (?, ?, ?, ?)",
        (target_date, message, food_suggestion, tip),
    )
    conn.commit()
    return message, food_suggestion, tip


def get_family_icon(name):
    return FAMILY_ICONS.get(name, "🧑‍🤝‍🧑")


def get_emotional_coach_phrase(current_mood, compliance):
    if compliance >= 0.7:
        return "Hoy vas bien 💪"
    if current_mood == "Difícil":
        return "No te rindas, Maye 🌸"
    return "Vamos a mejorar juntos"


def get_morar_phrase():
    index = date.today().day % len(MORAR_MESSAGES)
    return MORAR_MESSAGES[index]


def load_family_contacts(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM family_contacts ORDER BY name")
    contacts = []
    for row in cursor.fetchall():
        cursor.execute(
            "SELECT date, note FROM family_interactions WHERE contact_id = ? ORDER BY date DESC LIMIT 1",
            (row["id"],),
        )
        last = cursor.fetchone()
        last_date = last["date"] if last else None
        contacts.append({"id": row["id"], "name": row["name"], "last_date": last_date})
    return contacts


def save_family_interaction(conn, contact_id, interaction_date, note):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO family_interactions (contact_id, date, note) VALUES (?, ?, ?)",
        (contact_id, interaction_date, note),
    )
    conn.commit()


def load_expenses(conn, start_date=None, end_date=None):
    cursor = conn.cursor()
    if not start_date:
        start_date = date.today().isoformat()
    if not end_date:
        end_date = date.today().isoformat()
    cursor.execute(
        "SELECT date, category, amount, note FROM expenses WHERE user_id = 1 AND date BETWEEN ? AND ? ORDER BY date DESC",
        (start_date, end_date),
    )
    return cursor.fetchall()


def add_expense(conn, expense_date, category, amount, note):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (user_id, date, category, amount, note) VALUES (1, ?, ?, ?, ?)",
        (expense_date, category, float(amount), note),
    )
    conn.commit()


def load_wardrobe(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM wardrobe_items WHERE user_id = 1 ORDER BY added_at DESC")
    return cursor.fetchall()


def add_wardrobe_item(conn, name, category, brand, price, is_favorite):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO wardrobe_items (user_id, name, category, brand, price, is_favorite, use_count, last_used_date, added_at) VALUES (1, ?, ?, ?, ?, ?, 0, NULL, ?)",
        (name, category, brand, float(price), int(is_favorite), datetime.utcnow().isoformat()),
    )
    conn.commit()


def mark_wardrobe_used(conn, item_id):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE wardrobe_items SET use_count = use_count + 1, last_used_date = ? WHERE id = ?",
        (date.today().isoformat(), item_id),
    )
    conn.commit()


def toggle_favorite(conn, item_id, current_value):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE wardrobe_items SET is_favorite = ? WHERE id = ?",
        (0 if current_value else 1, item_id),
    )
    conn.commit()


def days_since(date_string):
    if not date_string:
        return None
    return (date.today() - date.fromisoformat(date_string)).days


def inject_styles():
    st.markdown(
        """
        <style>
            body { background: linear-gradient(180deg, #ffe4f0 0%, #ffcee8 40%, #fff0f6 100%); }
            .stApp, .main, .block-container { background: transparent; }
            .css-1aumxhk, .css-12w0qpk, .css-1v3fvcr, .css-1lcbmhc, .css-1yn9l5s {
                background: rgba(255, 244, 250, 0.95) !important;
                border: 1px solid #ffb4d2 !important;
                box-shadow: 0 8px 20px rgba(255, 157, 198, 0.15);
                border-radius: 18px;
            }
            .stButton>button {
                background-color: #ff8bb2 !important;
                color: #ffffff !important;
                border-color: #ffabc6 !important;
                box-shadow: 0 8px 24px rgba(255, 133, 187, 0.25);
                border-radius: 24px !important;
                padding: 0.85rem 1.5rem !important;
                font-weight: 600;
            }
            .stButton>button:hover {
                background-color: #ff6299 !important;
            }
            .stTextArea>div>div>textarea,
            .stTextInput>div>div>input,
            .stNumberInput>div>div>input,
            .stRadio>div>label,
            .stCheckbox>div>label,
            .stSelectbox>div>div>div,
            .stMultiSelect>div>div>div {
                background-color: #fff5f9 !important;
                border: 1px solid #ffc1d8 !important;
                color: #5d1451 !important;
                border-radius: 18px !important;
            }
            h1, h2, h3, h4, h5, h6 {
                color: #b7005a !important;
            }
            .stMetric > div > div {
                background: rgba(255, 211, 230, 0.92) !important;
                border-radius: 20px !important;
                border: 1px solid rgba(255, 171, 199, 0.45) !important;
            }
            .family-card, .hero-card, .mini-yo-card, .morar-bubble {
                background: #ffffff;
                border: 1px solid rgba(255, 177, 202, 0.55);
                box-shadow: 0 10px 30px rgba(255, 157, 198, 0.12);
                border-radius: 24px;
                padding: 18px;
                margin-bottom: 14px;
            }
            .hero-card {
                background: linear-gradient(135deg, #fff0f6 0%, #ffe4f2 100%) !important;
                border: 1px solid rgba(255, 147, 191, 0.5) !important;
            }
            .hero-card h1, .hero-card h2, .hero-card h3 {
                color: #8f074a !important;
            }
            .mini-yo-card {
                display: flex;
                align-items: center;
                gap: 16px;
            }
            .mini-yo-icon,
            .family-card-icon {
                width: 58px;
                height: 58px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 30px;
                border-radius: 20px;
                background: #ffdeea;
                color: #a2185f;
                border: 1px solid rgba(255, 142, 186, 0.55);
            }
            .mini-yo-content,
            .family-card-content {
                flex: 1;
                color: #54143e;
            }
            .family-card-action button {
                background: #ff79b8;
                color: white;
                border: none;
                border-radius: 18px;
                padding: 10px 18px;
                font-weight: 600;
                cursor: pointer;
            }
            .morar-bubble {
                font-size: 0.98rem;
                color: #6c173e;
                background: rgba(255, 236, 245, 0.9);
            }
            .morar-bubble strong {
                color: #b7005a;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main():
    st.set_page_config(page_title="MY-SUPERIOR", page_icon=":sparkles:")
    inject_styles()

    conn, exists = connect_db()
    if not exists:
        initialize_db(conn)
        st.toast("Base de datos creada para MY-SUPERIOR.")

    today = date.today().isoformat()
    habit_status = load_daily_habits(conn, today)
    current_mood = load_mood(conn, today)
    history = load_habit_history(conn)
    mood_stats = load_mood_stats(conn)
    mood_habit_relation = load_habit_vs_mood(conn)

    done_habits = sum(1 for done in habit_status.values() if done)
    compliance = done_habits / len(HABITS)
    message, food_suggestion, tip = get_or_generate_motivation(conn, today, current_mood, compliance)

    contacts = load_family_contacts(conn)
    expenses_today = load_expenses(conn, today, today)
    total_today_expenses = sum(row['amount'] for row in expenses_today)
    week_start = (date.today() - timedelta(days=6)).isoformat()
    expenses_week = load_expenses(conn, week_start, today)
    total_week = sum(row['amount'] for row in expenses_week)
    month_start = date.today().replace(day=1).isoformat()
    expenses_month = load_expenses(conn, month_start, today)
    total_month = sum(row['amount'] for row in expenses_month)
    wardrobe_items = load_wardrobe(conn)

    st.markdown(
        f"""
        <div class="hero-card">
            <h1>Hola {USER_NAME} 💖</h1>
            <p style="font-size:1.06rem; margin: 0.5rem 0 0 0; color: #6f1d4e;">Bienvenida a MY-SUPERIOR, tu espacio cálido para avanzar juntas.</p>
            <p style="margin: 0.8rem 0 0 0; color: #7d1f50;">{get_emotional_coach_phrase(current_mood, compliance)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<div class='morar-bubble'><strong>Morar:</strong> {get_morar_phrase()}</div>",
        unsafe_allow_html=True,
    )
    st.subheader("📊 Dashboard principal")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Hábitos hoy", f"{done_habits}/{len(HABITS)}", f"{int(compliance*100)}%")
    c2.metric("Ánimo", current_mood)
    c3.metric("Gastos hoy", f"${total_today_expenses:.2f}")
    days_since_values = [days_since(item['last_date']) for item in contacts if item['last_date']]
    c4.metric("Máx días sin contacto", f"{max(days_since_values) if days_since_values else 0} días")
    hearts = 2 + done_habits + (1 if current_mood == "Excelente" else 0) + (1 if total_today_expenses == 0 else 0)
    c5.metric("Corazones", f"{hearts} ❤️")

    st.markdown("#### Resumen rápido")
    st.write(
        f"- Último contacto familiar: {min(days_since_values) if days_since_values else 'Aún no hay contactos registrados'} días"
    )
    st.write(f"- Total gastos semana: ${total_week:.2f}")
    st.write(f"- Total gastos mes: ${total_month:.2f}")

    with st.expander("Progreso semanal de hábitos"):
        if history:
            df_hist = pd.DataFrame(history)
            df_hist = df_hist.set_index('date')
            st.bar_chart(df_hist['percent'])
            st.write(df_hist[['done', 'total', 'percent']])
        else:
            st.write("Aún no hay datos de hábitos.")

    tabs = st.tabs(["Hábitos", "Ánimo", "Motivación", "Familia", "Gastos", "Outfit"])

    with tabs[0]:
        st.header("🧘‍♂️ Hábitos diarios")
        st.write("Marca cada hábito como hecho y guarda tu avance diario.")
        with st.form("habits_form"):
            today_status = {}
            for habit in HABITS:
                today_status[habit] = st.checkbox(habit, value=habit_status.get(habit, False))
            if st.form_submit_button("Guardar hábitos"):
                save_daily_habits(conn, today, today_status)
                st.success("Hábitos guardados para hoy.")
                habit_status.update(today_status)
        st.write(f"Cumplimiento actual: {done_habits}/{len(HABITS)} hábitos")
        st.write("Historial semanal de cumplimiento:")
        df_hist = pd.DataFrame(history)
        st.line_chart(df_hist.set_index('date')['percent'])

    with tabs[1]:
        st.header("😊 Estado de ánimo diario")
        st.write("Registra cómo te sientes hoy y revisa tu historial emocional.")
        with st.form("mood_form"):
            mood = st.radio("Selecciona tu emoción", ["Excelente", "Bien", "Difícil"], index=["Excelente", "Bien", "Difícil"].index(current_mood))
            if st.form_submit_button("Guardar ánimo"):
                save_mood(conn, today, mood)
                st.success("Estado de ánimo guardado.")
                current_mood = mood
        st.write("##### Estado más frecuente (últimos 30 días)")
        if mood_stats:
            df_mood = pd.DataFrame(mood_stats, columns=["mood", "count"])
            st.bar_chart(df_mood.set_index('mood'))
            st.write(df_mood)
        else:
            st.write("Aún no hay datos de ánimo.")
        st.write("##### Relación entre ánimo y cumplimiento")
        if mood_habit_relation:
            df_relation = pd.DataFrame(mood_habit_relation, columns=["mood", "compliance"])
            df_relation['compliance'] = df_relation['compliance'].round(2)
            st.write(df_relation)
        else:
            st.write("Necesitas registrar más datos para ver la relación.")

    with tabs[2]:
        st.header("💬 Motivación y sugerencias diarias")
        st.info(message)
        st.success(f"Sugerencia de alimentación: {food_suggestion}")
        st.write(f"**Consejo del día:** {tip}")
        st.write("Motivación adaptada según tu ánimo y cumplimiento de hábitos.")

    with tabs[3]:
        st.header("👨‍👩‍👧‍👦 Vínculos familiares y sociales")
        st.write("Registra interacciones y revisa cuándo fue el último contacto con cada persona importante para ti.")
        contact_names = {item['name']: item['id'] for item in contacts}
        selected = st.selectbox("Selecciona persona", list(contact_names.keys()))
        interaction_date = st.date_input("Fecha de interacción", value=date.today())
        note = st.text_area("Nota de la interacción", height=120)
        if st.button("Registrar interacción"):
            save_family_interaction(conn, contact_names[selected], interaction_date.isoformat(), note)
            st.success("Interacción registrada.")

        st.write("### Últimos contactos")
        for item in contacts:
            last = item['last_date'] or "Nunca"
            days = days_since(item['last_date'])
            icon = get_family_icon(item['name'])
            with st.container():
                st.markdown(
                    f"""
                    <div class='family-card'>
                        <div style='display:flex; align-items:center; gap:16px;'>
                            <div class='family-card-icon'>{icon}</div>
                            <div class='family-card-content'>
                                <h3 style='margin:0 0 6px 0;'>{item['name']}</h3>
                                <p style='margin:0; color:#7f2a5d;'>Último contacto: <strong>{last}</strong></p>
                                <p style='margin:4px 0 0 0; color:#8d326c;'>Días sin ver: <strong>{days if days is not None else '-'}</strong></p>
                            </div>
                            <div class='family-card-action'>
                                <button type='button'>Registrar</button>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        if any(days is not None and days >= 7 for days in [days_since(item['last_date']) for item in contacts]):
            st.warning("Alguno de tus contactos no ha sido visto en más de 7 días. Puedes enviarles un mensaje o agendar un encuentro.")

    with tabs[4]:
        st.header("💰 Control de gastos personales")
        st.write("Registra tus gastos diarios y compara con tu presupuesto mensual.")
        with st.form("expense_form"):
            exp_date = st.date_input("Fecha", value=date.today())
            category = st.selectbox("Categoría", EXPENSE_CATEGORIES)
            amount = st.number_input("Monto", min_value=0.0, format="%.2f")
            note_exp = st.text_input("Nota")
            if st.form_submit_button("Registrar gasto"):
                add_expense(conn, exp_date.isoformat(), category, amount, note_exp)
                st.success("Gasto registrado.")
        st.write("#### Totales")
        st.write(f"- Semana actual: ${total_week:.2f}")
        st.write(f"- Mes actual: ${total_month:.2f}")
        alert_texts = []
        for cat in EXPENSE_CATEGORIES:
            week_cat = sum(row['amount'] for row in expenses_week if row['category'] == cat)
            threshold = MONTHLY_BUDGET[cat] / 4
            if week_cat > threshold:
                alert_texts.append(f"Has gastado ${week_cat:.2f} en {cat} esta semana, cerca de tu presupuesto semanal de ${threshold:.2f}.")
        for alert in alert_texts:
            st.warning(alert)
        st.write("#### Historial reciente")
        df_expense = pd.DataFrame(expenses_today, columns=["date", "category", "amount", "note"]) if expenses_today else pd.DataFrame(columns=["date", "category", "amount", "note"])
        st.dataframe(df_expense)

    with tabs[5]:
        st.header("👕 Guardarropa")
        st.write("Agrega prendas, marca favoritas y registra lo que usaste hoy.")
        with st.form("wardrobe_form"):
            item_name = st.text_input("Nombre de la prenda")
            category = st.selectbox("Categoría", WARDROBE_CATEGORIES)
            brand = st.text_input("Marca")
            price = st.number_input("Precio", min_value=0.0, format="%.2f")
            favorite = st.checkbox("Marcar como favorita")
            if st.form_submit_button("Agregar prenda"):
                if item_name.strip():
                    add_wardrobe_item(conn, item_name.strip(), category, brand.strip(), price, favorite)
                    st.success("Prenda agregada al guardarropa.")
                else:
                    st.error("Escribe el nombre de la prenda.")
        if wardrobe_items:
            total_investment = sum(item['price'] for item in wardrobe_items)
            most_used = max(wardrobe_items, key=lambda x: x['use_count'])
            st.write(f"Total de inversión en ropa: ${total_investment:.2f}")
            st.write(f"Prenda más usada: {most_used['name']} ({most_used['use_count']} veces)")
            st.write("### Tus prendas")
            for item in wardrobe_items:
                cols = st.columns([3, 1, 1, 1])
                cols[0].markdown(f"**{item['name']}** ({item['category']})\n{item['brand']} — ${item['price']:.2f}")
                cols[1].write(f"⭐ {item['use_count']} veces")
                if cols[2].button("Usé hoy", key=f"used_{item['id']}"):
                    mark_wardrobe_used(conn, item['id'])
                    st.experimental_rerun()
                fav_label = "Desmarcar favorita" if item['is_favorite'] else "Marcar favorita"
                if cols[3].button(fav_label, key=f"fav_{item['id']}"):
                    toggle_favorite(conn, item['id'], item['is_favorite'])
                    st.experimental_rerun()
        else:
            st.write("No tienes prendas registradas aún.")


if __name__ == "__main__":
    main()
from collections import defaultdict
from pathlib import Path
import sqlite3

import streamlit as st
import altair as alt
import pandas as pd


# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title="Inventory tracker",
    page_icon=":shopping_bags:",  # This is an emoji shortcode. Could be a URL too.
)


# -----------------------------------------------------------------------------
# Declare some useful functions.


def connect_db():
    """Connects to the sqlite database."""

    DB_FILENAME = Path(__file__).parent / "inventory.db"
    db_already_exists = DB_FILENAME.exists()

    conn = sqlite3.connect(DB_FILENAME)
    db_was_just_created = not db_already_exists

    return conn, db_was_just_created


def initialize_data(conn):
    """Initializes the inventory table with some data."""
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT,
            price REAL,
            units_sold INTEGER,
            units_left INTEGER,
            cost_price REAL,
            reorder_point INTEGER,
            description TEXT
        )
        """
    )

    cursor.execute(
        """
        INSERT INTO inventory
            (item_name, price, units_sold, units_left, cost_price, reorder_point, description)
        VALUES
            -- Beverages
            ('Bottled Water (500ml)', 1.50, 115, 15, 0.80, 16, 'Hydrating bottled water'),
            ('Soda (355ml)', 2.00, 93, 8, 1.20, 10, 'Carbonated soft drink'),
            ('Energy Drink (250ml)', 2.50, 12, 18, 1.50, 8, 'High-caffeine energy drink'),
            ('Coffee (hot, large)', 2.75, 11, 14, 1.80, 5, 'Freshly brewed hot coffee'),
            ('Juice (200ml)', 2.25, 11, 9, 1.30, 5, 'Fruit juice blend'),

            -- Snacks
            ('Potato Chips (small)', 2.00, 34, 16, 1.00, 10, 'Salted and crispy potato chips'),
            ('Candy Bar', 1.50, 6, 19, 0.80, 15, 'Chocolate and candy bar'),
            ('Granola Bar', 2.25, 3, 12, 1.30, 8, 'Healthy and nutritious granola bar'),
            ('Cookies (pack of 6)', 2.50, 8, 8, 1.50, 5, 'Soft and chewy cookies'),
            ('Fruit Snack Pack', 1.75, 5, 10, 1.00, 8, 'Assortment of dried fruits and nuts'),

            -- Personal Care
            ('Toothpaste', 3.50, 1, 9, 2.00, 5, 'Minty toothpaste for oral hygiene'),
            ('Hand Sanitizer (small)', 2.00, 2, 13, 1.20, 8, 'Small sanitizer bottle for on-the-go'),
            ('Pain Relievers (pack)', 5.00, 1, 5, 3.00, 3, 'Over-the-counter pain relief medication'),
            ('Bandages (box)', 3.00, 0, 10, 2.00, 5, 'Box of adhesive bandages for minor cuts'),
            ('Sunscreen (small)', 5.50, 6, 5, 3.50, 3, 'Small bottle of sunscreen for sun protection'),

            -- Household
            ('Batteries (AA, pack of 4)', 4.00, 1, 5, 2.50, 3, 'Pack of 4 AA batteries'),
            ('Light Bulbs (LED, 2-pack)', 6.00, 3, 3, 4.00, 2, 'Energy-efficient LED light bulbs'),
            ('Trash Bags (small, 10-pack)', 3.00, 5, 10, 2.00, 5, 'Small trash bags for everyday use'),
            ('Paper Towels (single roll)', 2.50, 3, 8, 1.50, 5, 'Single roll of paper towels'),
            ('Multi-Surface Cleaner', 4.50, 2, 5, 3.00, 3, 'All-purpose cleaning spray'),

            -- Others
            ('Lottery Tickets', 2.00, 17, 20, 1.50, 10, 'Assorted lottery tickets'),
            ('Newspaper', 1.50, 22, 20, 1.00, 5, 'Daily newspaper')
        """
    )
    conn.commit()


def load_data(conn):
    """Loads the inventory data from the database."""
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM inventory")
        data = cursor.fetchall()
    except:
        return None

    df = pd.DataFrame(
        data,
        columns=[
            "id",
            "item_name",
            "price",
            "units_sold",
            "units_left",
            "cost_price",
            "reorder_point",
            "description",
        ],
    )

    return df


def update_data(conn, df, changes):
    """Updates the inventory data in the database."""
    cursor = conn.cursor()

    if changes["edited_rows"]:
        deltas = st.session_state.inventory_table["edited_rows"]
        rows = []

        for i, delta in deltas.items():
            row_dict = df.iloc[i].to_dict()
            row_dict.update(delta)
            rows.append(row_dict)

        cursor.executemany(
            """
            UPDATE inventory
            SET
                item_name = :item_name,
                price = :price,
                units_sold = :units_sold,
                units_left = :units_left,
                cost_price = :cost_price,
                reorder_point = :reorder_point,
                description = :description
            WHERE id = :id
            """,
            rows,
        )

    if changes["added_rows"]:
        cursor.executemany(
            """
            INSERT INTO inventory
                (id, item_name, price, units_sold, units_left, cost_price, reorder_point, description)
            VALUES
                (:id, :item_name, :price, :units_sold, :units_left, :cost_price, :reorder_point, :description)
            """,
            (defaultdict(lambda: None, row) for row in changes["added_rows"]),
        )

    if changes["deleted_rows"]:
        cursor.executemany(
            "DELETE FROM inventory WHERE id = :id",
            ({"id": int(df.loc[i, "id"])} for i in changes["deleted_rows"]),
        )

    conn.commit()


# -----------------------------------------------------------------------------
# Draw the actual page, starting with the inventory table.

# Set the title that appears at the top of the page.
"""
# :shopping_bags: Inventory tracker

**Welcome to Alice's Corner Store's intentory tracker!**
This page reads and writes directly from/to our inventory database.
"""

st.info(
    """
    Use the table below to add, remove, and edit items.
    And don't forget to commit your changes when you're done.
    """
)

# Connect to database and create table if needed
conn, db_was_just_created = connect_db()

# Initialize data.
if db_was_just_created:
    initialize_data(conn)
    st.toast("Database initialized with some sample data.")

# Load data from database
df = load_data(conn)

# Display data with editable table
edited_df = st.data_editor(
    df,
    disabled=["id"],  # Don't allow editing the 'id' column.
    num_rows="dynamic",  # Allow appending/deleting rows.
    column_config={
        # Show dollar sign before price columns.
        "price": st.column_config.NumberColumn(format="$%.2f"),
        "cost_price": st.column_config.NumberColumn(format="$%.2f"),
    },
    key="inventory_table",
)

has_uncommitted_changes = any(len(v) for v in st.session_state.inventory_table.values())

st.button(
    "Commit changes",
    type="primary",
    disabled=not has_uncommitted_changes,
    # Update data in database
    on_click=update_data,
    args=(conn, df, st.session_state.inventory_table),
)


# -----------------------------------------------------------------------------
# Now some cool charts

# Add some space
""
""
""

st.subheader("Units left", divider="red")

need_to_reorder = df[df["units_left"] < df["reorder_point"]].loc[:, "item_name"]

if len(need_to_reorder) > 0:
    items = "\n".join(f"* {name}" for name in need_to_reorder)

    st.error(f"We're running dangerously low on the items below:\n {items}")

""
""

st.altair_chart(
    # Layer 1: Bar chart.
    alt.Chart(df)
    .mark_bar(
        orient="horizontal",
    )
    .encode(
        x="units_left",
        y="item_name",
    )
    # Layer 2: Chart showing the reorder point.
    + alt.Chart(df)
    .mark_point(
        shape="diamond",
        filled=True,
        size=50,
        color="salmon",
        opacity=1,
    )
    .encode(
        x="reorder_point",
        y="item_name",
    ),
    use_container_width=True,
)

st.caption("NOTE: The :diamonds: location shows the reorder point.")

""
""
""

# -----------------------------------------------------------------------------

st.subheader("Best sellers", divider="orange")

""
""

st.altair_chart(
    alt.Chart(df)
    .mark_bar(orient="horizontal")
    .encode(
        x="units_sold",
        y=alt.Y("item_name").sort("-x"),
    ),
    use_container_width=True,
)
