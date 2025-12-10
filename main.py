import streamlit as st
import requests
import pandas as pd
from io import BytesIO
from babel.numbers import format_decimal


def titulo_header(
    titulo: str,
    subtitulo: str | None = None,
    *,
    icon: str | None = "📊",
    badge: str | None = None,
    align: str = "center",          # "left" | "center" | "right"
    theme: str = "dark",            # "dark" | "light"
    accent: str = "#22d3ee",
    bg_from: str = "#0c1c2a",
    bg_to: str = "#003366",
    pad_y: int = 18,                # padding vertical em px
    show_divider: bool = True,
):
    """
    Renderiza um cabeçalho estilizado usando st.html().
    Exemplo:
        titulo_header("ANÁLISE DE VENDAS", "Período: Nov/2025", icon="📈", badge="Meta +12%")
    """
    is_center = (align == "center")
    justify = {"left": "flex-start", "center": "center", "right": "flex-end"}.get(align, "center")

    # Tema
    if theme == "light":
        txt = "#0b1a29"
        sub = "rgba(11,26,41,.75)"
        card_from, card_to = "#f5f9ff", "#e9f2ff"
        glow = "rgba(34,211,238,.35)"
    else:
        txt = "#eaf2ff"
        sub = "rgba(234,242,255,.75)"
        card_from, card_to = bg_from, bg_to
        glow = "rgba(34,211,238,.25)"

    # Divider opcional
    divider_html = f"""
        <div style="
            width: 100%;
            height: 2px;
            margin-top: 12px;
            background: linear-gradient(90deg, transparent, {accent}, transparent);
            opacity: .8;"></div>
    """ if show_divider else ""

    # Badge opcional
    badge_html = f"""
        <span class="hdr-badge">{badge}</span>
    """ if badge else ""

    # Subtítulo opcional
    sub_html = f"""
        <div class="hdr-sub">{subtitulo}</div>
    """ if subtitulo else ""

    # Ícone opcional
    icon_html = f"""
        <div class="hdr-icon">{icon}</div>
    """ if icon else ""

    st.html(f"""
    <section class="hdr-wrap">
        <style>
            .hdr-wrap {{
                width: 100%;
            }}
            .hdr {{
                --accent: {accent};
                --txt: {txt};
                --sub: {sub};
                --glow: {glow};

                background: linear-gradient(135deg, {card_from}, {card_to});
                border: 1px solid rgba(255,255,255,.08);
                border-radius: 18px;
                padding: {pad_y}px clamp(12px, 3vw, 28px);
                display: flex;
                align-items: center;
                justify-content: {justify};
                gap: clamp(10px, 2vw, 16px);
                box-shadow: 0 10px 30px rgba(0,0,0,.22), 0 0 0 1px rgba(255,255,255,.05) inset;
                position: relative;
                overflow: hidden;
            }}
            /* glow/acento suave ao fundo */
            .hdr::after {{
                content: "";
                position: absolute;
                inset: -20%;
                background: radial-gradient(60% 60% at 20% 10%, var(--glow), transparent 60%);
                pointer-events: none;
            }}

            .hdr-left {{
                display: flex;
                align-items: center;
                gap: clamp(10px, 2vw, 16px);
                max-width: 1200px;
                width: 100%;
                justify-content: {justify};
                text-align: {"center" if is_center else "left"};
            }}

            .hdr-icon {{
                font-size: clamp(22px, 4vw, 34px);
                filter: drop-shadow(0 2px 8px rgba(0,0,0,.25));
            }}

            .hdr-texts {{
                display: flex;
                flex-direction: column;
                gap: 4px;
                min-width: 0;
            }}

            .hdr-title {{
                color: var(--txt);
                font-weight: 800;
                letter-spacing: .3px;
                line-height: 1.1;
                /* responsivo: de 22px a 40px */
                font-size: clamp(22px, 2.6vw, 40px);
                text-shadow: 0 1px 0 rgba(0,0,0,.15);
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }}

            .hdr-sub {{
                color: var(--sub);
                font-weight: 500;
                line-height: 1.25;
                font-size: clamp(12px, 1.3vw, 16px);
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }}

            .hdr-badge {{
                display: inline-flex;
                align-items: center;
                gap: 6px;
                padding: 6px 10px;
                font-size: clamp(10px, 1.2vw, 12px);
                border-radius: 999px;
                background: linear-gradient(135deg, rgba(34,211,238,.15), rgba(34,211,238,.05));
                border: 1px solid rgba(34,211,238,.35);
                color: var(--txt);
                backdrop-filter: blur(4px);
                box-shadow: inset 0 0 0 1px rgba(255,255,255,.04);
            }}

            .hdr-accent-bar {{
                position: absolute;
                bottom: 0;
                left: 0;
                width: 100%;
                height: 3px;
                background: linear-gradient(90deg, transparent, var(--accent), transparent);
                opacity: .9;
            }}

            @media (max-width: 640px) {{
                .hdr {{
                    border-radius: 14px;
                }}
                .hdr-title {{
                    letter-spacing: .2px;
                }}
            }}
        </style>

        <div class="hdr">
            <div class="hdr-left">
                {icon_html}
                <div class="hdr-texts">
                    <div class="hdr-title">{titulo}</div>
                    {sub_html}
                </div>
                {badge_html}
            </div>
            <div class="hdr-accent-bar"></div>
        </div>

        {divider_html}
    </section>
    """)


