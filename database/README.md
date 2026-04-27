# location-loggerデータベース (MariaDBとphpMyAdminのコンテナ)

データベースは*Dockerコンテナ*で動かします。

以下のコマンドは`database/lldb`ディレクトリで実行してください。

```bash
cd database/lldb
```

## DBの起動

`.env.example`を参考に`.env`を作成してから、以下のコマンドを実行してください。

```bash
docker compose up -d
```

`docker ps`コマンドを実行して、`lldb-db-1`コンテナと`lldb-php-my-admin-1`コンテナが正常に起動していることを確認してください。

## DBの停止

```bash
docker compose down
```
