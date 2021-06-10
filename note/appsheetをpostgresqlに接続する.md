# Appsheet Postgresql

[WSL2を使ってWindowsでMisskey開発をはじめよう | Misskey Site!](https://misskey-site.com/posts/wsl2-dev-misskey)

# 目次 {ignore=true}

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->


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
ini.read("config.ini", encoding="utf-8")

from sqlalchemy import create_engine, text

database, user, password, host, dbname = (
    ini.get("DB", "database"),
    ini.get("DB", "user"),
    ini.get("DB", "password"),
    ini.get("DB", "host"),
    ini.get("DB", "dbname"),
)
url = f"{database}://{user}:{password}@{host}/{dbname}"

engine = create_engine(url)
conn = engine.connect().connection


import pandas as pd
import time

start = time.time()

df = pd.read_csv("tmp/_gs.csv")

rows = df.to_dict(orient="records")

sql = text(
    "\
    INSERT INTO estates( \
        id, note, price, shop, place, prefecture, city, station, route, work, area, \
        buildingarea, ldk, buildingyear, url) \
    VALUES( \
        :id, :note, :price, :shop, :place, :prefecture, :city, :station, :route, :work, :area,\
        :buildingarea, :ldk, :buildingyear, :url) \
    "
)

for row in rows:
    try:
        engine.execute(sql, row)
    except Exception as e:
        print(e)

end = time.time()
print(end - start, "s")

```


# appsheet からの接続 
## ODataとは？

Salesforce連携のためのOData入門 : https://www.slideshare.net/shunjikonishi/salesforceodata

特に使わなくても行けそうか？

## AppSheet マニュアル on-premises DB
オンプレミス データベースへの接続 | AppSheet ヘルプセンター : https://help.appsheet.com/en/articles/2213968-connecting-to-an-on-premises-database

###　方法１ IPを許可 一番かんたんな方法

接続先のIPを公開する事

- メリット：かんたん
- デメリット：Firewallを開けなければいけない

公開するIP

IP アドレスとファイアウォール情報の管理 | AppSheet ヘルプセンター : https://help.appsheet.com/en/articles/1658319-managing-ip-addresses-and-firewall-information


Add a new data source で CloudDatabase を選べば良い

### 方法２ DreamFactory の利用

- 別サーバを建ててインストールする方法
- 同一サーバにインストールする方法
インスタレーション - DreamFactory : https://wiki.dreamfactory.com/DreamFactory/Installation


一旦保留！　まず取得データをpostgreに登録して、それをGoogleスプレッドシートに再登録する仕組みで実装する

# 新規取得データをDBに登録