def dados(dt_ini: str, dt_fim: str) -> pd.DataFrame:
    query = f"""
        select 
            m.CODIGO,
            m.HISTORICO,
            SUM(b.VALOR) AS VALOR,
            b.DATADEPAGAMENTO AS DATA,
            b.COMPETENCIA,
            m.PAR_EMPRESA AS FILIAL,
            m.CONTADOPLANO AS CONTA,
            c.NOMEDACONTA AS DESCRICAO_CONTA,
            c.CODCONT AS CT_CONTAB
            
            from CAD_MVTO as m 

            join BX_PEPAG as b on m.CODIGO = b.COD_BANCARIO
            join PUBLICO_ELETRO.dbo.CAD_PLAN as c on m.CONTADOPLANO = c.CODIGO
            where m.CODIGODACONTA = 206 and b.DATADEPAGAMENTO BETWEEN '{dt_ini}' and '{dt_fim}'
        
            group by m.CODIGO, m.HISTORICO, b.DATADEPAGAMENTO, m.VALOR, b.COMPETENCIA, m.CONTADOPLANO, c.NOMEDACONTA, c.CODCONT, m.PAR_EMPRESA

        """
    
    try:    
        response = requests.post(
                'http://10.1.8.118:9000/sql_server/query',
                json={"sql": query}
            )

        response.raise_for_status()
        data = response.json()
    
    except Exception as e:
        st.error("**Erro ao tentar conectar com o banco de dados...**")
        st.stop()
        
    return pd.DataFrame(data=data['rows'])

def to_excel_bytes(df_):
    buff = BytesIO()
    with pd.ExcelWriter(buff, engine="xlsxwriter") as writer:
        df_.to_excel(writer, index=False, sheet_name="Vendas")
    buff.seek(0)
    return buff.getvalue()

class App:
    def __init__(self):
        st.set_page_config(
            page_title="CONTAS A PAGAR",
            layout='wide',
            page_icon="💵"
        )
        
        if 'dt_ini' not in st.session_state:
            st.session_state.dt_ini = None
        if 'dt_fim' not in st.session_state:
            st.session_state.dt_fim = None
        if 'dados' not in st.session_state:
            st.session_state.dados = pd.DataFrame()
            st.session_state.filtrado = pd.DataFrame()
        if 'conta' not in st.session_state:
            st.session_state.conta = None
        if 'filial' not in st.session_state:
            st.session_state.filial = None
        if 'comp' not in st.session_state:
            st.session_state.comp = None
    
            
        
    def sidebar_(self):
        with st.sidebar:
            st.markdown("💳", width='stretch')
            st.html(
                '<h3 style="text-align: center">FILTROS</h3>',
                width='stretch'
            )
            with st.container(border=True, width='stretch'):
                st.session_state.dt_ini = st.date_input(label="*Data Inicio*", format="DD/MM/YYYY")
                st.session_state.dt_fim = st.date_input(label="*Data Final*", format="DD/MM/YYYY")
            
            
            if st.button("**CARREGAR**", width="stretch", key='bt_carregar'):
                st.session_state.dados = dados(
                    st.session_state.dt_ini,
                    st.session_state.dt_fim
                )
                
            if not st.session_state.dados.empty:
                with st.container(border=True, width='stretch'):
                    st.session_state.conta = st.multiselect(
                        label='Conta',
                        options=sorted(st.session_state.dados.CONTA.unique().tolist()),
                        placeholder='Selecionar conta(s)'
                    )
                    st.session_state.filial = st.multiselect(
                        label='Filial',
                        options=sorted(st.session_state.dados.FILIAL.unique().tolist()),
                        placeholder='Selecionar filial'
                    )
                    st.session_state.comp = st.multiselect(
                        label='Competência',
                        options=sorted(st.session_state.dados.COMPETENCIA.unique().tolist()),
                        placeholder='Selecionar competência'
                    )
                    
                if st.button("*FILTAR*", width="stretch", key='bt_filtro'):
                    mask = pd.Series(True, index=st.session_state.dados.index)
                    filtros = {
                        "CONTA": st.session_state.conta,
                        "FILIAL": st.session_state.filial,
                        "COMPETENCIA": st.session_state.comp
                        
                    }
                    for filtro, valor in filtros.items():
                        print(filtro, valor)
                        if valor:
                            mask &= (st.session_state.dados[filtro].isin(valor))
                        
                        print(mask)
                        st.session_state.filtrado = st.session_state.dados[mask].copy()
                        
                                      
    def run(self):
        self.sidebar_()

        titulo_header(
            "Fechamento da Fatura de Cartão Corporativo",
            icon=None
        )

        if not st.session_state.dados.empty:
            if st.session_state.filtrado.empty:
                df = st.session_state.dados.copy()
            else:
                df = st.session_state.filtrado.copy()
                
            df["DATA"] = pd.to_datetime(df["DATA"], errors="coerce").dt.date
            
            config_col = {
                "DATA": st.column_config.DateColumn(
                    "DATA",
                    format="DD/MM/YYYY"
                ),
                "VALOR": st.column_config.NumberColumn(
                    "VALOR",
                    format="%.2f"
                )
            }
            st.data_editor(
                data=df,
                width='stretch',
                height='stretch',
                hide_index=True,
                column_config=config_col
            )
            
            st.download_button(
                'EXCEL', data=to_excel_bytes(st.session_state.dados),
                file_name='FaturaCartao.xlsx',
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key='dwn_excel'
            )
            
            COL = st.columns(3)

            with COL[2]:
                st.markdown('*Total da Fatura*')
                titulo_header(
                    icon="💳",
                    titulo=format_decimal(df.VALOR.sum(), locale="pt_br", format="#,##0.00")
                )
                
            
            
if __name__ == "__main__":
    App().run()