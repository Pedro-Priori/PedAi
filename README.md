
-----

# 🛒 PedAI - Marketplace & Dashboard

Bem-vindo ao **PedAI**\! Este projeto é um sistema de marketplace desenvolvido com **Django** (Backend/Site) que possui um painel de análise de dados integrado feito com **Streamlit**.

Siga o guia abaixo para configurar e rodar o projeto no seu computador.

-----

## 🛠️ 1. Pré-requisitos (Instalando o Python)

Antes de começar, você precisa ter o **Python** instalado.

### | Windows

1.  Acesse o site oficial: [python.org/downloads](https://www.python.org/downloads/).
2.  Baixe a versão mais recente.
3.  **MUITO IMPORTANTE:** Na hora de instalar, marque a caixinha **"Add Python to PATH"** antes de clicar em "Install".

### | Linux (Ubuntu/Debian)

Abra o seu terminal e rode os comandos:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip git -y
```

-----

## 🚀 2. Configurando o Projeto

Siga estes passos na ordem exata.

### Passo 1: Baixar e Entrar na Pasta

Se você baixou o arquivo zip, extraia-o. Abra o terminal (ou CMD no Windows) e entre na pasta do projeto `PedAi`:

```bash
# Exemplo (ajuste o caminho onde você salvou a pasta)
cd Downloads/PedAi
```

### Passo 2: Criar o Ambiente Virtual

Isso serve para não misturar as bibliotecas desse projeto com as do seu computador.

  * **| No Windows:**

    ```powershell
    python -m venv venv
    ```

  * **| No Linux:**

    ```bash
    python3 -m venv venv
    ```

### Passo 3: Ativar o Ambiente Virtual

Você saberá que funcionou se aparecer um `(venv)` na frente da linha do terminal.

  * **| No Windows (Powershell):**

    ```powershell
    .\venv\Scripts\Activate
    ```

    *(Se der erro de permissão, rode: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` e tente de novo)*.

    **| No Windows (CMD/Prompt de Comando):**

    ```cmd
    venv\Scripts\activate.bat
    ```

  * **| No Linux:**

    ```bash
    source venv/bin/activate
    ```

### Passo 4: Instalar as Dependências

Agora vamos baixar tudo que o projeto precisa (Django, Streamlit, Pandas, etc).

```bash
pip install -r requirements.txt
```

*(Aguarde a instalação terminar)*.

### Passo 5: Configurar o Banco de Dados

Vamos criar o arquivo do banco de dados (`db.sqlite3`) e as tabelas necessárias.

```bash
python manage.py migrate
```

*(No Linux, se der erro com "python", use "python3")*.

-----

## ▶️ 3. Rodando o Projeto

O projeto tem duas partes que precisam rodar ao mesmo tempo: o **Site (Django)** e o **Dashboard (Streamlit)**.

### 🌐 Parte 1: Rodar o Site (Django)

No terminal onde você já está (com a venv ativada):

```bash
python manage.py runserver
```

Agora, acesse no seu navegador: **[http://127.0.0.1:8000](https://www.google.com/search?q=http://127.0.0.1:8000)**

> **Dica:** Navegue pelo site, crie uma conta e faça alguns pedidos para gerar dados para o dashboard\!

-----

### 📊 Parte 2: Rodar o Dashboard (Streamlit)

**Não feche** o terminal do Django\! Abra um **NOVO terminal** (ou uma nova aba).

1.  Entre na pasta novamente:
    ```bash
    cd Downloads/PedAi
    ```
2.  Ative o ambiente virtual neste novo terminal também:
      * **Windows:** `.\venv\Scripts\Activate`
      * **Linux:** `source venv/bin/activate`
3.  Rode o dashboard:
    ```bash
    streamlit run dashboard.py
    ```

O navegador deve abrir automaticamente com o Dashboard. Se não abrir, acesse o link que aparecerá no terminal (geralmente **http://localhost:8501**).

-----

## 🛑 Como Parar?

Para parar qualquer um dos servidores, vá no terminal correspondente e aperte **CTRL + C**.

-----

## 📝 Resumo Rápido (Cheat Sheet)

| Ação | Comando |
| :--- | :--- |
| **Ativar Venv (Win)** | `.\venv\Scripts\Activate` |
| **Ativar Venv (Linux)** | `source venv/bin/activate` |
| **Rodar Site** | `python manage.py runserver` |
| **Rodar Dashboard** | `streamlit run dashboard.py` |

## 🤝 Colaboradores

Este projeto é o resultado do trabalho e da dedicação de uma equipe incrível. Conheça quem fez o **PedAI** acontecer:

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/Marcopolojr360">
        <img src="https://github.com/Marcopolojr360.png" width="100px;" alt="Foto de Marcos Paulo no GitHub"/>
        <br />
        <sub><b>Marcos Paulo</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Pedro-Priori">
        <img src="https://github.com/Pedro-Priori.png" width="100px;" alt="Foto de Pedro Priori no GitHub"/>
        <br />
        <sub><b>Pedro Priori</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Raicalira">
        <img src="https://github.com/Raicalira.png" width="100px;" alt="Foto de Raica Lira no GitHub"/>
        <br />
        <sub><b>Raica Lira</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/VictorGabriel-00">
        <img src="https://github.com/VictorGabriel-00.png" width="100px;" alt="Foto de Victor Gabriel no GitHub"/>
        <br />
        <sub><b>Victor Gabriel</b></sub>
      </a>
    </td>
  </tr>
</table>