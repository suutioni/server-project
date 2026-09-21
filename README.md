# server-project

FastAPI・PostgreSQL・Dockerを使って構築したタスク管理APIです。

Web APIの実装だけでなく、Nginxによるリバースプロキシ、AlembicによるDBマイグレーション、OpenTofuによるIaC、GitHub ActionsによるCIとDockerイメージの自動配布まで構築しています。

## Architecture

```text
Browser
   |
   | HTTP :80
   v
Nginx
   |
   | app:8000
   v
FastAPI
   |
   | SQLAlchemy / psycopg
   v
PostgreSQL
```

開発・CIでは以下の構成も使用しています。

```text
Developer
   |
   | git push
   v
GitHub
   |
   v
GitHub Actions
   |
   +-- Python syntax check
   +-- Docker image build
   +-- OpenTofu validation
   |
   v
GitHub Container Registry
```

## Features

- FastAPIによるREST API
- PostgreSQLによるデータ永続化
- SQLAlchemyによるORM
- TaskのCreate / Read / Update / Delete
- AlembicによるDBマイグレーション
- `.env` による環境変数管理
- Docker / Docker Composeによるコンテナ化
- Nginxによるリバースプロキシ
- OpenTofuによるIaC
- GitHub ActionsによるCI
- GHCRへのDockerイメージ自動配布

## API

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | APIの動作確認 |
| GET | `/db-check` | PostgreSQL接続確認 |
| POST | `/tasks` | Taskを作成 |
| GET | `/tasks` | Task一覧を取得 |
| PATCH | `/tasks/{task_id}` | Taskを更新 |
| DELETE | `/tasks/{task_id}` | Taskを削除 |

FastAPIのSwagger UIは以下から確認できます。

```text
http://localhost/docs
```

## Tech Stack

| Category | Technology |
|---|---|
| Language | Python 3.12 |
| Web API | FastAPI |
| ORM | SQLAlchemy |
| Database | PostgreSQL 17 |
| PostgreSQL Driver | psycopg |
| Migration | Alembic |
| Container | Docker |
| Container Management | Docker Compose |
| Reverse Proxy | Nginx |
| IaC | OpenTofu |
| IaC Provider | Docker Provider |
| CI / Delivery | GitHub Actions |
| Container Registry | GitHub Container Registry |
| Development Environment | WSL2 / Ubuntu |

## Project Structure

```text
server-project/
├── .github/
│   └── workflows/
│       └── ci.yml
├── alembic/
│   └── versions/
├── app/
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── infra/
│   ├── main.tf
│   ├── outputs.tf
│   ├── terraform.tfvars.example
│   └── variables.tf
├── nginx/
│   └── default.conf
├── .env.example
├── .gitignore
├── alembic.ini
├── compose.yaml
├── Dockerfile
└── requirements.txt
```

## Setup

### 1. Repositoryを取得

```bash
git clone https://github.com/suutioni/server-project.git
cd server-project
```

### 2. 環境変数を作成

```bash
cp .env.example .env
```

必要に応じて `.env` の値を変更します。

`.env` にはパスワードなどを含む可能性があるため、Gitにはコミットしません。

### 3. コンテナを起動

```bash
docker compose up --build -d
```

### 4. Database Migration

```bash
docker compose exec app alembic upgrade head
```

### 5. 動作確認

ブラウザで以下へアクセスします。

```text
http://localhost/
```

Swagger UI:

```text
http://localhost/docs
```

### 6. 終了

```bash
docker compose down
```

## Nginx

外部からFastAPIの8000番ポートへ直接アクセスさせず、Nginxの80番ポートを入口として使用しています。

```text
Client
  |
  v
Nginx :80
  |
  v
FastAPI :8000
```

FastAPIの8000番はDocker内部でのみ使用します。

これにより、外部公開する入口をNginxに一本化し、今後HTTPSやアクセス制御などを追加しやすい構成にしています。

## Database Migration

DBの構造変更にはAlembicを使用しています。

現在は以下のMigrationを作成しています。

```text
create_tasks_table
        |
        v
add_description_to_tasks
```

最新状態へ更新:

```bash
docker compose exec app alembic upgrade head
```

現在のMigration確認:

```bash
docker compose exec app alembic current
```

## Infrastructure as Code

OpenTofuとDocker Providerを使用し、Docker NetworkをIaCとして管理しています。

```bash
cd infra

tofu init
tofu fmt
tofu validate
tofu plan
tofu apply
```

OpenTofuでは以下の流れを確認しています。

```text
.tf
 |
 v
OpenTofu
 |
 v
Docker Provider
 |
 v
Docker Engine
 |
 v
Docker Network
```

`terraform.tfstate` や実際の `terraform.tfvars` はGit管理から除外しています。

## CI / Delivery

GitHub Actionsは以下のタイミングで実行されます。

```text
push
pull_request
```

CIでは以下を自動確認します。

```text
python-check
    |
    +-- Install dependencies
    +-- Python syntax check

docker-build
    |
    +-- Docker image build

opentofu-check
    |
    +-- tofu fmt -check
    +-- tofu init
    +-- tofu validate
```

さらに `main` ブランチへのpush時にはDockerイメージをビルドし、GitHub Container Registryへ自動配布します。

```text
main push
   |
   v
GitHub Actions
   |
   v
Docker Build
   |
   v
ghcr.io/suutioni/server-project:latest
```

現時点では実サーバーへの自動デプロイは行っていません。

## Security

秘密情報をGitHubへ公開しないよう、以下のファイルをGit管理から除外しています。

```text
.env
terraform.tfstate
terraform.tfstate.*
terraform.tfvars
terraform.tfvars.json
.terraform/
```

公開用には以下のサンプルファイルを用意しています。

```text
.env.example
terraform.tfvars.example
```

## What I Learned

このプロジェクトを通して、Web APIの実装だけでなく、アプリケーションを実際に運用するための構成を段階的に学習・構築しました。

```text
FastAPI
   ↓
PostgreSQL
   ↓
CRUD
   ↓
Alembic
   ↓
Nginx
   ↓
OpenTofu
   ↓
Git / GitHub
   ↓
GitHub Actions
   ↓
Container Registry
```

特に、アプリケーションコード・データベース・ネットワーク・CIを別々に考え、それぞれをコードで管理して再現できる構成を意識しています。

## Future Improvements

- 自動テストの追加
- HTTPS対応
- 認証・認可機能
- ログ・監視
- クラウド環境へのデプロイ
- CDによる実環境への自動デプロイ
