# location-loggerバックエンド (Python)

本プロジェクトでは[*uv*](https://docs.astral.sh/uv/)が必要です。

以下のコマンドは`backend`ディレクトリで実行してください。

```bash
cd backend
```

## ローカル環境での使い方

## プロジェクトのセットアップ

```bash
# タスク: T001
uv sync
```

## DBの初期化

予め、[`../database/README.md`](../database/README.md)の手順に従ってMariaDBを動かしてください。

```bash
# タスク: T011
uv run -m location_logger.db init
```

## バックエンドの起動

データベースの`.env`と一致するようにバックエンド用の`.env`を作成してから、以下のコマンドを実行してください。

```bash
uv run -m uvicorn --host=localhost --port=8000 --factory location_logger:create_app
```

debugpyを使う場合は、以下のコマンドを実行します。

```bash
# タスク: T012
uv run -m debugpy --listen localhost:8001 -m uvicorn --host=localhost --port=8000 --factory location_logger:create_app --reload
```

## 動作確認

[*REST Client*](https://open-vsx.org/extension/humao/rest-client)で`api_test.rest`を使うか、ターミナルで以下のコマンドを実行してください。

```bash
curl http://localhost:8000/api/v1/misc/version
```
