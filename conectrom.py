import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ===============================
# CONFIGURAÇÃO DA PÁGINA
# ===============================
st.set_page_config(
    page_title="FP&A Dashboard",
    page_icon="📊",
    layout="wide"
)

# CSS da sidebar
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            background-color: #002d70 !important;
        }

        section[data-testid="stSidebar"] * {
            color: white !important;
        }

        section[data-testid="stSidebar"] .stRadio label,
        section[data-testid="stSidebar"] .stSelectbox label,
        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] div {
            color: white !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# conteúdo da sidebar
with st.sidebar:
    st.image("logo conectrom.png", width=180)

    st.markdown("<br>", unsafe_allow_html=True)

    st.image("Assinatura visual 11B.png")

# ===============================
# PRIMEIRO PROCESSO – LEITURA E LIMPEZA
# ===============================
# Contas Pagas
df1 = pd.read_excel("contas pagas ajustado.xlsx")

# Recebimentos
df2 = pd.read_excel("recebimentos ajustado.xlsx")

# Unindo bases
df = pd.concat([df1, df2], ignore_index=True)

# ===============================
# AJUSTE DE TIPOS
# ===============================
# Datas
colunas_data = ["Emissão", "Baixa"]
for col in colunas_data:
    df[col] = pd.to_datetime(df[col], format="%d/%m/%y", errors="coerce")

# Strings
colunas_string = [
    "Gerencial", "Classificação",
    "Histórico",
    "Ent/Saída Recursos", "Classificação ajustada"
]
for col in colunas_string:
    df[col] = df[col].astype("string")

# ===============================
# DE-PARA DRE
# ===============================

mapa_dre = {

    # ===============================
    # RECEITA BRUTA
    # ===============================
    **dict.fromkeys(
        [
            "RECEITA DE PRESTACAO DE SERVICOS",
            "RECEITA COM CONTRATO DE MANUTENÇÃO",
            "RECEITA COM LOCACAO DE CENTRAIS TELEFONICAS",
            "RECEITA COM LOCACAO DE EQUIPAMENTOS DIVERSOS"
        ],
        "Receita Bruta"
    ),

    # ===============================
    # OUTRAS RECEITAS
    # ===============================
    **dict.fromkeys(
        [
            "RECEITA COM ALUGUEL",
            "VENDA DE ATIVOS",
            "OUTRAS RECEITAS"
        ],
        "Outras Receitas"
    ),


    # ===============================
    # RECEITAS FINANCEIRAS
    # ===============================
    **dict.fromkeys(
        [
            "JUROS OPERACIONAIS",
            "RENDIMENTOS EM APLICACAO FINANCEIRA",
            "RENDIMENTOS DE APLICAÇÕES FINANCEIRAS"
        ],
        "Receitas Financeiras"
    ),

    # ===============================
    # DEDUÇÕES DA RECEITA
    # ===============================
    **dict.fromkeys(
        ["ISS", "ICMS", "PIS", "Pis/Cofins/Csll - Impostos lei 10.833", "DEVOLUCOES", "DEVOLUÇÕES"],
        "Deduções"
    ),

    # ===============================
    # CUSTOS DOS SERVIÇOS
    # ===============================
    **dict.fromkeys(
    [
        "13º Salário Operacional",
        "ACOS  CORDOALHAS E PROTENSAO",
        "ADESIVOS / ADITIVOS / QUIMICOS",
        "ADIANTAMENTOS - OBRAS",
        "AGLOMERANTE",
        "AGREGADO",
        "AGUA E ESGOTO - ALOJAMENTOS",
        "AGUA POTAVEL - ADMINISTRATIVO - OBRAS",
        "AJUDA DE CUSTOS - OBRA",
        "ALIMENTACAO - OBRAS",
        "ALUGUEL - ALOJAMENTOS",
        "ART DAS OBRAS",
        "AUXILIO MORADIA - OBRAS",
        "CABOS DE COMUNICACAO",
        "CABOS ELETRICOS E GUARDA",
        "Caixa de Obra",
        "CESTAS BASICAS - OBRAS",
        "COMBUSTIVEIS E LUBRIFICANTES",
        "CONCRETOS / BOMBEAMENTO / LANCAMENTO",
        "CONSTRUCAO PREDIAL (ALVENARIA / ELETRICA / HIDRAULICA / PINTURA / COBERTURA)",
        "SERVICOS TECNICOS (TOPOGRAFIA / SONDAGEM / PROJETOS / ENSAIOS / CONSULTORIA)",
        "Contratos de Terceirizados",
        "CONTRIBUICAO SINDICAL - OBRAS",
        "FGTS CREDITO CONSIGNADO  - OBRAS",
        "CUSTEIO COM VEICULOS - OBRAS",
        "MANUTENCAO DE MAQUINAS E EQUIPAMENTOS DE OBRA",
        "Desenhos Técnicos",
        "DESLOCAMENTO (UBER  TAXI  99) - OBRAS",
        "ELETRODUTO PEAD CORRUGADO E ACESSORIOS",
        "EMENDAS E SEUS ACESSORIOS",
        "ENERGIA ELETRICA - ALOJAMENTOS",
        "ENXOVAL - OBRAS",
        "EPC - OBRAS",
        "EPI - OBRAS",
        "EXAMES OCUPACIONAIS - OBRAS",
        "Fardamento/EPI - OBRAS",
        "FERIAS - OBRAS",
        "FERRAMENTAS DE UTILIZACAO EM OBRA",
        "FGTS - OBRAS",
        "FRETES E CARRETOS - OBRAS",
        "FUNDO FIXO - OBRA",
        "GELO CANTEIRO - OBRAS",
        "GRATIFICACOES - OBRAS",
        "Horas Extras - OBRAS",
        "HOSPEDAGENS PARA OBRAS",
        "Indenizações - Obras",
        "Indenizações Trabalhistas - Obras",
        "INFRAESTRUTURA CANTEIRO - OBRAS",
        "INFRAESTRUTURA VIARIA (TERRAPLENAGEM / PAVIMENTACAO / DRENAGEM / SINALIZACAO)",
        "INSS - OBRAS",
        "INTERNET - ALOJAMENTOS",
        "INTERNET - ADMINISTRATIVO DE OBRAS",
        "IRRF - OBRAS",
        "LANCHES E REFEICOES - OBRAS",
        "LAVANDERIA - ALOJAMENTOS",
        "LOCACAO DE MAQUINAS E EQUIPAMENTOS - OBRAS",
        "LOCACAO DE VEÍCULOS UTILIZADOS EM OBRA",
        "MADEIRAS E COMPENSADOS",
        "MANUTENCAO DE ALOJAMENTO",
        "MANUTENCAO DE MATERIAL DE INFORMATICA - OBRAS",
        "MANUTENCAO E CONSERVACAO MATERIAL DE OBRA",
        "Marcenaria",
        "MATERIAIS DE LIMPEZA - OBRAS",
        "MATERIAIS PARA COPA E COZINHA - ALOJAMENTOS",
        "MATERIAIS PARA COPA E COZINHA - OBRAS",
        "Material Aplicado em Obras",
        "Material de Consumo/Obras",
        "MATERIAL DE EXPEDIENTE EM OBRAS - OBRAS",
        "MEDICAMENTOS E FARMACIA - OBRAS",
        "Mercadorias para Revenda",
        "MOVEIS E UTENSILIOS DE USO EM OBRA",
        "MULTA RESCISORIA - OBRAS",
        "MULTAS DE TRANSITO - OBRAS",
        "PASSAGENS PARA OBRAS",
        "Pavimentação de Acessos",
        "PECAS DE DESGATE DE MAQUINA (FPS)",
        "SERVICOS TERCEIRIZADOS DE ALVENARIA",
        "Pensão Alimentícia - obras",
        "Processamento de Resíduos",
        "Produção",
        "PRODUTIVIDADE - OBRAS",
        "RESCISOES - OBRAS",
        "SALARIOS - OBRAS",
        "SEGURANCA PATRIMONIAL - OBRAS",
        "SEGURO DE VIDA - OBRAS",
        "Seguro Garantia - OBRAS",
        "SEGUROS DE GARANTIA - OBRAS",
        "SEGUROS DE MAQUINAS E EQUIPAMENTOS - OBRAS",
        "SEGUROS DE RESPONSABILIDADE CIVIL - OBRAS",
        "Serviços de Concretagem",
        "Serviços de Metalúrgica",
        "Serviços de Pintura",
        "SERVICOS GRAFICOS - OBRAS",
        "SERVICOS TERCEIRIZADOS ADMINISTRATIVOS EM OBRA",
        "SINISTROS /AVARIA BENS TERCEIROS (NAO VEÍCULOS) - OBRAS",
        "SINISTROS VEICULOS - OBRAS",
        "SOFTWARES E SISTEMAS - OBRAS",
        "TAXAS E LICENCIAMENTOS - OBRAS",
        "TERMINAIS E CONECTORES",
        "TREINAMENTOS - OBRAS",
        "VALE ALIMENTACAO - OBRAS",
        "VALE TRANSPORTE - OBRAS"
    ],
    "Custos dos Serviços"
    ),

    # ===============================
    # DESPESAS OPERACIONAIS
    # ===============================
    **dict.fromkeys(
    [
        "Não identificada",
        "13º Salário",
        "AGUA E ESGOTO",
        "Ajuda de Custos",
        "ALIMENTACAO",
        "ALUGUEL E TAXAS CONDOMINIAIS",
        "TAXAS ADMINISTRATIVAS",
        "Anuidades e Mensalidades",
        "Área de vivência",
        "ASSESSORIA CONTABIL",
        "ASSOCIACAO DE CLASSE MEMBROS",
        "AUXILIO MOBILIDADE",
        "AUXILIO MORADIA",
        "Bens de Pequeno Valor",
        "BRINDES",
        "Cartoes de Credito",
        "CESTAS BASICAS ",
        "Chaveiro",
        "Comissão sobre serviços ",
        "Confraternização",
        "CONSULTORIAS GESTAO",
        "Contribuição Sindical ",
        "Coordenação de SMS",
        "Copa e Cozinha",
        "CORREIOS E POSTAGENS",
        "CURSOS E ESPECIALIZACOES",
        "Custas Cartorarias",
        "CUSTEIO COM VEICULOS",
        "MANUTENCAO E CONSERVACAO DAS INSTALACOES",
        "DESLOCAMENTO (UBER  TAXI  99)",
        "Despesas Processos Judiciais",
        "DESPESAS BANCARIAS",
        "DESPESAS CARTORIAIS",
        "DESPESAS DIRETORIA",
        "DESPESAS MEDICAS",
        "DESPESAS TAXA DE CARTAO",
        "DOACOES",
        "ENERGIA ELETRICA",
        "ENXOVAL",
        "EPC - SEDE",
        "EPI - SEDE",
        "EVENTOS E CONFRATERNIZACOES",
        "EXAMES OCUPACIONAIS",
        "Fardamento/EPI",
        "FERIAS",
        "FGTS",
        "FGTS CREDITO CONSIGNADO",
        "FRETES E CARRETOS",
        "FUNDO FIXO",
        "Gerenciamento de Projetos",
        "GRATIFICACOES",
        "Honorários Advocatícios",
        "Horas Extras",
        "HOSPEDAGENS",
        "INSS",
        "INSS a Recuperar",
        "INTERNET",
        "IRRF",
        "Itens Decorativos",
        "LANCHES E REFEICOES",
        "LOCAÇÃO DE MÁQUINAS E EQUIPAMENTOS",
        "LOCACAO DE VEICULOS",
        "Manutenção de Máquinas e Equipamentos",
        "MANUTENCAO DE MATERIAL DE INFORMATICA",
        "MATERIAIS DE LIMPEZA",
        "MATERIAIS PARA COPA E COZINHA",
        "MATERIAL DE EXPEDIENTE",
        "Material de Seguranca",
        "MEDICAMENTOS E FARMACIA",
        "Movéis e Utensílios",
        "MULTA RESCISORIA",
        "MULTAS DE TRANSITO",
        "Multas Diversas",
        "Paisagismo e Jardinagem",
        "PASSAGENS",
        "Patrocínios",
        "PLANO DE SAUDE",
        "PRODUTIVIDADE",
        "PROGRAMA BOLSA DE ESTUDOS",
        "Programas de Saúde e Segurança do Trabalho",
        "Pro-Labore",
        "Propaganda e Publicidade",
        "QUALIDADE DE VIDA",
        "CUSTOS COM VEICULOS",
        "RESCISOES",
        "SALARIOS",
        "SEGURANCA PATRIMONIAL",
        "Seguro de Máquinas e Equipamentos",
        "SEGURO DE VIDA",
        "SEGURO VEICULOS - SEDE",
        "Seguros",
        "SERVICOS DE APRENDIZAGEM",
        "SERVICOS GRAFICOS",
        "Serviços Médicos",
        "SERVICOS TERCEIRIZADOS ESPECIALIZADOS",
        "Sinistro",
        "SOFTWARES E SISTEMAS",
        "SUPRIMENTO DE CAIXA",
        "TELEFONIA",
        "TREINAMENTOS",
        "VALE ALIMENTACAO",
        "VALE TRANSPORTE",
        "VEÍCULOS",
        "Viagens e Estadias"
    ],
    "Despesas Operacionais"
),

    # ===============================
    # DESPESAS FINANCEIRAS
    # ===============================
    **dict.fromkeys(
        ["Juros Passivo", "IOF",
        "Encargos s/Financiamentos",
        "JUROS DE EMPRESTIMOS/FINANCIAMENTOS",
        "SEGURO PRESTAMISTA"
        ],
        "Despesas Financeiras"
    ),
    **dict.fromkeys(
        ["ICMS HOMOLOGADO",
        "ICMS Parcelamento",
        "Impostos e Taxas",
        "ISS HOMOLOGADO",
        "ISS RETIDO - SEDE",
        "Parcelamento de Impostos",
        "Parcelamento de Impostos ",
        "IPTU",
        "DIFERENCIAL DE ALIQUOTAS (DIFAL)",
        "ICMS (DIFAL) - OBRAS"
        ],
        "Despesas Tributárias"
    ),
    # ===============================
    # IMPOSTOS
    # ===============================
    **dict.fromkeys(
        ["IRPJ s/Lucro", "Csll s/Lucro", "CSLL a Recuperar", ],
        "Imposto de Renda e CSLL"
    ),

    # ===============================
    # MOVIMENTAÇÃO FINANCEIRA – ENTRADA
    # ===============================
    **dict.fromkeys(
        ["EMPRESTIMO TOMADO - ENTRADA"],
        "Empréstimo Tomado"
    ),

    # ===============================
    # MOVIMENTAÇÃO FINANCEIRA – SAÍDA
    # ===============================
    **dict.fromkeys(
        ["EMPRESTIMOS TOMADOS","EMPRESTIMOS CEDIDOS", 
        "ENERGIAS RENOVAVEIS - EMPRESTIMO CEDIDO",],
        "Empréstimo Cedido"
    ),
    **dict.fromkeys(
        ["Veículos","(DESATIVADO) Máquinas e Equipamentos","Computadores e Periféricos",
        "EQUIPAMENTOS",
        "EQUIPAMENTOS DE TI",
        "Instalações",
        "Máquinas e Equipamentos",
        "Marcas e Patentes",
        "Materiais Adquirido de Terceiros"
        ],
        "Aquisição de Ativos"
    ),
    **dict.fromkeys(
        ["Adiantamento a diretores","ADIANTAMENTOS","DESPESAS DOS DIRETORES"],
        "Antecipação de Lucros"
    ),
    **dict.fromkeys(
        ["PLR - Participação nos Lucros e Resultados",
        "PARTICIPACAO DE LUCROS E RESULTADOS CCT - OBRAS"],
        "PLR"
    ),
    **dict.fromkeys(
        ["Empréstimos/financiamentos",
        "PARCELA PRINCIPAL EMRESTIMOS E FINANCIAMENTOS"
        ],
        "Pagamento de Empréstimos"
    ),
       **dict.fromkeys(
        ["Crédito Consignado", "Consórcio em Andamento"],
        "Consórcios e Consignados"
    ),
}

df["Grupo_DRE"] = df["Classificação ajustada"].map(mapa_dre).fillna("SEM CLASSIFICAÇÃO")


# ===============================
# FUNÇÃO DE SOMA
# ===============================
def soma(grupo):
    return df.loc[df["Grupo_DRE"] == grupo, "Composição"].sum()

# ===============================
# MONTAGEM DA DRE (ORDEM CLÁSSICA)
# ===============================
dre_layout = []

receita_bruta = soma("Receita Bruta")
deducoes = soma("Deduções")
outras_receitas = soma("Outras Receitas")
receita_liquida = receita_bruta + outras_receitas - deducoes

dre_layout += [
    ("Receita Bruta", receita_bruta),
    ("(-) Deduções da Receita", -deducoes),
    ("Outras Receitas", outras_receitas),
    ("Receita Líquida", receita_liquida),
]

custos = soma("Custos dos Serviços")
lucro_bruto = receita_liquida - custos

dre_layout += [
    ("(-) Custos dos Serviços", -custos),
    ("Lucro Bruto", lucro_bruto),
]

despesas_operacionais = soma("Despesas Operacionais")
despesas_tributarias = soma("Despesas Tributárias")
ebitda = lucro_bruto - despesas_operacionais - despesas_tributarias

dre_layout += [
    ("(-) Despesas Operacionais", -despesas_operacionais),
    ("(-) Despesas Tributárias",-despesas_tributarias),
    ("Resultado Operacional", ebitda),
]

resultado_financeiro = soma("Receitas Financeiras") - soma("Despesas Financeiras")
resultado_antes_ir = ebitda + resultado_financeiro

dre_layout += [
    ("Resultado Financeiro", resultado_financeiro),
    ("Resultado Antes dos Impostos", resultado_antes_ir),
]

ir_csll = soma("Imposto de Renda e CSLL")
resultado_liquido = resultado_antes_ir - ir_csll

dre_layout += [
    ("(-) IR/CSLL", -ir_csll),
    ("Resultado Líquido", resultado_liquido),
]

emprestimo_tom = soma("Empréstimo Tomado")
emprestimo_ced = soma("Empréstimo Cedido")
aquisicao = soma("Aquisição de Ativos")
antecip = soma("Antecipação de Lucros")
participacao = soma("PLR")
pag_emp = soma("Pagamento de Empréstimos")
cons = soma("Consórcios e Consignados")
saldo_operacional = resultado_liquido + emprestimo_tom - emprestimo_ced -aquisicao - antecip - participacao - pag_emp - cons

dre_layout += [
    ("Entrada Emprestimos", emprestimo_tom),
    ("(-) Emprestimos Cedidos", -emprestimo_ced),
    ("(-) Pagamento de Empréstimos", -pag_emp),
    ("(-) Consórcios e Consignados", -cons),
    ("(-) Aquisição de Ativos", -aquisicao),
    ("(-) Participação nos Lucros", -participacao),
    ("(-) Antecipação de Lucros", -antecip),
    ("Saldo Operacional", saldo_operacional)

]
# ===============================
# DATAFRAME FINAL DA DRE
# ===============================
dre_df = pd.DataFrame(dre_layout, columns=["Descrição", "Valor"])

# 👉 Converter para MILHARES
dre_df["Valor (R$ mil)"] = dre_df["Valor"] / 1000

# ===============================
# VISUALIZAÇÃO STREAMLIT
# ===============================
st.title("Conectrom FP&A")

# ===============================
# MENU LATERAL
# ===============================
menu = st.sidebar.radio(
    "MENU",
    ["Dashboard", "Relatório", "Tabelas"]
)

# 
# Novas linhas auxiliares
#
def formatar_mes_coluna(df_base, valor_col="Composição", idx="Gerencial"):
    tabela = (
        df_base
        .pivot_table(
            index=idx,
            columns="Ano_Mes",
            values=valor_col,
            aggfunc="sum",
            fill_value=0
        )
        .sort_index(axis=1)
    )

    tabela.columns = [col.strftime("%m/%Y") for col in tabela.columns]
    tabela = tabela.reset_index()

    return tabela


def exibir_tabela_gerencial(df_base, titulo, indice="Gerencial"):
    st.markdown(f"#### {titulo}")

    tabela = formatar_mes_coluna(df_base, valor_col="Composição", idx=indice)

    colunas_numericas = [c for c in tabela.columns if c != indice]
    tabela[colunas_numericas] = tabela[colunas_numericas] / 1000

    st.dataframe(
        tabela.style.format(
            {col: "R$ {:,.2f} mil".format for col in colunas_numericas}
        ),
        use_container_width=True
    )


def montar_percentual_sobre_receita(df_base, grupo_escolhido):
    base = df_base.copy()
    base["Ano_Mes"] = base["Baixa"].dt.to_period("M").dt.to_timestamp()

    receita_total = (
        base[base["Grupo_DRE"] == "Receita Bruta"]
        .groupby("Ano_Mes", as_index=False)["Composição"]
        .sum()
        .rename(columns={"Composição": "Receita_Bruta_Total"})
    )

    grupo_hist = (
        base[base["Grupo_DRE"] == grupo_escolhido]
        .groupby(["Ano_Mes", "Classificação ajustada"], as_index=False)["Composição"]
        .sum()
    )

    grupo_hist = grupo_hist.merge(receita_total, on="Ano_Mes", how="left")
    grupo_hist = grupo_hist[grupo_hist["Receita_Bruta_Total"] != 0].copy()
    grupo_hist["Percentual_Receita_Bruta"] = (
        grupo_hist["Composição"] / grupo_hist["Receita_Bruta_Total"]
    ) * 100

    return grupo_hist


def tabela_ranking_valor(df_base):
    ranking = (
        df_base[df_base["Grupo_DRE"].notna()]
        .groupby(["Grupo_DRE", "Classificação ajustada"], as_index=False)["Composição"]
        .sum()
        .sort_values(["Grupo_DRE", "Composição"], ascending=[True, False])
    )

    ranking["Rank na Divisão"] = (
        ranking.groupby("Grupo_DRE")["Composição"]
        .rank(method="dense", ascending=False)
        .astype(int)
    )

    ranking["Valor_R$mil"] = ranking["Composição"] / 1000

    ranking = ranking[
        ["Grupo_DRE", "Rank na Divisão", "Classificação ajustada", "Valor_R$mil"]
    ]

    return ranking


def tabela_ranking_participacao(df_base):
    ranking = (
        df_base[df_base["Grupo_DRE"].notna()]
        .groupby(["Grupo_DRE", "Classificação ajustada"], as_index=False)["Composição"]
        .sum()
    )

    total_divisao = (
        ranking.groupby("Grupo_DRE", as_index=False)["Composição"]
        .sum()
        .rename(columns={"Composição": "Total_Grupo"})
    )

    ranking = ranking.merge(total_divisao, on="Grupo_DRE", how="left")
    ranking["Participação (%)"] = (ranking["Composição"] / ranking["Total_Grupo"]) * 100

    ranking = ranking.sort_values(
        ["Grupo_DRE", "Participação (%)"], ascending=[True, False]
    )

    ranking["Rank na Divisão"] = (
        ranking.groupby("Grupo_DRE")["Participação (%)"]
        .rank(method="dense", ascending=False)
        .astype(int)
    )

    ranking["Valor_R$mil"] = ranking["Composição"] / 1000

    ranking = ranking[
        ["Grupo_DRE", "Rank na Divisão", "Classificação ajustada", "Participação (%)", "Valor_R$mil"]
    ]

    return ranking

# ===============================
# DASHBOARD
# ===============================
if menu == "Dashboard":
    # =========================================================
    # FUNÇÕES AUXILIARES DO DASHBOARD
    # =========================================================
    def formatar_tabela_mensal_gerencial(df_base, indice="Gerencial"):
        tabela = (
            df_base
            .pivot_table(
                index=indice,
                columns="Ano_Mes",
                values="Composição",
                aggfunc="sum",
                fill_value=0
            )
            .sort_index(axis=1)
        )

        tabela.columns = [col.strftime("%m/%Y") for col in tabela.columns]
        tabela = tabela.reset_index()

        colunas_numericas = [c for c in tabela.columns if c != indice]
        tabela[colunas_numericas] = tabela[colunas_numericas] / 1000

        return tabela

    def exibir_tabela_mensal_gerencial(df_base, titulo, indice="Gerencial"):
        st.markdown(f"#### {titulo}")
        tabela = formatar_tabela_mensal_gerencial(df_base, indice=indice)

        colunas_numericas = [c for c in tabela.columns if c != indice]

        st.dataframe(
            tabela.style.format({col: "R$ {:,.2f} mil" for col in colunas_numericas}),
            use_container_width=True
        )

    def montar_percentual_grupos_dre(df_base):
        base = df_base.copy()
        base["Ano_Mes"] = base["Baixa"].dt.to_period("M").dt.to_timestamp()

        receita_total = (
            base[base["Grupo_DRE"] == "Receita Bruta"]
            .groupby("Ano_Mes", as_index=False)["Composição"]
            .sum()
            .rename(columns={"Composição": "Receita_Bruta_Total"})
        )

        dre_mensal = (
            base[
                base["Grupo_DRE"].notna() &
                (~base["Grupo_DRE"].isin(["SEM CLASSIFICAÇÃO"]))
            ]
            .groupby(["Ano_Mes", "Grupo_DRE"], as_index=False)["Composição"]
            .sum()
        )

        dre_mensal = dre_mensal.merge(receita_total, on="Ano_Mes", how="left")
        dre_mensal = dre_mensal[dre_mensal["Receita_Bruta_Total"] != 0].copy()

        dre_mensal["Percentual_Receita_Bruta"] = (
            dre_mensal["Composição"] / dre_mensal["Receita_Bruta_Total"]
        ) * 100

        return dre_mensal

    def tabela_ranking_grupo(df_base, grupo_escolhido):
        ranking = (
            df_base[df_base["Grupo_DRE"] == grupo_escolhido]
            .groupby("Classificação ajustada", as_index=False)["Composição"]
            .sum()
            .sort_values("Composição", ascending=False)
            .reset_index(drop=True)
        )

        ranking["Rank"] = ranking.index + 1
        ranking["Valor_R$mil"] = ranking["Composição"] / 1000

        total_grupo = ranking["Composição"].sum()
        if total_grupo != 0:
            ranking["Participação (%)"] = (ranking["Composição"] / total_grupo) * 100
        else:
            ranking["Participação (%)"] = 0

        ranking = ranking[
            ["Rank", "Classificação ajustada", "Valor_R$mil", "Participação (%)"]
        ]

        return ranking

    # =========================================================
    # DASHBOARD – RECEITA
    # =========================================================
    st.subheader("📈 Dashboard – Receita")
    st.markdown("### Receita Bruta Mensal com Média Móvel 12M e Projeção 6M")

    receita_df = df[df["Grupo_DRE"] == "Receita Bruta"].copy()
    receita_df["Ano_Mes"] = receita_df["Baixa"].dt.to_period("M").dt.to_timestamp()

    receita_mensal = (
        receita_df
        .groupby("Ano_Mes", as_index=False)["Composição"]
        .sum()
        .sort_values("Ano_Mes")
    )

    receita_mensal["Receita_R$mil"] = receita_mensal["Composição"] / 1000

    receita_mensal = (
        receita_mensal.set_index("Ano_Mes")
        .asfreq("MS")
        .fillna(0)
        .reset_index()
    )

    receita_mensal["MM_12M_R$mil"] = (
        receita_mensal["Receita_R$mil"]
        .rolling(window=12, min_periods=1)
        .mean()
    )

    # -------------------------------
    # PROJEÇÃO DOS PRÓXIMOS 6 MESES
    # -------------------------------
    serie_base = receita_mensal["Receita_R$mil"].tolist()
    ultima_data = receita_mensal["Ano_Mes"].max()

    datas_proj = []
    valores_proj = []
    serie_expandida = serie_base.copy()

    for i in range(6):
        proxima_data = ultima_data + pd.DateOffset(months=i + 1)
        valor_proj = sum(serie_expandida[-12:]) / min(12, len(serie_expandida))

        datas_proj.append(proxima_data)
        valores_proj.append(valor_proj)
        serie_expandida.append(valor_proj)

    projecao_df = pd.DataFrame({
        "Ano_Mes": datas_proj,
        "Receita_R$mil": [None] * 6,
        "MM_12M_R$mil": valores_proj,
        "Tipo": ["Projeção"] * 6
    })

    historico_df = receita_mensal.copy()
    historico_df["Tipo"] = "Histórico"

    grafico_df = pd.concat([historico_df, projecao_df], ignore_index=True)

    vega_receita = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "layer": [
            {
                "transform": [{"filter": "datum.Tipo == 'Histórico'"}],
                "mark": {
                    "type": "bar",
                    "color": "#4e79a7",
                    "tooltip": True
                },
                "encoding": {
                    "x": {
                        "field": "Ano_Mes",
                        "type": "temporal",
                        "timeUnit": "yearmonth",
                        "title": "Mês/Ano",
                        "axis": {"format": "%m/%Y"}
                    },
                    "y": {
                        "field": "Receita_R$mil",
                        "type": "quantitative",
                        "title": "Receita (R$ mil)"
                    },
                    "tooltip": [
                        {
                            "field": "Ano_Mes",
                            "type": "temporal",
                            "title": "Mês",
                            "format": "%m/%Y"
                        },
                        {
                            "field": "Receita_R$mil",
                            "type": "quantitative",
                            "title": "Receita Real (R$ mil)",
                            "format": ",.2f"
                        }
                    ]
                }
            },
            {
                "transform": [{"filter": "datum.Tipo == 'Histórico'"}],
                "mark": {
                    "type": "line",
                    "strokeWidth": 3,
                    "color": "#59a14f"
                },
                "encoding": {
                    "x": {
                        "field": "Ano_Mes",
                        "type": "temporal",
                        "timeUnit": "yearmonth"
                    },
                    "y": {
                        "field": "MM_12M_R$mil",
                        "type": "quantitative"
                    },
                    "tooltip": [
                        {
                            "field": "Ano_Mes",
                            "type": "temporal",
                            "title": "Mês",
                            "format": "%m/%Y"
                        },
                        {
                            "field": "MM_12M_R$mil",
                            "type": "quantitative",
                            "title": "MM 12M Histórica (R$ mil)",
                            "format": ",.2f"
                        }
                    ]
                }
            },
            {
                "transform": [{"filter": "datum.Tipo == 'Projeção'"}],
                "mark": {
                    "type": "line",
                    "strokeWidth": 3,
                    "strokeDash": [6, 4],
                    "color": "#e15759"
                },
                "encoding": {
                    "x": {
                        "field": "Ano_Mes",
                        "type": "temporal",
                        "timeUnit": "yearmonth"
                    },
                    "y": {
                        "field": "MM_12M_R$mil",
                        "type": "quantitative"
                    },
                    "tooltip": [
                        {
                            "field": "Ano_Mes",
                            "type": "temporal",
                            "title": "Mês Projetado",
                            "format": "%m/%Y"
                        },
                        {
                            "field": "MM_12M_R$mil",
                            "type": "quantitative",
                            "title": "MM 12M Projetada (R$ mil)",
                            "format": ",.2f"
                        }
                    ]
                }
            }
        ],
        "height": 380
    }

    st.vega_lite_chart(grafico_df, vega_receita, use_container_width=True)

    # =========================================================
    # COMPOSIÇÃO DA RECEITA + HISTÓRICO POR CLASSIFICAÇÃO AJUSTADA
    # =========================================================
    st.subheader("📊 Composição da Receita e Histórico por Conta")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Receita Bruta por Classificação Ajustada - Últimos 12 Meses")

        ultima_data_receita = receita_df["Ano_Mes"].max()
        inicio_12m = ultima_data_receita - pd.DateOffset(months=11)

        receita_12m = receita_df[
            (receita_df["Ano_Mes"] >= inicio_12m) &
            (receita_df["Ano_Mes"] <= ultima_data_receita)
        ].copy()

        receita_class_12m = (
            receita_12m
            .groupby("Classificação ajustada", as_index=False)["Composição"]
            .sum()
            .sort_values("Composição", ascending=False)
        )

        receita_class_12m["Valor_R$mil"] = receita_class_12m["Composição"] / 1000

        vega_radial_12m = {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "mark": {
                "type": "arc",
                "innerRadius": 55,
                "stroke": "#fff"
            },
            "encoding": {
                "theta": {
                    "field": "Valor_R$mil",
                    "type": "quantitative",
                    "title": "Receita (R$ mil)"
                },
                "color": {
                    "field": "Classificação ajustada",
                    "type": "nominal",
                    "legend": {
                        "title": "Classificação ajustada",
                        "orient": "bottom"
                    }
                },
                "tooltip": [
                    {
                        "field": "Classificação ajustada",
                        "type": "nominal",
                        "title": "Classificação ajustada"
                    },
                    {
                        "field": "Valor_R$mil",
                        "type": "quantitative",
                        "title": "Receita 12M (R$ mil)",
                        "format": ",.2f"
                    }
                ]
            },
            "height": 320
        }

        st.vega_lite_chart(receita_class_12m, vega_radial_12m, use_container_width=True)

    with col2:
        st.markdown("### Histórico Mensal por Classificação Ajustada")

        contas_disponiveis = sorted(receita_df["Classificação ajustada"].dropna().unique())

        conta_selecionada = st.selectbox(
            "Selecione uma Classificação ajustada:",
            contas_disponiveis
        )

        historico_conta = receita_df[
            receita_df["Classificação ajustada"] == conta_selecionada
        ].copy()

        historico_conta = (
            historico_conta
            .groupby("Ano_Mes", as_index=False)["Composição"]
            .sum()
            .sort_values("Ano_Mes")
        )

        historico_conta["Valor_R$mil"] = historico_conta["Composição"] / 1000

        vega_historico = {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "mark": {
                "type": "bar",
                "tooltip": True
            },
            "encoding": {
                "x": {
                    "field": "Ano_Mes",
                    "type": "temporal",
                    "timeUnit": "yearmonth",
                    "title": "Mês/Ano",
                    "axis": {
                        "format": "%m/%Y",
                        "labelAngle": -35
                    }
                },
                "y": {
                    "field": "Valor_R$mil",
                    "type": "quantitative",
                    "title": "Receita (R$ mil)"
                },
                "tooltip": [
                    {
                        "field": "Ano_Mes",
                        "type": "temporal",
                        "title": "Mês",
                        "format": "%m/%Y"
                    },
                    {
                        "field": "Valor_R$mil",
                        "type": "quantitative",
                        "title": "Valor (R$ mil)",
                        "format": ",.2f"
                    }
                ]
            },
            "height": 320
        }

        st.vega_lite_chart(historico_conta, vega_historico, use_container_width=True)

    # =========================================================
    # RECEITA POR GERENCIAL + TABELA
    # =========================================================
    st.markdown("### Receita Bruta por Centro de Lucros")

    receita_cl = (
        receita_df
        .groupby(["Ano_Mes", "Gerencial"], as_index=False)["Composição"]
        .sum()
    )

    receita_cl["Receita_R$mil"] = receita_cl["Composição"] / 1000

    staked_bar = px.bar(
        receita_cl,
        x="Ano_Mes",
        y="Receita_R$mil",
        color="Gerencial",
        labels={
            "Ano_Mes": "Mês",
            "Receita_R$mil": "Receita (R$ mil)",
            "Gerencial": "Centro de Lucros"
        }
    )

    staked_bar.update_xaxes(tickformat="%m/%Y")
    st.plotly_chart(staked_bar, use_container_width=True)

    exibir_tabela_mensal_gerencial(
        receita_cl,
        "Tabela mensal – Receita Bruta por Centro de Lucros"
    )

    # =========================================================
    # GRÁFICO: GRUPOS DA DRE SOBRE RECEITA BRUTA
    # =========================================================
    st.subheader("📉 Divisões da DRE sobre a Receita Bruta Total")

    percentual_dre_df = montar_percentual_grupos_dre(df)

    grupos_exibir = sorted([
        g for g in percentual_dre_df["Grupo_DRE"].dropna().unique()
        if g != "SEM CLASSIFICAÇÃO"
    ])

    grupos_selecionados = st.multiselect(
        "Selecione os grupos da DRE para visualizar sobre a Receita Bruta:",
        grupos_exibir,
        default=grupos_exibir[:5] if len(grupos_exibir) > 5 else grupos_exibir
    )

    base_plot = percentual_dre_df[
        percentual_dre_df["Grupo_DRE"].isin(grupos_selecionados)
    ].copy()

    grafico_percentual = px.line(
        base_plot,
        x="Ano_Mes",
        y="Percentual_Receita_Bruta",
        color="Grupo_DRE",
        markers=True,
        labels={
            "Ano_Mes": "Mês",
            "Percentual_Receita_Bruta": "% da Receita Bruta",
            "Grupo_DRE": "Divisão DRE"
        }
    )

    grafico_percentual.update_xaxes(tickformat="%m/%Y")
    grafico_percentual.update_yaxes(ticksuffix="%")

    st.plotly_chart(grafico_percentual, use_container_width=True)

    # =========================================================
    # DASHBOARD – CUSTOS
    # =========================================================
    st.subheader("📈 Dashboard – Custos e Despesas")

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### Custos Mensais")

        custos_df = df[df["Grupo_DRE"] == "Custos dos Serviços"].copy()
        custos_df["Ano_Mes"] = custos_df["Baixa"].dt.to_period("M").dt.to_timestamp()

        custos_mensal = (
            custos_df
            .groupby("Ano_Mes", as_index=False)["Composição"]
            .sum()
        )

        custos_mensal["custos_R$mil"] = custos_mensal["Composição"] / 1000

        vega_area_custos = {
            "$schema": "https://vega.github.io/schema/vega-lite/v6.json",
            "mark": {
                "type": "area",
                "line": True,
                "point": True
            },
            "encoding": {
                "x": {
                    "field": "Ano_Mes",
                    "type": "temporal",
                    "timeUnit": "yearmonth",
                    "title": "Mês/Ano",
                    "axis": {"format": "%m/%Y"}
                },
                "y": {
                    "field": "custos_R$mil",
                    "type": "quantitative",
                    "title": "Custos (R$ mil)"
                },
                "tooltip": [
                    {
                        "field": "Ano_Mes",
                        "type": "temporal",
                        "title": "Mês",
                        "format": "%m/%Y"
                    },
                    {
                        "field": "custos_R$mil",
                        "type": "quantitative",
                        "title": "Custos (R$ mil)",
                        "format": ",.2f"
                    }
                ]
            },
            "height": 300
        }

        st.vega_lite_chart(custos_mensal, vega_area_custos, use_container_width=True)

    with col4:
        st.markdown("### Custos por Classificação Ajustada")

        custos_class = (
            df[df["Grupo_DRE"] == "Custos dos Serviços"]
            .groupby("Classificação ajustada", as_index=False)["Composição"]
            .sum()
            .sort_values("Composição", ascending=False)
        )

        custos_class["Valor_R$mil"] = custos_class["Composição"] / 1000

        vega_radial_custos = {
            "mark": {
                "type": "arc",
                "innerRadius": 50,
                "stroke": "#fff"
            },
            "encoding": {
                "theta": {
                    "field": "Valor_R$mil",
                    "type": "quantitative",
                    "title": "Custos (R$ mil)"
                },
                "color": {
                    "field": "Classificação ajustada",
                    "type": "nominal",
                    "legend": {
                        "title": "Classificação ajustada",
                        "orient": "right"
                    }
                },
                "tooltip": [
                    {
                        "field": "Classificação ajustada",
                        "type": "nominal",
                        "title": "Classificação ajustada"
                    },
                    {
                        "field": "Valor_R$mil",
                        "type": "quantitative",
                        "title": "Custos (R$ mil)",
                        "format": ",.2f"
                    }
                ]
            },
            "height": 300,
            "width": 300
        }

        st.vega_lite_chart(custos_class, vega_radial_custos, use_container_width=True)

    st.markdown("### Divisão por Centro de Custos")

    custos_cl = (
        custos_df
        .groupby(["Ano_Mes", "Gerencial"], as_index=False)["Composição"]
        .sum()
    )

    custos_cl["custos_R$mil"] = custos_cl["Composição"] / 1000

    staked_bar_c = px.bar(
        custos_cl,
        x="Ano_Mes",
        y="custos_R$mil",
        color="Gerencial",
        labels={
            "Ano_Mes": "Mês",
            "custos_R$mil": "Custos (R$ mil)",
            "Gerencial": "Centro de Custos"
        }
    )

    staked_bar_c.update_xaxes(tickformat="%m/%Y")
    st.plotly_chart(staked_bar_c, use_container_width=True)

    exibir_tabela_mensal_gerencial(
        custos_cl,
        "Tabela mensal – Custos por Centro de Custos"
    )

    # =========================================================
    # DASHBOARD – DESPESAS OPERACIONAIS
    # =========================================================
    col5, col6 = st.columns(2)

    with col5:
        st.markdown("### Despesas Operacionais Mensais")

        despesas_df = df[df["Grupo_DRE"] == "Despesas Operacionais"].copy()
        despesas_df["Ano_Mes"] = despesas_df["Baixa"].dt.to_period("M").dt.to_timestamp()

        despesas_mensal = (
            despesas_df
            .groupby("Ano_Mes", as_index=False)["Composição"]
            .sum()
        )

        despesas_mensal["despesas_R$mil"] = despesas_mensal["Composição"] / 1000

        vega_area_despesas = {
            "$schema": "https://vega.github.io/schema/vega-lite/v6.json",
            "mark": {
                "type": "area",
                "line": True,
                "point": True
            },
            "encoding": {
                "x": {
                    "field": "Ano_Mes",
                    "type": "temporal",
                    "timeUnit": "yearmonth",
                    "title": "Mês/Ano",
                    "axis": {"format": "%m/%Y"}
                },
                "y": {
                    "field": "despesas_R$mil",
                    "type": "quantitative",
                    "title": "Despesas (R$ mil)"
                },
                "tooltip": [
                    {
                        "field": "Ano_Mes",
                        "type": "temporal",
                        "title": "Mês",
                        "format": "%m/%Y"
                    },
                    {
                        "field": "despesas_R$mil",
                        "type": "quantitative",
                        "title": "Despesas (R$ mil)",
                        "format": ",.2f"
                    }
                ]
            },
            "height": 300
        }

        st.vega_lite_chart(despesas_mensal, vega_area_despesas, use_container_width=True)

    with col6:
        st.markdown("### Despesas Operacionais por Classificação Ajustada")

        despesas_class = (
            df[df["Grupo_DRE"] == "Despesas Operacionais"]
            .groupby("Classificação ajustada", as_index=False)["Composição"]
            .sum()
            .sort_values("Composição", ascending=False)
        )

        despesas_class["Valor_R$mil"] = despesas_class["Composição"] / 1000

        vega_radial_despesas = {
            "mark": {
                "type": "arc",
                "innerRadius": 50,
                "stroke": "#fff"
            },
            "encoding": {
                "theta": {
                    "field": "Valor_R$mil",
                    "type": "quantitative",
                    "title": "Despesas Operacionais (R$ mil)"
                },
                "color": {
                    "field": "Classificação ajustada",
                    "type": "nominal",
                    "legend": {
                        "title": "Classificação ajustada",
                        "orient": "right"
                    }
                },
                "tooltip": [
                    {
                        "field": "Classificação ajustada",
                        "type": "nominal",
                        "title": "Classificação ajustada"
                    },
                    {
                        "field": "Valor_R$mil",
                        "type": "quantitative",
                        "title": "Despesas Operacionais (R$ mil)",
                        "format": ",.2f"
                    }
                ]
            },
            "height": 300,
            "width": 300
        }

        st.vega_lite_chart(despesas_class, vega_radial_despesas, use_container_width=True)

    st.markdown("### Divisão por Centro de Custos")

    despesas_cl = (
        despesas_df
        .groupby(["Ano_Mes", "Gerencial"], as_index=False)["Composição"]
        .sum()
    )

    despesas_cl["despesas_R$mil"] = despesas_cl["Composição"] / 1000

    staked_bar_d = px.bar(
        despesas_cl,
        x="Ano_Mes",
        y="despesas_R$mil",
        color="Gerencial",
        labels={
            "Ano_Mes": "Mês",
            "despesas_R$mil": "Despesas Operacionais (R$ mil)",
            "Gerencial": "Centro de Custos"
        }
    )

    staked_bar_d.update_xaxes(tickformat="%m/%Y")
    st.plotly_chart(staked_bar_d, use_container_width=True)

    exibir_tabela_mensal_gerencial(
        despesas_cl,
        "Tabela mensal – Despesas Operacionais por Centro de Custos"
    )

    # =========================================================
    # RANKING POR GRUPO DA DRE
    # =========================================================
    st.subheader("🏆 Ranking das Classificações Ajustadas por Grupo da DRE")

    grupos_ranking = sorted([
        g for g in df["Grupo_DRE"].dropna().unique()
        if g not in ["SEM CLASSIFICAÇÃO"]
    ])

    grupo_ranking_escolhido = st.selectbox(
        "Selecione o grupo da DRE para ver o ranking das Classificações ajustadas:",
        grupos_ranking
    )

    ranking_grupo_df = tabela_ranking_grupo(df, grupo_ranking_escolhido)

    st.markdown(f"### Ranking – {grupo_ranking_escolhido}")

    st.dataframe(
        ranking_grupo_df.style.format({
            "Valor_R$mil": "R$ {:,.2f} mil",
            "Participação (%)": "{:,.2f}%"
        }),
        use_container_width=True,
        height=500
    )
