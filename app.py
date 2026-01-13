import json
import os
import uuid
from datetime import datetime

import pandas as pd
import streamlit as st

# Usuários hard-coded (simples / uso interno)
USUARIOS = {
    "Neo": "pedeja2025",
    "Frodo": "pedeja2025",
    "Troio": "pedeja2025",
}

DATA_FILE = "dados.json"

ETAPAS_PADRAO = ["Captação", "Cadastro Produtos", "Vinculação Conta"]


def _rerun() -> None:
    # Compatibilidade entre versões
    if hasattr(st, "rerun"):
        st.rerun()
    st.experimental_rerun()


def load_data() -> list[dict]:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        data = migrate_data(data)
        save_data(data)
        return data

    initial_data = [
        {
            "local": "Róbson",
            "data_hora": "13/01/2026 - Manhã",
            "etapas": {k: False for k in ETAPAS_PADRAO},
            "status": "Pendente",
            "prioridade": "",
            "responsavel": "",
            "notas": "",
            "ultima_atualizacao": "",
        },
        {
            "local": "Amazonina",
            "data_hora": "13/01/2026 - Manhã",
            "etapas": {k: False for k in ETAPAS_PADRAO},
            "status": "Pendente",
            "prioridade": "",
            "responsavel": "",
            "notas": "",
            "ultima_atualizacao": "",
        },
        {
            "local": "Bom Gosto",
            "data_hora": "13/01/2026 - Durante o dia",
            "etapas": {k: False for k in ETAPAS_PADRAO},
            "status": "Pendente",
            "prioridade": "",
            "responsavel": "",
            "notas": "",
            "ultima_atualizacao": "",
        },
        {
            "local": "Açaí do Vizinho da Esquina",
            "data_hora": "13/01/2026 - Durante o dia",
            "etapas": {k: False for k in ETAPAS_PADRAO},
            "status": "Pendente",
            "prioridade": "",
            "responsavel": "",
            "notas": "",
            "ultima_atualizacao": "",
        },
        {
            "local": "Granja",
            "data_hora": "15/01/2026 - Durante o dia",
            "etapas": {k: False for k in ETAPAS_PADRAO},
            "status": "Pendente",
            "prioridade": "",
            "responsavel": "",
            "notas": "",
            "ultima_atualizacao": "",
        },
        {
            "local": "Açougue do Marquinhos",
            "data_hora": "15/01/2026 - Fim do dia",
            "etapas": {k: False for k in ETAPAS_PADRAO},
            "status": "Pendente",
            "prioridade": "",
            "responsavel": "",
            "notas": "",
            "ultima_atualizacao": "",
        },
        {
            "local": "Adelson dos Salgados",
            "data_hora": "16/01/2026 - 07:30",
            "etapas": {k: False for k in ETAPAS_PADRAO},
            "status": "Pendente",
            "prioridade": "",
            "responsavel": "",
            "notas": "",
            "ultima_atualizacao": "",
        },
        {
            "local": "Padeiro (pra roça)",
            "data_hora": "A Definir",
            "etapas": {k: False for k in ETAPAS_PADRAO},
            "status": "Pendente",
            "prioridade": "",
            "responsavel": "",
            "notas": "",
            "ultima_atualizacao": "",
        },
        {
            "local": "Teresinha",
            "data_hora": "A Definir",
            "etapas": {k: False for k in ETAPAS_PADRAO},
            "status": "Pendente",
            "prioridade": "",
            "responsavel": "",
            "notas": "",
            "ultima_atualizacao": "",
        },
        {
            "local": "Valéria do Nunes",
            "data_hora": "A Definir",
            "etapas": {k: False for k in ETAPAS_PADRAO},
            "status": "Pendente",
            "prioridade": "",
            "responsavel": "",
            "notas": "",
            "ultima_atualizacao": "",
        },
        {
            "local": "Taila da Drogaria Vitória",
            "data_hora": "A Definir",
            "etapas": {k: False for k in ETAPAS_PADRAO},
            "status": "Pendente",
            "prioridade": "",
            "responsavel": "",
            "notas": "",
            "ultima_atualizacao": "",
        },
        {
            "local": "Açougue 1 (nome esquecido)",
            "data_hora": "A Definir",
            "etapas": {k: False for k in ETAPAS_PADRAO},
            "status": "Pendente",
            "prioridade": "",
            "responsavel": "",
            "notas": "",
            "ultima_atualizacao": "",
        },
    ]

    initial_data = migrate_data(initial_data)
    save_data(initial_data)
    return initial_data


