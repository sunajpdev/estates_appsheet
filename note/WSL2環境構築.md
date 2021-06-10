# WSL2開発緩急設定

[WSL2を使ってWindowsでMisskey開発をはじめよう | Misskey Site!](https://misskey-site.com/posts/wsl2-dev-misskey)

# 目次 {ignore=true}
<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [WSL2開発緩急設定](#wsl2開発緩急設定)
- [「保留」 WSLにlocalhostで接続できるように](#保留-wslにlocalhostで接続できるように)
- [必要パッケージインストール](#必要パッケージインストール)
- [PostgreSQLのセットアップ](#postgresqlのセットアップ)
  - [初期設定](#初期設定)

<!-- /code_chunk_output -->

# 「保留」 WSLにlocalhostで接続できるように

C:\ユーザー\[ユーザー名]\.wslconfig に追加

エクスプローラーであれば%USERPROFILE%にアクセス
```
localhostForwarding=True
```


# 必要パッケージインストール

```
# Node.js
curl -sL https://deb.nodesource.com/setup_current.x | sudo -E bash -
sudo apt install -y nodejs
node -v

# PostgreSQL
wget https://salsa.debian.org/postgresql/postgresql-common/raw/master/pgdg/apt.postgresql.org.sh
sudo sh apt.postgresql.org.sh -i -v 13
sudo /etc/init.d/postgresql restart

# Redis
sudo add-apt-repository ppa:chris-lea/redis-server
sudo apt update
sudo apt install -y redis-server
# systemctlではなくservice
sudo service redis-server start

# build-essential
sudo apt install build-essential -y
```

# PostgreSQLのセットアップ

## 初期設定
```
sudo -u postgres psql
```

```
alter role postgres with password 'poepoe';
create database estate;
exit
```

# 起動

```
$ sudo /etc/init.d/postgresql restart
```

# postgresqlの設計

文字列型の使い分け | Let's POSTGRES : https://lets.postgresql.jp/documents/technical/text-processing/1

## DB 作成とDBの確認

```
$ sudo -u postgres psql
```

```
# CREATE DATABASE estates_appsheet;

# \l
```



## ログイン
```
$ psql -U postgres -d estates_appsheet -h localhost
```


## テーブル作成

```
CREATE TABLE estates  (
  id text primary key,
  note text,
  price numeric(8,0),
  shop text, 
  place text, 
  prefecture text, 
  city text, 
  station text, 
  route text, 
  work text, 
  area numeric(8,2), 
  buildingarea numeric(8,2), 
  buildingyear text, 
  ldk text, 
  url text, 
  created timestamp
);

CREATE INDEX on estates(prefecture, city, station, route);

```

## python psycopg2から接続できるようにする pg_hba

psycopg2で接続する際にはipv4での接続となるため、IPv4に追加する必要がある。
外部接続の場合は、そのIPアドレスも許可する

```
$ sudo vi /etc/postgresql/13/main/pg_hba.conf 
```

```
# IPv4 local connections:
host    all             all             127.0.0.1/32        md5
```

アドレスの確認方法は、ログを確認する

```
$ sudo tail -f /var/log/postgresql/postgresql-13-main.log 
```



# CSVからPostgresqlにデータ登録
## 登録用スクリプト

```
import configparser
ini = configparser.ConfigParser()
ini.read('config.ini', encoding='utf-8')

from sqlalchemy import create_engine, text
database, user, password, host, dbname = \
    ini.get('DB', 'database'), \
    ini.get('DB', 'user'), \
    ini.get('DB', 'password'), \
    ini.get('DB', 'host'), \
    ini.get('DB', 'dbname')
url = f'{database}://{user}:{password}@{host}/{dbname}'

engine = create_engine(url)
conn = engine.connect().connection

```