# ===============================
# RELATÓRIO
# ===============================
elif menu == "Relatório":
    st.subheader("Disclaimer")
    st.markdown(
    """
    <div style="text-align: justify; font-size: 22px; line-height: 1.3;">

    A presente análise foi desenvolvida exclusivamente com base nas informações fornecidas pela Conectrom, empresa atuante no setor da construção civil, especializada na construção de estações e redes de distribuição de energia elétrica.<br><br>

    As informações analisadas contemplam o período até setembro de 2025. O material teve como objetivo contribuir para a maturidade e o desenvolvimento de uma gestão financeira mais assertiva, por meio de uma visão estruturada e orientada à tomada de decisão.<br><br>

    A análise foi organizada em três seções principais de informações e resultados. A primeira parte apresentou uma comparação das informações contábeis da companhia com referências de mercado. Em seguida, a segunda parte abordou o comportamento financeiro da empresa ao longo dos exercícios de 2023, 2024 e 2025 (até setembro). Por fim, foram apresentadas conclusões e sugestões relacionadas às ações necessárias para aprimoramento da gestão financeira.<br><br>

    Adicionalmente, foram incorporadas análises de <b>Necessidade de Capital de Giro (NCG)</b> e <b>Ponto de Equilíbrio</b>, com o objetivo de aprofundar a compreensão sobre a estrutura financeira, capacidade de geração de resultado e necessidade de financiamento das operações.<br><br>

    O material foi disponibilizado em formato digital, por meio de link, contemplando dashboards de acompanhamento, relatórios com atualizações e a base de dados utilizada, construída a partir das informações fornecidas pela empresa.


    <b>Equipe de FP&A - FMCE</b>

    </div>
    """,
    unsafe_allow_html=True,)

    st.subheader("Dados Utilizados")
    st.markdown(
    """
    <div style="text-align: justify; font-size: 22px; line-height: 1.3;">

    Para a avaliação financeira, foram utilizados relatórios extraídos via sistema e fornecidos pela equipe financeira da Conectrom.<br><br>

    O relatório base utilizado consiste no controle de contas pagas e recebidas, que serviu como principal fonte para a construção das análises. Como suporte e complementação das informações, também foram considerados os seguintes relatórios: Relatório de Produção, Demonstração Financeira, Plano de Contas utilizado e Conciliação Bancária.

    </div>
    """,
    unsafe_allow_html=True
)

    st.subheader("Materiais Entregues")
    with open("FASE 1 - CONECTROM.pdf", "rb") as file:
        st.download_button(
            label="FASE 1 - CONECTROM",
            data=file,
            file_name="FASE 1 - CONECTROM.pdf",
            mime="application/pdf"
        )
    with open("FASE 2 - CONECTROM.pdf", "rb") as file:
        st.download_button(
            label="FASE 2 - CONECTROM",
            data=file,
            file_name="FASE 2 - CONECTROM.pdf",
            mime="application/pdf"
        )
    with open("PLANO DE CONTAS  - Conectrom.xlsx", "rb") as file:
        st.download_button(
            label="PLANO DE CONTAS",
            data=file,
            file_name="PLANO DE CONTAS - Conectrom.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )        

    st.subheader("📊 Demonstração do Resultado do Exercício (DRE)")
    st.dataframe(
        dre_df[["Descrição", "Valor (R$ mil)"]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Valor (R$ mil)": st.column_config.NumberColumn(
                "Valor (R$ mil)",
                format="R$ %.2f"
            )
        }
    )


    st.subheader("Principais Pontos de Destaque")

    st.markdown(
    """
    <div style="text-align: justify; font-size: 22px; line-height: 1.3;">

    <b>1. Margem operacional positiva, porém pressionada pela estrutura de despesas</b><br>
    A companhia apresentou Receita Líquida de aproximadamente R$ 295,1 milhões com Lucro Bruto de cerca de 69,2 milhões, o que corresponde a uma margem bruta de aproximadamente 23,5%. Apesar disso, o Resultado Operacional foi de cerca de 28,6 milhões de reais, equivalente a uma margem operacional próxima de 9,7%, evidenciando que parte relevante da geração bruta é consumida pela estrutura de despesas operacionais. Esse comportamento reforça a importância de ações voltadas ao ganho de eficiência e ao controle das despesas administrativas e operacionais.

    <br>

    <b>2. Estrutura de custos elevada com impacto direto sobre a rentabilidade</b><br>
    Os Custos dos Serviços somaram aproximadamente R$ 225,9 milhões, representando cerca de 76% da Receita Líquida. Esse percentual demonstra uma operação intensiva em custos diretos, característica compatível com o setor de atuação da empresa, mas que também evidencia elevada sensibilidade da rentabilidade a variações nessa linha. Assim, melhorias na gestão dos custos operacionais tendem a gerar impacto significativo sobre a margem e sobre o resultado final do negócio.

    <br>

    <b>3. Resultado líquido positivo, mas com baixa conversão em disponibilidade financeira</b><br>
    O Lucro Líquido apurado foi de aproximadamente R$ 14,3 milhões, equivalente a uma margem líquida próxima de 4,8%. Entretanto, observa-se consumo relevante de recursos em linhas como aquisição de ativos, antecipação de lucros e pagamento de empréstimos, o que contribuiu para que o saldo operacional final permanecesse em patamar reduzido, em torno de 744 mil reais. Esse cenário indica que, embora a empresa apresente lucro contábil, a conversão desse resultado em caixa ainda se mostra limitada, exigindo atenção sobre capital de giro, liquidez e planejamento financeiro.

    </div>
    """,
    unsafe_allow_html=True
    )

    def grafico_duplo_valor_percentual(df_base, grupo_dre, titulo):
        base = df_base.copy()
        base["Ano_Mes"] = base["Baixa"].dt.to_period("M").dt.to_timestamp()

        # Receita Bruta mensal
        receita_mensal = (
            base[base["Grupo_DRE"] == "Receita Bruta"]
            .groupby("Ano_Mes", as_index=False)["Composição"]
            .sum()
            .rename(columns={"Composição": "Receita_Bruta"})
        )

        # Grupo mensal
        grupo_mensal = (
            base[base["Grupo_DRE"] == grupo_dre]
            .groupby("Ano_Mes", as_index=False)["Composição"]
            .sum()
            .rename(columns={"Composição": "Valor_Grupo"})
        )

        graf_df = receita_mensal.merge(grupo_mensal, on="Ano_Mes", how="left")
        graf_df["Valor_Grupo"] = graf_df["Valor_Grupo"].fillna(0)

        graf_df["Valor_R$mil"] = graf_df["Valor_Grupo"] / 1000
        graf_df["Percentual_Receita"] = np.where(
            graf_df["Receita_Bruta"] != 0,
            (graf_df["Valor_Grupo"] / graf_df["Receita_Bruta"]) * 100,
            np.nan
        )

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Valor em R$
        fig.add_trace(
            go.Bar(
                x=graf_df["Ano_Mes"],
                y=graf_df["Valor_R$mil"],
                name=f"{titulo} (R$ mil)",
                hovertemplate="%{x|%m/%Y}<br>Valor: R$ %{y:,.2f} mil<extra></extra>"
            ),
            secondary_y=False
        )

        # % sobre receita
        fig.add_trace(
            go.Scatter(
                x=graf_df["Ano_Mes"],
                y=graf_df["Percentual_Receita"],
                name=f"{titulo} / Receita Bruta (%)",
                mode="lines+markers",
                hovertemplate="%{x|%m/%Y}<br>% Receita: %{y:,.2f}%<extra></extra>"
            ),
            secondary_y=True
        )

        fig.update_layout(
            title=titulo,
            xaxis_title="Mês",
            legend_title="Indicadores",
            hovermode="x unified",
            height=420
        )

        fig.update_xaxes(tickformat="%m/%Y")
        fig.update_yaxes(title_text="Valor (R$ mil)", secondary_y=False)
        fig.update_yaxes(title_text="% da Receita Bruta", ticksuffix="%", secondary_y=True)

        st.plotly_chart(fig, use_container_width=True)

        # tabela de apoio opcional
        tabela = graf_df[["Ano_Mes", "Valor_R$mil", "Percentual_Receita"]].copy()
        tabela["Ano_Mes"] = tabela["Ano_Mes"].dt.strftime("%m/%Y")

        st.dataframe(
            tabela.style.format({
                "Valor_R$mil": "R$ {:,.2f} mil",
                "Percentual_Receita": "{:,.2f}%"
            }),
            use_container_width=True,
            height=220
        )