def save_data(data: list[dict]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def migrate_data(data: list[dict]) -> list[dict]:
    """Migra/normaliza dados para manter compatibilidade entre versões do app."""

    for idx, item in enumerate(data):
        if not isinstance(item, dict):
            continue

        if not item.get("id"):
            item["id"] = str(uuid.uuid4())

        if "etapas" not in item or not isinstance(item.get("etapas"), dict):
            item["etapas"] = {k: False for k in ETAPAS_PADRAO}

        # Garantir que todas as etapas padrão existam
        for etapa in ETAPAS_PADRAO:
            item["etapas"].setdefault(etapa, False)

        item.setdefault("local", f"Estabelecimento {idx + 1}")
        item.setdefault("data_hora", "A Definir")
        item.setdefault("status", _status_from_etapas(item["etapas"]))
        item.setdefault("prioridade", "")
        item.setdefault("responsavel", "")
        item.setdefault("notas", "")
        item.setdefault("ultima_atualizacao", "")

        # Missões (pendências/visitas extras) - não entram no progresso geral
        if "missoes" not in item or not isinstance(item.get("missoes"), list):
            item["missoes"] = []
        for m in item["missoes"]:
            if not isinstance(m, dict):
                continue
            if not m.get("id"):
                m["id"] = str(uuid.uuid4())
            m.setdefault("titulo", "")
            m.setdefault("data_hora", "A Definir")
            m.setdefault("status", "Pendente")
            m.setdefault("notas", "")
            m.setdefault("ultima_atualizacao", "")

    return data


def _parse_datahora_sort_key(value: str, original_index: int) -> tuple[int, str, int, int]:
    value = (value or "").strip()
    if not value or value.lower().startswith("a definir"):
        return (1, "9999-12-31", 9999, original_index)

    if " - " not in value:
        return (0, "9999-12-31", 9999, original_index)

    date_part, period_part = value.split(" - ", 1)
    date_part = date_part.strip()
    period_part = period_part.strip().lower()

    try:
        date_iso = datetime.strptime(date_part, "%d/%m/%Y").date().isoformat()
    except ValueError:
        return (0, "9999-12-31", 9999, original_index)

    # Horários aproximados
    if ":" in period_part:
        try:
            hh, mm = period_part.split(":", 1)
            minutes = int(hh) * 60 + int(mm)
        except ValueError:
            minutes = 12 * 60
    else:
        map_minutes = {
            "manhã": 9 * 60,
            "durante o dia": 13 * 60,
            "fim do dia": 18 * 60,
        }
        minutes = map_minutes.get(period_part, 12 * 60)

    return (0, date_iso, minutes, original_index)


def _status_from_etapas(etapas: dict) -> str:
    if all(etapas.values()):
        return "Concluído"
    if any(etapas.values()):
        return "Em andamento"
    return "Pendente"


def _color_badge(text: str) -> str:
    t = (text or "").strip().lower()
    if t in {"concluído", "concluido"}:
        return "✅ Concluído"
    if t in {"em andamento", "andamento"}:
        return "🟡 Em andamento"
    if t == "pendente":
        return "🔴 Pendente"
    return text


def login_ui() -> None:
    st.title("Login — Agenda de Visitas")
    user = st.selectbox("Usuário", list(USUARIOS.keys()))
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar", use_container_width=True):
        if senha == USUARIOS.get(user):
            st.session_state.logged_in = True
            st.session_state.user = user
            _rerun()
        else:
            st.error("Senha incorreta.")


def main_ui() -> None:
    data = load_data()

    # Ordenar (data definida primeiro)
    indexed = list(enumerate(data))
    indexed.sort(
        key=lambda pair: _parse_datahora_sort_key(pair[1].get("data_hora", ""), pair[0])
    )
    data = [row for _, row in indexed]

    st.title("Agenda de Visitas")

    with st.sidebar:
        st.write(f"Logado como: **{st.session_state.user}**")
        if st.button("Sair", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            _rerun()

    # Progresso
    meta_estabelecimentos = 20
    etapas_por_estab = len(ETAPAS_PADRAO)
    meta_total_etapas = meta_estabelecimentos * etapas_por_estab

    etapas_concluidas = sum(sum(item.get("etapas", {}).values()) for item in data)
    progresso = (etapas_concluidas / meta_total_etapas) if meta_total_etapas > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Etapas concluídas", f"{etapas_concluidas}/{meta_total_etapas}")
    concluidos = sum(1 for item in data if item.get("status") == "Concluído")
    col2.metric("Estabelecimentos concluídos", f"{concluidos}/{meta_estabelecimentos}")
    col3.metric("Progresso", f"{progresso * 100:.1f}%")
    st.progress(progresso)

    st.divider()

    changed_any = False
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")

    for item in data:
        item_changed = False
        est_id = item.get("id", "")
        local = item.get("local", "")
        data_hora = item.get("data_hora", "")
        status = item.get("status", "Pendente")

        header = f"{local} — {data_hora} — {_color_badge(status)}"
        with st.expander(header, expanded=False):
            left, right = st.columns([2, 1])

            with left:
                # Etapas
                etapas = item.get("etapas", {k: False for k in ETAPAS_PADRAO})
                for etapa in ETAPAS_PADRAO:
                    key = f"etapa_{est_id}_{etapa}"
                    novo_valor = st.checkbox(etapa, value=bool(etapas.get(etapa, False)), key=key)
                    if novo_valor != bool(etapas.get(etapa, False)):
                        etapas[etapa] = novo_valor
                        item_changed = True

                # Notas
                notas_key = f"notas_{est_id}"
                novas_notas = st.text_area("Notas", value=item.get("notas", ""), key=notas_key)
                if novas_notas != item.get("notas", ""):
                    item["notas"] = novas_notas
                    item_changed = True

                st.markdown("---")
                st.subheader("Missões (pendências/visitas extras)")

                missoes = item.get("missoes", [])
                # Ordenar missões por data/hora, mantendo ordem em empates
                indexed_m = list(enumerate(missoes))
                indexed_m.sort(
                    key=lambda pair: _parse_datahora_sort_key(
                        pair[1].get("data_hora", ""), pair[0]
                    )
                )
                missoes_sorted = [m for _, m in indexed_m]

                if not missoes_sorted:
                    st.caption("Nenhuma missão cadastrada ainda.")

                for m in missoes_sorted:
                    mid = m.get("id", "")
                    cols = st.columns([1, 3, 2, 4])

                    feito = (m.get("status", "Pendente") or "Pendente").strip().lower() in {
                        "feito",
                        "concluído",
                        "concluido",
                    }
                    novo_feito = cols[0].checkbox(
                        "Feito",
                        value=feito,
                        key=f"missao_feito_{est_id}_{mid}",
                    )
                    novo_titulo = cols[1].text_input(
                        "Missão",
                        value=m.get("titulo", ""),
                        key=f"missao_titulo_{est_id}_{mid}",
                        label_visibility="collapsed",
                    )
                    novo_data_m = cols[2].text_input(
                        "Data/Hora",
                        value=m.get("data_hora", "A Definir"),
                        key=f"missao_data_{est_id}_{mid}",
                        label_visibility="collapsed",
                    )
                    cols[3].caption(
                        f"Status: {'Feito' if novo_feito else 'Pendente'} · {m.get('ultima_atualizacao', '') or '—'}"
                    )

                    novo_status = "Feito" if novo_feito else "Pendente"
                    if (
                        novo_status != m.get("status")
                        or novo_titulo != m.get("titulo")
                        or novo_data_m != m.get("data_hora")
                    ):
                        m["status"] = novo_status
                        m["titulo"] = novo_titulo
                        m["data_hora"] = novo_data_m
                        m["ultima_atualizacao"] = f"Por {st.session_state.user} em {agora}"
                        item_changed = True

                with st.form(f"add_missao_{est_id}"):
                    c1, c2 = st.columns([3, 2])
                    nova_missao_titulo = c1.text_input("Nome da missão")
                    nova_missao_data = c2.text_input(
                        "Data/Hora",
                        placeholder="Ex: 18/01/2026 - 14:00 ou A Definir",
                    )
                    add_m = st.form_submit_button("Adicionar missão")
                    if add_m:
                        if not nova_missao_titulo.strip():
                            st.error("Informe o nome da missão.")
                        else:
                            item.setdefault("missoes", []).append(
                                {
                                    "id": str(uuid.uuid4()),
                                    "titulo": nova_missao_titulo.strip(),
                                    "data_hora": (nova_missao_data or "A Definir").strip(),
                                    "status": "Pendente",
                                    "notas": "",
                                    "ultima_atualizacao": f"Por {st.session_state.user} em {agora}",
                                }
                            )
                            item_changed = True

            with right:
                prioridade = st.selectbox(
                    "Prioridade",
                    options=["", "Alta", "Média", "Baixa"],
                    index=["", "Alta", "Média", "Baixa"].index(item.get("prioridade", "") if item.get("prioridade", "") in {"", "Alta", "Média", "Baixa"} else ""),
                    key=f"prioridade_{est_id}",
                )
                if prioridade != item.get("prioridade", ""):
                    item["prioridade"] = prioridade
                    item_changed = True

                responsavel = st.text_input(
                    "Responsável", value=item.get("responsavel", ""), key=f"resp_{est_id}"
                )
                if responsavel != item.get("responsavel", ""):
                    item["responsavel"] = responsavel
                    item_changed = True

                st.caption(f"Última atualização: {item.get('ultima_atualizacao', '') or '—'}")

            # Atualizar status automaticamente
            item["etapas"] = etapas
            novo_status = _status_from_etapas(etapas)
            if novo_status != item.get("status"):
                item["status"] = novo_status
                item_changed = True

            if item_changed:
                item["ultima_atualizacao"] = f"Por {st.session_state.user} em {agora}"

        changed_any = changed_any or item_changed

    st.divider()

    st.subheader("Adicionar novo estabelecimento")
    with st.form("add_form", clear_on_submit=True):
        novo_local = st.text_input("Local")
        novo_data_hora = st.text_input("Data/Hora", placeholder="Ex: 18/01/2026 - Manhã ou A Definir")
        novo_prioridade = st.selectbox("Prioridade", ["", "Alta", "Média", "Baixa"])
        novo_responsavel = st.text_input("Responsável")
        submitted = st.form_submit_button("Adicionar")

        if submitted:
            if not novo_local.strip():
                st.error("Informe o Local.")
            else:
                data.append(
                    {
                        "id": str(uuid.uuid4()),
                        "local": novo_local.strip(),
                        "data_hora": (novo_data_hora or "A Definir").strip(),
                        "etapas": {k: False for k in ETAPAS_PADRAO},
                        "status": "Pendente",
                        "prioridade": novo_prioridade,
                        "responsavel": novo_responsavel.strip(),
                        "notas": "",
                        "ultima_atualizacao": f"Por {st.session_state.user} em {agora}",
                        "missoes": [],
                    }
                )
                save_data(data)
                st.success("Adicionado!")
                _rerun()

    if changed_any:
        save_data(data)
        st.toast("Salvo.")

    st.subheader("Visão geral")
    df = pd.DataFrame(
        [
            {
                "Local": i.get("local", ""),
                "Data/Hora": i.get("data_hora", ""),
                "Prioridade": i.get("prioridade", ""),
                "Responsável": i.get("responsavel", ""),
                "Status": i.get("status", ""),
                "Última atualização": i.get("ultima_atualizacao", ""),
            }
            for i in data
        ]
    )
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.subheader("Panorama geral — Missões")
    all_missoes: list[dict] = []
    for item in data:
        local = item.get("local", "")
        for m in item.get("missoes", []) or []:
            all_missoes.append(
                {
                    "Local": local,
                    "Missão": m.get("titulo", ""),
                    "Data/Hora": m.get("data_hora", ""),
                    "Status": m.get("status", ""),
                    "Última atualização": m.get("ultima_atualizacao", ""),
                }
            )

    if not all_missoes:
        st.caption("Nenhuma missão cadastrada ainda.")
    else:
        indexed_pm = list(enumerate(all_missoes))
        indexed_pm.sort(
            key=lambda pair: _parse_datahora_sort_key(pair[1].get("Data/Hora", ""), pair[0])
        )
        all_missoes = [row for _, row in indexed_pm]
        dfm = pd.DataFrame(all_missoes)
        st.dataframe(dfm, use_container_width=True, hide_index=True)


def main() -> None:
    st.set_page_config(page_title="Agenda de Visitas", layout="wide")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "user" not in st.session_state:
        st.session_state.user = None

    if not st.session_state.logged_in:
        login_ui()
    else:
        main_ui()


if __name__ == "__main__":
    main()
