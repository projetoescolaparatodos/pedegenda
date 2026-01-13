# Agenda de Visitas (Excel + Web)

Projeto simples pra organizar visitas/pendências:

- Gera uma planilha Excel (`Agenda_Visitas.xlsx`) com estilo e cores.
- App web local (Streamlit) com login, progresso por etapas e "missões" por estabelecimento.

## Requisitos

- Python 3

## Instalação

```bash
pip install -r requirements.txt
```

> Se você estiver usando a `.venv` deste projeto, rode os comandos com o Python da venv.

## Gerar planilha Excel

```bash
python gerar_agenda.py
```

Vai criar/atualizar `Agenda_Visitas.xlsx`.

## Rodar o app web

```bash
python -m streamlit run app.py
```

Abre no navegador (normalmente): `http://localhost:8501`

### Login

Usuários:
- `Neo`
- `Frodo`
- `Troio`

Senha (para todos): `pedeja2025`

## Dados

O app salva em `dados.json` (arquivo local). Por padrão, ele **não** está versionado no git.