# =========================================================
# GRÁFICOS – VALOR EM R$ E % DA RECEITA BRUTA
# =========================================================
    st.subheader("📊 Análise das Principais Estruturas de Gasto")
    st.subheader("Principais Pontos de Destaque")

    st.markdown(
    """
    <div style="text-align: justify; font-size: 22px; line-height: 1.3;">

    1. Forte concentração de valores nas principais classificações  
    Observa-se que os maiores valores estão concentrados em um número reduzido de classificações, indicando que poucas contas possuem impacto relevante sobre o resultado total. Esse comportamento sugere a necessidade de foco gerencial nessas principais linhas, uma vez que pequenas variações nelas podem gerar impactos significativos no desempenho financeiro.

    <br>

    2. Presença de diversas contas com baixo impacto individual  
    Após os principais itens do ranking, há uma queda acentuada nos valores, evidenciando a existência de diversas contas com baixa representatividade. Esse cenário pode indicar oportunidades de simplificação da estrutura analítica e maior direcionamento dos esforços para as contas de maior relevância.

    <br>

    3. Tendência de crescimento dos custos ao longo do tempo  
    A análise temporal dos custos demonstra um comportamento crescente ao longo dos períodos avaliados, indicando expansão operacional ou aumento da atividade. Esse movimento exige acompanhamento contínuo, especialmente em relação à evolução da receita, para garantir manutenção ou melhoria das margens.

    <br>

    4. Momentos de aceleração no crescimento dos custos  
    Observa-se que em determinados períodos há aumento mais acentuado dos custos, o que pode estar relacionado a sazonalidade, novos projetos ou mudanças na estrutura operacional. Esses pontos devem ser analisados de forma mais detalhada para identificação das causas e avaliação de sustentabilidade.

    <br>

    5. Indício de pressão estrutural sobre a rentabilidade  
    O crescimento consistente dos custos, quando não acompanhado proporcionalmente pela receita, pode gerar pressão sobre as margens. Esse comportamento reforça a importância do controle de custos e da análise contínua da eficiência operacional.

    </div>
    """,
    unsafe_allow_html=True
    )
    grafico_duplo_valor_percentual(
        df,
        "Despesas Operacionais",
        "Despesas Operacionais"
    )

    grafico_duplo_valor_percentual(
        df,
        "Despesas Financeiras",
        "Despesas Financeiras"
    )

    grafico_duplo_valor_percentual(
        df,
        "Despesas Tributárias",
        "Despesas Tributárias"
    )

    grafico_duplo_valor_percentual(
        df,
        "Custos dos Serviços",
        "Custos dos Serviços"
    )
