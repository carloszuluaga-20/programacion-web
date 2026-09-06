import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st

DB = "notas.db"

st.set_page_config(
    page_title="Gestor Académico",
    page_icon="📚",
    layout="wide"
)


# =========================
# BASE DE DATOS
# =========================

def db():
    return sqlite3.connect(DB)


def init_db():
    conn = db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS cuts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER NOT NULL,
            number INTEGER NOT NULL,
            percentage REAL NOT NULL,
            FOREIGN KEY(subject_id) REFERENCES subjects(id),
            UNIQUE(subject_id, number)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cut_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            percentage REAL NOT NULL,
            grade REAL,
            FOREIGN KEY(cut_id) REFERENCES cuts(id)
        )
    """)

    conn.commit()
    conn.close()


def subjects():
    conn = db()
    data = pd.read_sql(
        "SELECT * FROM subjects ORDER BY name",
        conn
    )
    conn.close()
    return data


def cuts(subject_id):
    conn = db()
    data = pd.read_sql(
        "SELECT * FROM cuts WHERE subject_id=? ORDER BY number",
        conn,
        params=(subject_id,)
    )
    conn.close()
    return data


def activities(cut_id):
    conn = db()
    data = pd.read_sql(
        "SELECT * FROM activities WHERE cut_id=? ORDER BY id",
        conn,
        params=(cut_id,)
    )
    conn.close()
    return data


# =========================
# CÁLCULOS
# =========================

def cut_result(cut_id):
    data = activities(cut_id)

    if data.empty:
        return 0, 0

    graded = data.dropna(subset=["grade"])

    if graded.empty:
        return 0, 0

    grade = (
        graded["grade"] *
        graded["percentage"] / 100
    ).sum()

    evaluated = graded["percentage"].sum()

    return grade, evaluated


def subject_result(subject_id):
    data = cuts(subject_id)

    accumulated = 0
    evaluated = 0

    for _, cut in data.iterrows():

        grade, percent = cut_result(
            int(cut["id"])
        )

        accumulated += (
            grade *
            cut["percentage"] / 100
        )

        evaluated += (
            percent *
            cut["percentage"] / 100
        )

    final = (
        accumulated
        if evaluated >= 99.99
        else None
    )

    return accumulated, evaluated, final


init_db()


# =========================
# MENÚ
# =========================

st.sidebar.title("📚 Gestor Académico")

page = st.sidebar.radio(
    "Menú",
    [
        "📊 Dashboard",
        "📚 Asignaturas",
        "⚙️ Cortes",
        "📝 Actividades y notas"
    ]
)


# =========================
# DASHBOARD
# =========================

if page == "📊 Dashboard":

    st.title("📊 Dashboard académico")

    data = subjects()

    if data.empty:

        st.info("Primero crea una asignatura.")

    else:

        results = []

        for _, subject in data.iterrows():

            accumulated, evaluated, final = subject_result(
                int(subject["id"])
            )

            results.append({
                "Asignatura": subject["name"],
                "Nota": (
                    final
                    if final is not None
                    else accumulated
                ),
                "Evaluado": evaluated,
                "Final": final
            })

        results = pd.DataFrame(results)

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Asignaturas",
            len(data)
        )

        col2.metric(
            "Promedio",
            f"{results['Nota'].mean():.2f}"
        )

        col3.metric(
            "Evaluado",
            f"{results['Evaluado'].mean():.1f}%"
        )

        st.divider()

        st.subheader("📋 Resumen")

        table = results.copy()

        table["Nota"] = table["Nota"].round(2)
        table["Evaluado"] = table["Evaluado"].round(1)

        table["Estado"] = table["Final"].apply(
            lambda x:
            "Finalizada"
            if pd.notna(x)
            else "En progreso"
        )

        st.dataframe(
            table[
                [
                    "Asignatura",
                    "Nota",
                    "Evaluado",
                    "Estado"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.subheader("📊 Notas por asignatura")

        fig = px.bar(
            results,
            x="Asignatura",
            y="Nota",
            text="Nota",
            range_y=[0, 5]
        )

        fig.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================
# ASIGNATURAS
# =========================

elif page == "📚 Asignaturas":

    st.title("📚 Asignaturas")

    with st.form("new_subject"):

        name = st.text_input(
            "Nombre de la asignatura",
            placeholder="Ej: Bases de Datos"
        )

        save = st.form_submit_button(
            "Guardar"
        )

        if save:

            name = name.strip()

            if not name:

                st.error(
                    "Escribe el nombre de la asignatura."
                )

            else:

                conn = db()

                try:

                    cur = conn.cursor()

                    cur.execute(
                        """
                        INSERT INTO subjects (name)
                        VALUES (?)
                        """,
                        (name,)
                    )

                    subject_id = cur.lastrowid

                    for number, percentage in [
                        (1, 30),
                        (2, 30),
                        (3, 40)
                    ]:

                        cur.execute(
                            """
                            INSERT INTO cuts
                            (subject_id, number, percentage)
                            VALUES (?, ?, ?)
                            """,
                            (
                                subject_id,
                                number,
                                percentage
                            )
                        )

                    conn.commit()

                    st.success(
                        f"'{name}' creada correctamente."
                    )

                    st.rerun()

                except sqlite3.IntegrityError:

                    st.error(
                        "Ya existe una asignatura con ese nombre."
                    )

                finally:

                    conn.close()

    st.divider()

    data = subjects()

    if data.empty:

        st.info(
            "No tienes asignaturas todavía."
        )

    else:

        for _, subject in data.iterrows():

            accumulated, evaluated, final = subject_result(
                int(subject["id"])
            )

            st.write(
                f"**{subject['name']}** — "
                f"Acumulado: **{accumulated:.2f}** — "
                f"Evaluado: **{evaluated:.0f}%**"
            )


# =========================
# CORTES
# =========================

elif page == "⚙️ Cortes":

    st.title("⚙️ Configuración de cortes")

    data = subjects()

    if data.empty:

        st.info(
            "Primero crea una asignatura."
        )

    else:

        selected = st.selectbox(
            "Asignatura",
            data["name"]
        )

        subject = data[
            data["name"] == selected
        ].iloc[0]

        subject_id = int(
            subject["id"]
        )

        data_cuts = cuts(subject_id)

        with st.form("cuts"):

            c1, c2, c3 = st.columns(3)

            p1 = c1.number_input(
                "Corte 1 (%)",
                0.0,
                100.0,
                float(
                    data_cuts.iloc[0]["percentage"]
                )
            )

            p2 = c2.number_input(
                "Corte 2 (%)",
                0.0,
                100.0,
                float(
                    data_cuts.iloc[1]["percentage"]
                )
            )

            p3 = c3.number_input(
                "Corte 3 (%)",
                0.0,
                100.0,
                float(
                    data_cuts.iloc[2]["percentage"]
                )
            )

            total = p1 + p2 + p3

            st.write(
                f"Total: **{total:.1f}%**"
            )

            save = st.form_submit_button(
                "Guardar cortes"
            )

            if save:

                if abs(total - 100) > 0.01:

                    st.error(
                        "Los cortes deben sumar exactamente 100%."
                    )

                else:

                    conn = db()
                    cur = conn.cursor()

                    for number, percentage in [
                        (1, p1),
                        (2, p2),
                        (3, p3)
                    ]:

                        cur.execute(
                            """
                            UPDATE cuts
                            SET percentage=?
                            WHERE subject_id=?
                            AND number=?
                            """,
                            (
                                percentage,
                                subject_id,
                                number
                            )
                        )

                    conn.commit()
                    conn.close()

                    st.success(
                        "Cortes actualizados."
                    )

                    st.rerun()


# =========================
# ACTIVIDADES Y NOTAS
# =========================

elif page == "📝 Actividades y notas":

    st.title("📝 Actividades y notas")

    data = subjects()

    if data.empty:

        st.info(
            "Primero crea una asignatura."
        )

    else:

        selected = st.selectbox(
            "Asignatura",
            data["name"]
        )

        subject = data[
            data["name"] == selected
        ].iloc[0]

        subject_id = int(
            subject["id"]
        )

        data_cuts = cuts(subject_id)

        cut_number = st.selectbox(
            "Corte",
            [1, 2, 3]
        )

        cut = data_cuts[
            data_cuts["number"] == cut_number
        ].iloc[0]

        cut_id = int(
            cut["id"]
        )

        data_activities = activities(
            cut_id
        )

        # =========================
        # RESUMEN DEL CORTE
        # =========================

        grade, evaluated = cut_result(
            cut_id
        )

        col1, col2 = st.columns(2)

        col1.metric(
            "Nota del corte",
            f"{grade:.2f}"
        )

        col2.metric(
            "Evaluado",
            f"{evaluated:.1f}%"
        )

        st.divider()

        # =========================
        # ACTIVIDADES EXISTENTES
        # =========================

        if not data_activities.empty:

            st.subheader(
                "📋 Actividades registradas"
            )

            show = data_activities.copy()

            show["grade"] = show["grade"].apply(
                lambda x:
                "Pendiente"
                if pd.isna(x)
                else round(x, 2)
            )

            show["percentage"] = show[
                "percentage"
            ].apply(
                lambda x: f"{x:.1f}%"
            )

            st.dataframe(
                show[
                    [
                        "name",
                        "percentage",
                        "grade"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

            st.divider()

            # =========================
            # EDITAR ACTIVIDAD
            # =========================

            st.subheader(
                "✏️ Editar actividad"
            )

            activity_options = {}

            for _, row in data_activities.iterrows():

                activity_options[
                    f"{row['name']} — {row['percentage']:.1f}%"
                ] = int(row["id"])

            selected_activity = st.selectbox(
                "Selecciona la actividad",
                list(activity_options.keys())
            )

            activity_id = activity_options[
                selected_activity
            ]

            activity = data_activities[
                data_activities["id"] == activity_id
            ].iloc[0]

            with st.form("edit_activity"):

                new_name = st.text_input(
                    "Nombre",
                    value=str(activity["name"])
                )

                new_percentage = st.number_input(
                    "Porcentaje (%)",
                    min_value=0.1,
                    max_value=100.0,
                    value=float(
                        activity["percentage"]
                    ),
                    step=0.1
                )

                already_has_grade = pd.notna(
                    activity["grade"]
                )

                has_grade = st.checkbox(
                    "Ya tengo la nota",
                    value=already_has_grade
                )

                if has_grade:

                    current_grade = (
                        3.0
                        if pd.isna(activity["grade"])
                        else float(activity["grade"])
                    )

                    new_grade = st.number_input(
                        "Nota",
                        min_value=0.0,
                        max_value=5.0,
                        value=current_grade,
                        step=0.1
                    )

                else:

                    new_grade = None

                update = st.form_submit_button(
                    "💾 Actualizar actividad"
                )

                if update:

                    new_name = new_name.strip()

                    other_percentage = data_activities[
                        data_activities["id"] != activity_id
                    ]["percentage"].sum()

                    if not new_name:

                        st.error(
                            "Escribe el nombre de la actividad."
                        )

                    elif (
                        other_percentage +
                        new_percentage > 100
                    ):

                        st.error(
                            f"El corte superaría el 100%. "
                            f"Las demás actividades ocupan "
                            f"{other_percentage:.1f}%."
                        )

                    else:

                        conn = db()
                        cur = conn.cursor()

                        cur.execute(
                            """
                            UPDATE activities
                            SET name=?,
                                percentage=?,
                                grade=?
                            WHERE id=?
                            """,
                            (
                                new_name,
                                new_percentage,
                                new_grade,
                                activity_id
                            )
                        )

                        conn.commit()
                        conn.close()

                        st.success(
                            "Actividad actualizada correctamente."
                        )

                        st.rerun()

            # =========================
            # ELIMINAR ACTIVIDAD
            # =========================

            st.subheader(
                "🗑️ Eliminar actividad"
            )

            delete_confirm = st.checkbox(
                "Quiero eliminar la actividad seleccionada"
            )

            if delete_confirm:

                if st.button(
                    "🗑️ Eliminar actividad",
                    type="primary"
                ):

                    conn = db()
                    cur = conn.cursor()

                    cur.execute(
                        """
                        DELETE FROM activities
                        WHERE id=?
                        """,
                        (activity_id,)
                    )

                    conn.commit()
                    conn.close()

                    st.success(
                        "Actividad eliminada correctamente."
                    )

                    st.rerun()

        else:

            st.info(
                "Este corte todavía no tiene actividades."
            )

        st.divider()

        # =========================
        # NUEVA ACTIVIDAD
        # =========================

        st.subheader(
            "➕ Nueva actividad"
        )

        with st.form("new_activity"):

            name = st.text_input(
                "Nombre"
            )

            percentage = st.number_input(
                "Porcentaje (%)",
                0.1,
                100.0,
                20.0,
                step=0.1
            )

            has_grade = st.checkbox(
                "Ya tengo la nota"
            )

            grade = None

            if has_grade:

                grade = st.number_input(
                    "Nota",
                    0.0,
                    5.0,
                    3.0,
                    step=0.1
                )

            save = st.form_submit_button(
                "Guardar actividad"
            )

            if save:

                name = name.strip()

                current = data_activities[
                    "percentage"
                ].sum()

                if not name:

                    st.error(
                        "Escribe el nombre de la actividad."
                    )

                elif current + percentage > 100:

                    st.error(
                        f"El corte superaría el 100%. "
                        f"Actualmente tiene {current:.1f}%."
                    )

                else:

                    conn = db()
                    cur = conn.cursor()

                    cur.execute(
                        """
                        INSERT INTO activities
                        (cut_id, name, percentage, grade)
                        VALUES (?, ?, ?, ?)
                        """,
                        (
                            cut_id,
                            name,
                            percentage,
                            grade
                        )
                    )

                    conn.commit()
                    conn.close()

                    st.success(
                        f"'{name}' guardada correctamente."
                    )

                    st.rerun()