import streamlit as st
import pandas as pd
import sqlite3
import os

DB_PATH = "data/kpis.db"
SQL_PATH = "src/init_db.sql"
CSV_PATH = "data/kpis_mensal.csv"


def init_database():
    """Inicializa o banco SQLite a partir do script SQL."""
    if os.path.exists(DB_PATH):
        return

    conn = sqlite3.connect(DB_PATH)
    with open(SQL_PATH, "r") as f:
        script = f.read()

    # Executa apenas os comandos de CREATE e INSERT
    for statement in script.split(";"):
        # Remove comentarios e espacos
        lines = [l for l in statement.strip().splitlines() if not l.strip().startswith("--")]
        clean = "\n".join(lines).strip()
        if clean.startswith("CREATE") or clean.startswith("INSERT"):
            conn.execute(clean)
    conn.commit()
    conn.close()


def query_db(sql):
    """Executa uma consulta e retorna um DataFrame."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df


def main():
    st.set_page_config(page_title="KPIs Comerciais", layout="wide")
    st.title("Dashboard de KPIs Comerciais")
    st.caption("Acompanhamento mensal de indicadores de receita, clientes e performance")

    init_database()

    # --- Cards principais ---
    resumo = query_db("""
        SELECT
            SUM(receita_recorrente) AS receita_total,
            SUM(novos_clientes) AS total_novos,
            SUM(cancelamentos) AS total_cancelamentos,
            ROUND(AVG(nps), 1) AS nps_medio,
            SUM(upsell) AS receita_upsell
        FROM kpis_mensal
    """)

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Receita Total (MRR)", f"R$ {resumo['receita_total'][0]:,.0f}")
    col2.metric("Novos Clientes", f"{resumo['total_novos'][0]}")
    col3.metric("Cancelamentos", f"{resumo['total_cancelamentos'][0]}")
    col4.metric("NPS Médio", f"{resumo['nps_medio'][0]}")
    col5.metric("Receita Upsell", f"R$ {resumo['receita_upsell'][0]:,.0f}")

    st.divider()

    # --- Evolucao MRR ---
    st.subheader("Evolução do MRR")
    mrr_df = query_db("SELECT mes, receita_recorrente AS MRR FROM kpis_mensal ORDER BY mes")
    st.line_chart(mrr_df.set_index("mes"))

    # --- Duas colunas ---
    left, right = st.columns(2)

    with left:
        st.subheader("Novos Clientes vs Cancelamentos")
        clientes_df = query_db("""
            SELECT mes, novos_clientes, cancelamentos
            FROM kpis_mensal ORDER BY mes
        """)
        st.bar_chart(clientes_df.set_index("mes"))

    with right:
        st.subheader("NPS Mensal")
        nps_df = query_db("SELECT mes, nps FROM kpis_mensal ORDER BY mes")
        st.line_chart(nps_df.set_index("mes"))

    st.divider()

    # --- Eficiência comercial ---
    st.subheader("Eficiência Comercial (CAC vs Upsell)")
    eficiencia_df = query_db("""
        SELECT
            mes,
            custo_aquisicao AS CAC,
            upsell AS Upsell,
            ROUND(upsell * 1.0 / NULLIF(custo_aquisicao, 0), 2) AS ROI
        FROM kpis_mensal ORDER BY mes
    """)
    st.bar_chart(eficiencia_df.set_index("mes")[["CAC", "Upsell"]])

    st.divider()

    # --- Tabela completa ---
    st.subheader("Dados Completos")
    dados = query_db("SELECT * FROM kpis_mensal ORDER BY mes")
    st.dataframe(dados, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