# =========================================================
# GRÁFICO – PONTO DE EQUILÍBRIO (BASE: MÉDIA MÓVEL 12M)
# =========================================================
    st.subheader("⚖️ Ponto de Equilíbrio (Média dos Últimos 12 Meses)")

    base_pe = df.copy()
    base_pe["Ano_Mes"] = base_pe["Baixa"].dt.to_period("M").dt.to_timestamp()

    mensal_grupos = (
        base_pe
        .groupby(["Ano_Mes", "Grupo_DRE"], as_index=False)["Composição"]
        .sum()
    )

    pe_mensal = (
        mensal_grupos
        .pivot(index="Ano_Mes", columns="Grupo_DRE", values="Composição")
        .fillna(0)
        .reset_index()
        .sort_values("Ano_Mes")
    )

    # Garantir colunas
    for col in ["Receita Bruta", "Custos dos Serviços", "Despesas Operacionais"]:
        if col not in pe_mensal.columns:
            pe_mensal[col] = 0

    # Converter para R$ mil
    pe_mensal["Receita_R$mil"] = pe_mensal["Receita Bruta"] / 1000
    pe_mensal["Custos_Variaveis_R$mil"] = pe_mensal["Custos dos Serviços"] / 1000
    pe_mensal["Despesas_Fixas_R$mil"] = pe_mensal["Despesas Operacionais"] / 1000

    # ===============================
    # MÉDIAS MÓVEIS DE 12 MESES
    # ===============================
    pe_mensal["Receita_MM12"] = (
        pe_mensal["Receita_R$mil"]
        .rolling(window=12, min_periods=1)
        .mean()
    )

    pe_mensal["Custos_Variaveis_MM12"] = (
        pe_mensal["Custos_Variaveis_R$mil"]
        .rolling(window=12, min_periods=1)
        .mean()
    )

    pe_mensal["Despesas_Fixas_MM12"] = (
        pe_mensal["Despesas_Fixas_R$mil"]
        .rolling(window=12, min_periods=1)
        .mean()
    )

    # ===============================
    # MARGEM DE CONTRIBUIÇÃO COM BASE NA MM12
    # ===============================
    pe_mensal["Margem_Contribuicao_MM12"] = (
        pe_mensal["Receita_MM12"] - pe_mensal["Custos_Variaveis_MM12"]
    )

    pe_mensal["MC_percentual_MM12"] = np.where(
        pe_mensal["Receita_MM12"] != 0,
        pe_mensal["Margem_Contribuicao_MM12"] / pe_mensal["Receita_MM12"],
        np.nan
    )

    # ===============================
    # PONTO DE EQUILÍBRIO COM BASE NA MM12
    # ===============================
    pe_mensal["Ponto_Equilibrio_MM12"] = np.where(
        pe_mensal["MC_percentual_MM12"] > 0,
        pe_mensal["Despesas_Fixas_MM12"] / pe_mensal["MC_percentual_MM12"],
        np.nan
    )

    # Folga comparando a receita média 12M com o ponto de equilíbrio 12M
    pe_mensal["Folga_MM12"] = (
        pe_mensal["Receita_MM12"] - pe_mensal["Ponto_Equilibrio_MM12"]
    )

    # Status
    pe_mensal["Status_PE"] = np.where(
        pe_mensal["Folga_MM12"] >= 0,
        "Acima do ponto de equilíbrio",
        "Abaixo do ponto de equilíbrio"
    )

    # ===============================
    # CARDS
    # ===============================
    col_pe1, col_pe2, col_pe3 = st.columns(3)

    ultimo_mes_pe = pe_mensal.dropna(subset=["Ponto_Equilibrio_MM12"]).copy()

    if not ultimo_mes_pe.empty:
        ultima_linha_pe = ultimo_mes_pe.sort_values("Ano_Mes").iloc[-1]

        col_pe1.metric(
            "Receita média 12M",
            f"R$ {ultima_linha_pe['Receita_MM12']:,.2f} mil"
        )
        col_pe2.metric(
            "Ponto de equilíbrio 12M",
            f"R$ {ultima_linha_pe['Ponto_Equilibrio_MM12']:,.2f} mil"
        )
        col_pe3.metric(
            "Folga 12M",
            f"R$ {ultima_linha_pe['Folga_MM12']:,.2f} mil"
        )

    st.subheader("Principais Pontos de Destaque")

    st.markdown(
    """
    <div style="text-align: justify; font-size: 22px; line-height: 1.3;">

    1. Estrutura próxima ao ponto de equilíbrio  
    A análise da DRE evidencia que uma parcela relevante da receita é consumida por custos operacionais e despesas, reduzindo de forma significativa as margens ao longo da estrutura. Esse comportamento indica que a operação se encontra próxima ao ponto de equilíbrio, onde pequenas variações podem gerar impactos relevantes no resultado final.

    <br>

    2. Alta sensibilidade do resultado às variações operacionais  
    Dado o nível de comprometimento da receita, o resultado apresenta elevada sensibilidade a alterações na operação. Crescimentos de receita tendem a ampliar a geração de resultado de forma relevante, enquanto aumentos de custos ou retrações de faturamento podem rapidamente pressionar as margens.

    <br>

    3. Importância de gestão ativa para geração de folga operacional  
    A proximidade ao ponto de equilíbrio reforça a necessidade de ações voltadas ao aumento da margem, seja por crescimento de receita com estrutura controlada, seja pela otimização de custos e despesas. O monitoramento contínuo desse indicador é fundamental para garantir maior segurança financeira e estabilidade dos resultados.

    </div>
    """,
    unsafe_allow_html=True
    )
    # ===============================
    # GRÁFICO PRINCIPAL
    # ===============================
    grafico_pe = px.line(
        pe_mensal,
        x="Ano_Mes",
        y=["Receita_MM12", "Ponto_Equilibrio_MM12"],
        markers=True,
        labels={
            "Ano_Mes": "Mês",
            "value": "Valor (R$ mil)",
            "variable": "Indicador"
        }
    )

    grafico_pe.update_layout(legend_title_text="Indicador")
    grafico_pe.update_traces(mode="lines+markers")
    grafico_pe.update_xaxes(tickformat="%m/%Y")

    st.plotly_chart(grafico_pe, use_container_width=True)

    # ===============================
    # GRÁFICO DE FOLGA
    # ===============================
    st.markdown("### Folga em relação ao ponto de equilíbrio (MM 12M)")
    

    grafico_folga = px.bar(
        pe_mensal,
        x="Ano_Mes",
        y="Folga_MM12",
        color="Status_PE",
        labels={
            "Ano_Mes": "Mês",
            "Folga_MM12": "Folga / Defasagem (R$ mil)",
            "Status_PE": "Status"
        }
    )

    grafico_folga.update_xaxes(tickformat="%m/%Y")

    st.plotly_chart(grafico_folga, use_container_width=True)

    # ===============================
    # TABELA DE APOIO
    # ===============================
    st.markdown("### Tabela de apoio – Ponto de Equilíbrio (MM 12M)")

    tabela_pe = pe_mensal[
        [
            "Ano_Mes",
            "Receita_MM12",
            "Custos_Variaveis_MM12",
            "Despesas_Fixas_MM12",
            "Margem_Contribuicao_MM12",
            "MC_percentual_MM12",
            "Ponto_Equilibrio_MM12",
            "Folga_MM12"
        ]
    ].copy()

    tabela_pe["Ano_Mes"] = tabela_pe["Ano_Mes"].dt.strftime("%m/%Y")

    st.dataframe(
        tabela_pe.style.format({
            "Receita_MM12": "R$ {:,.2f} mil",
            "Custos_Variaveis_MM12": "R$ {:,.2f} mil",
            "Despesas_Fixas_MM12": "R$ {:,.2f} mil",
            "Margem_Contribuicao_MM12": "R$ {:,.2f} mil",
            "MC_percentual_MM12": "{:,.2%}",
            "Ponto_Equilibrio_MM12": "R$ {:,.2f} mil",
            "Folga_MM12": "R$ {:,.2f} mil"
        }),
        use_container_width=True,
        height=350
    )

