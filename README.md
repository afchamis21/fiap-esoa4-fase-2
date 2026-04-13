# Plant Disease Mock Analytics

Este projeto gera dados sintéticos de doenças de plantas e disponibiliza no Metabase para criação de dashboards.

---

## ⚙️ Pré-requisitos

* Python 3.10+
* Docker + Docker Compose
* Git

---

## 🚀 Setup (Primeira vez)

### 1. Instalar dependências Python

```
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\\Scripts\\activate     # Windows

pip install -r requirements.txt
```

---

### 2. Gerar o banco de dados

```
python setup-db.py
```

Isso vai gerar:

* `data/database.db`
* ~400 registros de treino
* Predições mockadas (~85% de acurácia)

---

### 3. Subir o Metabase

```
docker-compose up -d
```

Acesse:

```
http://localhost:3000
```

---

### 4. Banco já configurado automaticamente

O Metabase já vem pré-configurado.

Isso acontece porque a pasta `postgres_data` (volume do Metabase) está versionada no repositório.

Ou seja:

* Não é necessário adicionar banco manualmente
* Não é necessário configurar conexão
* Os dashboards (se existirem) já estarão disponíveis

Basta subir os containers e acessar

```
/database_files/database.db
```

---

## 🔁 Uso no dia a dia

### Subir containers

```
docker-compose up -d
```

### Parar containers

```
docker-compose down
```

---

## 🧠 Boas práticas (Git + Docker) — IMPORTANTE

Para evitar problemas com banco, volumes ou dashboards:

### ✅ Sempre siga esta ordem

1. Parar os containers

```
docker-compose down
```

2. Puxar atualizações

```
git pull
```

3. (Opcional) Regerar banco

```
python setup-db.py
```

4. Subir containers novamente

```
docker-compose up -d
```

---

### 🚫 Evite

* Rodar `git pull` com containers ativos
* Editar arquivos enquanto o Metabase está usando o banco
* Versionar `data/database.db` (a não ser que queira compartilhar snapshot)

---

### 📤 Antes de dar push

```
docker-compose down
git add .
git commit -m "mensagem"
git push
```

---

## 📊 O que cada pessoa terá

* Mesmo schema
* Dataset semelhante (se cada um gerar localmente)
* Metabase local
* Liberdade para criar dashboards

---

## 🧪 Resetar dados

Se algo quebrar:

```
docker-compose down
rm -rf data/database.db
python setup-db.py
```

---

## 🔐 Credenciais do Metabase

Use as credenciais abaixo para acessar:

```
Email: admin@fiap.com
Senha: abc123!
```

> ⚠️ Recomenda-se não alterar essas credenciais, pois a pasta `postgres_data` está versionada e compartilhada com o grupo.

---

## 🐳 Troubles

### Porta já em uso

Altere no `docker-compose.yml`:

```
ports:
  - "3001:3000"
```

---

### Metabase não encontra o banco

* Rode `setup-db.py`
* Verifique se existe `data/database.db`
* Reinicie os containers

---

## ✅ Quick Start

```
pip install -r requirements.txt
python setup-db.py
docker-compose up -d
```

Acesse: [http://localhost:3000](http://localhost:3000)
