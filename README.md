# Dashboard de KPIs Comerciais

Dashboard interativo construído com Streamlit e SQLite para acompanhamento mensal de indicadores comerciais de uma operação SaaS B2B. Simula o tipo de painel utilizado por equipes de RevOps e BI para monitorar receita, churn, NPS e eficiência comercial.

## O que o projeto faz

- Apresenta cards com indicadores consolidados do período (receita, novos clientes, cancelamentos, NPS, upsell)
- Exibe gráfico de evolução do MRR (Monthly Recurring Revenue)
- Compara visualmente aquisição vs cancelamento de clientes mês a mês
- Acompanha a variação do NPS ao longo do tempo
- Mostra a relação entre CAC (Custo de Aquisição) e receita de upsell
- Permite visualizar a base de dados completa em tabela interativa
- Utiliza SQLite como banco de dados, inicializado automaticamente via script SQL

## Tecnologias utilizadas

- Python 3.10+
- Streamlit (dashboard interativo)
- SQLite (banco de dados local)
- pandas (manipulação de dados)
- SQL (consultas analíticas e modelagem)

## Estrutura do projeto

```
dashboard-kpis-comerciais/
├── data/
│   └── kpis_mensal.csv        # Dados de referência
├── src/
│   ├── app.py                 # Aplicação Streamlit
│   └── init_db.sql            # Script de criação e carga do banco
├── requirements.txt
└── README.md
```

## Como executar

1. Clone o repositório:
```bash
git clone https://github.com/martamfps/dashboard-kpis-comerciais.git
cd dashboard-kpis-comerciais
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute o dashboard:
```bash
streamlit run src/app.py
```

O dashboard abre automaticamente no navegador em `http://localhost:8501`.

## Indicadores apresentados

| Indicador | Descrição |
|---|---|
| MRR | Receita recorrente mensal |
| Novos Clientes | Clientes adquiridos no mês |
| Cancelamentos | Clientes perdidos no mês (churn) |
| NPS | Net Promoter Score médio |
| CAC | Custo de aquisição por cliente |
| Upsell | Receita adicional de clientes existentes |

## Consultas SQL

O arquivo `src/init_db.sql` contém tanto a estrutura do banco quanto consultas analíticas prontas para uso, incluindo cálculo de crescimento MRR, taxa de churn e ROI de upsell.