# =========================================================
# GRÁFICO – NCG GERENCIAL (BASE: MÉDIA MÓVEL 12M)
# =========================================================
    st.subheader("🏦 NCG Gerencial Estimada (Base: Média Móvel 12M)")

    if "Emissão" not in df.columns or "Baixa" not in df.columns:
        st.warning("Para calcular a NCG estimada, a base precisa ter as colunas 'Emissão' e 'Baixa'.")
    else:
        base_ncg = df.copy()

        base_ncg["Emissão"] = pd.to_datetime(base_ncg["Emissão"], errors="coerce")
        base_ncg["Baixa"] = pd.to_datetime(base_ncg["Baixa"], errors="coerce")
        base_ncg["Ano_Mes"] = base_ncg["Baixa"].dt.to_period("M").dt.to_timestamp()

        # Prazo em dias entre emissão e baixa
        base_ncg["Prazo_Dias"] = (base_ncg["Baixa"] - base_ncg["Emissão"]).dt.days

        # Limpeza mínima para evitar distorções absurdas
        base_ncg.loc[
            (base_ncg["Prazo_Dias"] < 0) | (base_ncg["Prazo_Dias"] > 365),
            "Prazo_Dias"
        ] = np.nan

        # -----------------------------
        # RECEITA LÍQUIDA MENSAL
        # -----------------------------
        receita_bruta_mensal = (
            base_ncg[base_ncg["Grupo_DRE"] == "Receita Bruta"]
            .groupby("Ano_Mes", as_index=False)["Composição"]
            .sum()
            .rename(columns={"Composição": "Receita_Bruta"})
        )

        deducoes_mensal = (
            base_ncg[base_ncg["Grupo_DRE"] == "Deduções"]
            .groupby("Ano_Mes", as_index=False)["Composição"]
            .sum()
            .rename(columns={"Composição": "Deducoes"})
        )

        receita_liquida_mensal = receita_bruta_mensal.merge(
            deducoes_mensal, on="Ano_Mes", how="left"
        )
        receita_liquida_mensal["Deducoes"] = receita_liquida_mensal["Deducoes"].fillna(0)
        receita_liquida_mensal["Receita_Liquida"] = (
            receita_liquida_mensal["Receita_Bruta"] - receita_liquida_mensal["Deducoes"]
        )

        # -----------------------------
        # CUSTOS + DESPESAS OPERACIONAIS MENSAIS
        # -----------------------------
        custos_despesas_mensal = (
            base_ncg[
                base_ncg["Grupo_DRE"].isin(["Custos dos Serviços", "Despesas Operacionais"])
            ]
            .groupby("Ano_Mes", as_index=False)["Composição"]
            .sum()
            .rename(columns={"Composição": "Custos_Despesas_Operacionais"})
        )

        # -----------------------------
        # PMR – PRAZO MÉDIO DE RECEBIMENTO
        # -----------------------------
        pmr_mensal = (
            base_ncg[
                (base_ncg["Grupo_DRE"] == "Receita Bruta") &
                (base_ncg["Prazo_Dias"].notna())
            ]
            .groupby("Ano_Mes")
            .apply(lambda x: np.average(x["Prazo_Dias"], weights=np.abs(x["Composição"])))
            .reset_index(name="PMR")
        )

        # -----------------------------
        # PMP – PRAZO MÉDIO DE PAGAMENTO
        # -----------------------------
        pmp_mensal = (
            base_ncg[
                (base_ncg["Grupo_DRE"].isin(["Custos dos Serviços", "Despesas Operacionais"])) &
                (base_ncg["Prazo_Dias"].notna())
            ]
            .groupby("Ano_Mes")
            .apply(lambda x: np.average(x["Prazo_Dias"], weights=np.abs(x["Composição"])))
            .reset_index(name="PMP")
        )

        # -----------------------------
        # BASE FINAL MENSAL
        # -----------------------------
        ncg_df = receita_liquida_mensal.merge(
            custos_despesas_mensal, on="Ano_Mes", how="outer"
        ).merge(
            pmr_mensal, on="Ano_Mes", how="left"
        ).merge(
            pmp_mensal, on="Ano_Mes", how="left"
        ).sort_values("Ano_Mes")

        ncg_df["Receita_Liquida"] = ncg_df["Receita_Liquida"].fillna(0)
        ncg_df["Custos_Despesas_Operacionais"] = ncg_df["Custos_Despesas_Operacionais"].fillna(0)

        # Converter para R$ mil
        ncg_df["Receita_Liquida_R$mil"] = ncg_df["Receita_Liquida"] / 1000
        ncg_df["Custos_Despesas_R$mil"] = ncg_df["Custos_Despesas_Operacionais"] / 1000

        # -----------------------------
        # MÉDIAS MÓVEIS 12M
        # -----------------------------
        ncg_df["Receita_Liquida_MM12"] = (
            ncg_df["Receita_Liquida_R$mil"]
            .rolling(window=12, min_periods=1)
            .mean()
        )

        ncg_df["Custos_Despesas_MM12"] = (
            ncg_df["Custos_Despesas_R$mil"]
            .rolling(window=12, min_periods=1)
            .mean()
        )

        ncg_df["PMR_MM12"] = (
            ncg_df["PMR"]
            .rolling(window=12, min_periods=1)
            .mean()
        )

        ncg_df["PMP_MM12"] = (
            ncg_df["PMP"]
            .rolling(window=12, min_periods=1)
            .mean()
        )

        # -----------------------------
        # NCG ESTIMADA
        # -----------------------------
        ncg_df["Clientes_Estimado_MM12"] = (
            (ncg_df["Receita_Liquida_MM12"] / 30) * ncg_df["PMR_MM12"]
        )

        ncg_df["Fornecedores_Estimado_MM12"] = (
            (ncg_df["Custos_Despesas_MM12"] / 30) * ncg_df["PMP_MM12"]
        )

        ncg_df["NCG_MM12"] = (
            ncg_df["Clientes_Estimado_MM12"] - ncg_df["Fornecedores_Estimado_MM12"]
        )

        ncg_df["Status_NCG"] = np.where(
            ncg_df["NCG_MM12"] >= 0,
            "NCG Positiva",
            "NCG Negativa"
        )

        # -----------------------------
        # CARDS
        # -----------------------------
        col_ncg1, col_ncg2, col_ncg3 = st.columns(3)

        ncg_valid = ncg_df.dropna(subset=["NCG_MM12"]).copy()

        if not ncg_valid.empty:
            ultima_linha_ncg = ncg_valid.sort_values("Ano_Mes").iloc[-1]

            col_ncg1.metric(
                "NCG estimada 12M",
                f"R$ {ultima_linha_ncg['NCG_MM12']:,.2f} mil"
            )
            col_ncg2.metric(
                "PMR médio 12M",
                f"{ultima_linha_ncg['PMR_MM12']:,.1f} dias"
            )
            col_ncg3.metric(
                "PMP médio 12M",
                f"{ultima_linha_ncg['PMP_MM12']:,.1f} dias"
            )

        # -----------------------------
        # GRÁFICO PRINCIPAL
        # -----------------------------
        grafico_ncg = px.line(
            ncg_df,
            x="Ano_Mes",
            y=["Clientes_Estimado_MM12", "Fornecedores_Estimado_MM12", "NCG_MM12"],
            markers=True,
            labels={
                "Ano_Mes": "Mês",
                "value": "Valor (R$ mil)",
                "variable": "Indicador"
            }
        )

        grafico_ncg.update_layout(legend_title_text="Indicador")
        grafico_ncg.update_xaxes(tickformat="%m/%Y")

        st.plotly_chart(grafico_ncg, use_container_width=True)
        st.subheader("Principais Pontos de Destaque")

        st.markdown(
        """
        <div style="text-align: justify; font-size: 22px; line-height: 1.3;">

        1. Necessidade de capital de giro positiva, indicando consumo de caixa operacional  
        A análise evidencia que a operação demanda capital de giro para sustentação de suas atividades, refletindo um descasamento entre os prazos de recebimento e pagamento. Esse comportamento indica consumo de caixa operacional e exige atenção quanto à disponibilidade de recursos para manutenção das operações.

        <br>

        2. Pressão sobre o caixa decorrente da dinâmica operacional  
        A relação entre receita, custos e prazos operacionais sugere que parte do resultado gerado pode estar sendo absorvida pela necessidade de financiamento da operação. Esse cenário reforça a importância de monitoramento contínuo da NCG, especialmente em contextos de crescimento.

        <br>

        3. Potencial de melhoria via gestão de prazos operacionais  
        A NCG está diretamente relacionada aos prazos médios de recebimento e pagamento. Assim, ações voltadas à redução do prazo de recebimento ou à ampliação do prazo de pagamento podem contribuir para redução da necessidade de capital de giro, liberando recursos e aumentando a eficiência financeira.

        </div>
        """,
        unsafe_allow_html=True
        )
        # -----------------------------
        # GRÁFICO DE BARRAS DA NCG
        # -----------------------------
        st.markdown("### Evolução da NCG Estimada (MM 12M)")

        grafico_ncg_barra = px.bar(
            ncg_df,
            x="Ano_Mes",
            y="NCG_MM12",
            color="Status_NCG",
            labels={
                "Ano_Mes": "Mês",
                "NCG_MM12": "NCG Estimada (R$ mil)",
                "Status_NCG": "Status"
            }
        )

        grafico_ncg_barra.update_xaxes(tickformat="%m/%Y")

        st.plotly_chart(grafico_ncg_barra, use_container_width=True)

        # -----------------------------
        # TABELA DE APOIO
        # -----------------------------
        st.markdown("### Tabela de apoio – NCG Gerencial (MM 12M)")

        tabela_ncg = ncg_df[
            [
                "Ano_Mes",
                "Receita_Liquida_MM12",
                "Custos_Despesas_MM12",
                "PMR_MM12",
                "PMP_MM12",
                "Clientes_Estimado_MM12",
                "Fornecedores_Estimado_MM12",
                "NCG_MM12"
            ]
        ].copy()

        tabela_ncg["Ano_Mes"] = tabela_ncg["Ano_Mes"].dt.strftime("%m/%Y")

        st.dataframe(
            tabela_ncg.style.format({
                "Receita_Liquida_MM12": "R$ {:,.2f} mil",
                "Custos_Despesas_MM12": "R$ {:,.2f} mil",
                "PMR_MM12": "{:,.1f} dias",
                "PMP_MM12": "{:,.1f} dias",
                "Clientes_Estimado_MM12": "R$ {:,.2f} mil",
                "Fornecedores_Estimado_MM12": "R$ {:,.2f} mil",
                "NCG_MM12": "R$ {:,.2f} mil"
            }),
            use_container_width=True,
            height=350
        )
    st.subheader("Conclusões")

    st.markdown(
    """
    <div style="text-align: justify; font-size: 22px; line-height: 1.3;">

    • A companhia apresenta capacidade de geração de resultado operacional positivo, evidenciando uma estrutura de negócio funcional e aderente ao seu nível de atividade.

    <br>

    • A operação encontra-se posicionada próxima ao ponto de equilíbrio, com folga operacional moderada, o que indica sensibilidade do resultado a variações de receita e custos.

    <br>

    • A estrutura de custos e despesas possui peso relevante sobre a receita, reforçando a necessidade de controle contínuo e ganhos de eficiência operacional para sustentação das margens.

    <br>

    • A necessidade de capital de giro é positiva, indicando consumo de caixa para financiamento da operação, especialmente em função da dinâmica entre prazos de recebimento e pagamento.

    <br>

    • O crescimento da operação tende a ampliar a demanda por capital de giro, exigindo planejamento financeiro adequado para evitar pressão sobre a liquidez.

    <br>

    • Há oportunidade de melhoria na eficiência financeira por meio da gestão de prazos operacionais, com potencial de liberação de caixa via redução do ciclo financeiro.

    <br>

    • Incrementos de receita, quando acompanhados de controle de custos, tendem a gerar ganho relevante de resultado, caracterizando potencial de alavancagem operacional.

    <br>

    • Recomenda-se acompanhamento contínuo dos indicadores de margem, ponto de equilíbrio e capital de giro, garantindo maior previsibilidade e segurança na gestão financeira.
    
    <br>

    <b> Equipe FMCE </b>
    </div>
    """,
    unsafe_allow_html=True
    )

# ===============================
# TABELAS
# ===============================
elif menu == "Tabelas":
    st.subheader("📋 Contas Pagas")
    st.dataframe(df1, use_container_width=True)

    st.subheader("📋 Recebimentos")
    st.dataframe(df2, use_container_width=True)

    st.subheader("📋 Base Geral")
    st.dataframe(df, use_container_width=True)




