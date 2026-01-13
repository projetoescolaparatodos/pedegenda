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

### Deploy no Render (sem banco, com persistência)

Para manter os dados sem usar banco, use um **Persistent Disk** e a variável `DATA_DIR`.

- Crie um **Web Service** apontando para este repo.
- Adicione um **Persistent Disk** e monte em `/var/data`.
- Configure a env var: `DATA_DIR=/var/data`
- Start command (Render):

```bash
python -m streamlit run app.py --server.address 0.0.0.0 --server.port $PORT --server.headless true --browser.gatherUsageStats false
```

Assim o `dados.json` fica em `/var/data/dados.json` (persistente).
