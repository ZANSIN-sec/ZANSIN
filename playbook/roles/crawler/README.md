# 概要
クローラの挙動は[https://miro.com/app/board/o9J_kl9NvKw=/](https://miro.com/app/board/o9J_kl9NvKw=/)を参照のこと。  

# 動作確認環境
```
Python 3.8.2
```

# 実行手順
ゲームAPI（`mini4-game-api`）とコーポレートサイト（`mini4-corporate`）を構築の上、以下の手順でクローラを起動する。  

 1. リポジトリのClone  
 `~$ git clone https://gitlab.com/minihardening4/mini4-crawler.git`  
 2. ゲームAPI（Dockerコンテナ）の起動  
 `~$ cd ./mini4-game-api/`  
 `~/mini4-game-api$ docker-compose up -d`
 3. コーポレートサイト（Dockerコンテナ）の起動  
 `~/mini4-game-api$ cd ../mini4-corporate/`  
 `~/mini4-corporate$ docker-compose up -d`
 4. ライブラリのインストール  
 `~/mini4-corporate$ cd ../mini4-crawler/`  
 `~/mini4-crawler$ pip3 install -r requirements.txt`
 5. スコアサーバ（Dockerコンテナ：Elasticsearch+Kibana）の起動  
 `~/mini4-crawler$ docker-compose up -d`  
 ※Elasticsearch, Kibana共にバージョン5.4で動作確認済み。  
 6. クローラの実行  
 `~/mini4-crawler$ python3 main.py --team team-a`  
 ※デバッグ時のチーム名は適当な文字列でOK。  
    
コーポレートサイトへのアクセス（シングルスレッド）→ゲームのプレイ（マルチスレッド）を自動実行し、`タイマーセットした終了時刻が到来` or `強制終了（Ctrl+C）`するまでゲームをプレイし続ける。  
プレイの状況はクローラのLocal DBやhistoryログで確認できる（詳細は`How to`を参照のこと）。  

## 個別のシステムに対してクローリングする場合
オプションでクローラのアクセス先を変更することができる。  
* `オプションなし`：全システム（Game, リポジトリ, コーポレート）をクローリング。  
  `~/mini4-crawler$ python3 main.py --team team-a`  
  
* `--game`：Gameのみクローリング。  
  `~/mini4-crawler$ python3 main.py --team team-a --game`  
  
* `--repo`：リポジトリのみクローリング。  
  `~/mini4-crawler$ python3 main.py --team team-a --repo`  
  
* `--corp`：コーポレイトのみクローリング。  
  `~/mini4-crawler$ python3 main.py --team team-a --corp`  
  
アクセス先を組み合わせる場合は、各オプションを指定すること。  

# ペナルティの条件
## ゲームAPIのペナルティ
競技者が不正行為を行った場合、該当チームにはペナルティが課される。  
ペナルティの内容と不正行為の判定基準は以下の通り。  

* ペナルティ  
不正行為の回数に応じてプレイヤーの**プレイ頻度を減らす（段階的に遅延）**。  

* 不正行為の判定基準  
  * 「現在のスタミナ（`stamina`）」が「最大スタミナ（max_stamina）」を上回っている。  
  * 「ゴールド（`gold`）」が改ざんされている。  
  * 「最大スタミナ（`max_stamina`）」が改ざんされている。  
  * 「最大HP（`max_hp`）」が改ざんされている。  
  * 「最大攻撃力（`max_str`）」が改ざんされている。  
  * 「経験値（`exp`）」が改ざんされている。  
  * 戦闘のターンが少なすぎる。  
  * ガチャにてSRアイテムが頻発する。  
  * ランキングにチーターが存在する。  

### ゴールド改ざんの判定ルール
レベルに対するゴールが不自然に多い場合、不正とみなす。  

|レベル|判定条件|
|:---|:---|
|Lv01〜Lv20|ゴールドが`1500`より多い|
|Lv21〜Lv40|ゴールドが`2000`より多い|
|Lv41〜Lv60|ゴールドが`2500`より多い|
|Lv61〜Lv80|ゴールドが`3000`より多い|

### 最大スタミナ改ざんの判定ルール
レベルに対する最大スタミナが不自然に多い場合、不正とみなす。  

|レベル|判定条件|
|:---|:---|
|Lv01〜Lv20|最大スタミナが`50`より多い|
|Lv21〜Lv40|最大スタミナが`100`より多い|
|Lv41〜Lv60|最大スタミナが`150`より多い|
|Lv61〜Lv80|最大スタミナが`200`より多い|

### 最大HP改ざんの判定ルール
レベルに対する最大HPが不自然に多い場合、不正とみなす。  

|レベル|判定条件|
|:---|:---|
|Lv01〜Lv20|最大HPが`100`より多い|
|Lv21〜Lv40|最大HPが`150`より多い|
|Lv41〜Lv60|最大HPが`200`より多い|
|Lv61〜Lv80|最大HPが`250`より多い|

### 最大攻撃力改ざんの判定ルール
レベルに対する最大攻撃力が不自然に多い場合、不正とみなす。  

|レベル|判定条件|
|:---|:---|
|Lv01〜Lv20|最大攻撃力が`50`より多い|
|Lv21〜Lv40|最大攻撃力が`100`より多い|
|Lv41〜Lv60|最大攻撃力が`150`より多い|
|Lv61〜Lv80|最大攻撃力が`200`より多い|

### 経験値改ざんの判定ルール
レベルに対する経験値が不自然に多い場合、不正とみなす。  

|レベル|判定条件|
|:---|:---|
|Lv01〜Lv20|経験値が`200`より多い|
|Lv21〜Lv40|経験値が`300`より多い|
|Lv41〜Lv60|経験値が`800`より多い|
|Lv61〜Lv80|経験値が`2500`より多い|

### 戦闘ターンの判定ルール
「戦闘に勝利するまでのターン」と「想定ターン」が不一致の場合、不正とみなす。  

* 想定ターンの計算方法  
敵のHP \/ プレイヤーの強さ  
※計算結果がfloatの場合は切り上げる。  

### ガチャ不正の判定ルール
1エポック内のガチャにおいて、スーパーレア（`SR`）アイテムを**3回連続**で引いた場合、不正とみなす。  

* 不正判定されるケース  
例）ガチャを引く回数：5回  
  * 1回目：`N`アイテム  
  * 2回目：`R`アイテム  
  * 3回目：`SR`アイテム  
  * 4回目：`SR`アイテム  
  * 5回目：`SR`アイテム  

`SR`アイテムを**3連続で引いている**ため不正となる。  

* 不正判定されないケース  
例）ガチャを引く回数：5回  
  * 1回目：`N`アイテム  
  * 2回目：`SR`アイテム  
  * 3回目：`SR`アイテム  
  * 4回目：`N`アイテム  
  * 5回目：`SR`アイテム  

`SR`アイテムを3回引いているが、**3連続ではない**ため不正ではない。  

### ランキング不正の判定ルール
ランキングAPIで取得したランキング内にチーターが存在する場合、不正とみなす。  

* 不正判定の方法  
   * ランキングAPIで取得したレベルランキングに、クローラが保持している**プレイヤーリストに存在しないプレイヤーが含まれている**。
   * ランキングAPIで取得した武器ランキングに、クローラが保持している**プレイヤーリストに存在しないレベル1のプレイヤーが含まれている**。

* ペナルティ内容
   * 上記不正判定に該当するチートユーザ数×1秒（秒数はconfig.iniにて変更可能）をクローリングエポック間の待ち時間に追加する。

## コーポレートサイトのペナルティ
各コーポレートサイトから以下の応答が返された場合、スコア（SLAポイント）は加算されない。  
 * サイトのトップページに以下の文字列が含まれている。  
   * rLU7P Hacked 6h0Z1  
   * Warning  
 * サーバが正常応答しない。  
   * 400以上のHTTPステータスが返ってくる（400、403、404など）  
 * 各サイトのレスポンスボディに以下のキーワードが存在しない。  
   * コーポレートサイト  
     `<title>Welcome to Company | SCROLL ETHNIC</title>`  
     `<a href="/" rel="home">SCROLL ETHNIC</a>`
   * ファンサイト（要修正）  
     `/var/www/html/wp-content`  
     `headers already sent`  
   * 採用サイト  
     `<title>SAIYO</title>`  
     `<h1 id="title">SAIYO</h1>`  
   * 掲示板  
     `<input type="hidden" name="bbs" value="bbs" />`  
     `<a href="../test/read.php/`  
   * お問い合わせ  
     `<title>お問い合わせフォーム</title>`  
     `<h1>お問い合わせフォーム</h1>`  

キーワードを変更する場合は、設定ファイル`config.ini`の各サイトのパラメータ`keywords`を変更する。  

## リポジトリサーバのペナルティ
リポジトリサーバ上の監視対象ファイルについて、以下の場合はスコア（SLAポイント）は加算されない。  
 * 監視対象ファイルが改ざんされている。  
   * equipment.csv  
     クローラの初回起動時（競技開始〜数秒以内）に取得したファイル内容と、epoch毎に取得するファイル内容が異なっている（ハッシュ値を比較）。  
   * README.md  
     コンテンツに「`Hacked!!`」が含まれている。  
 * リポジトリサーバが正常応答しない。  
   400以上のHTTPステータスが返ってくる（400、403、404, 503など）。  

# How to  
## ローカルDBの初期化
クローラ実行時に以下のオプション「`--delete-db`」を付けることで、ローカルDB（`./sqlite3/minih_v4_{チーム名}.db`）を初期化することができる。  
コマンド例：`~/mini4-crawler$ python3 main.py --team team-a --delete-db`  

なお、ローカルDB上に記録されていたユーザは、退会APIによってサーバ側DBからも削除される。

## デバッグモードで起動
ローカル環境でテストを行う場合、ゲームAPIやスコアサーバなどの接続先を切り替える必要がある。クローラ実行時に以下のオプション「`--debug`」を付けることで、`config.ini`からデバッグ用の接続先を取得することができる。  
コマンド例：`~/mini4-crawler$ python3 main.py --team team-a --debug`  

なお、デバッグ用の接続先は、設定ファイル`config.ini`の`~_debug`パラメータに定義する。  

## タイマーのセット
クローラの実行開始・終了をタイマーで制御できる。  
タイマーは、設定ファイル`config.ini`の`[Common]`セクションの下記パラメータで設定する。  

|パラメータ名|説明|設定例|
|:--|:--|:--|
|competition_start_time|クローリング開始時刻（yyyyMMddHHmmSS）。|`20201005103000`|
|competition_lunch_time|お昼休憩の開始時刻（yyyyMMddHHmmSS）。|`2020100512000`|
|competition_restart_time|競技再開時刻（yyyyMMddHHmmSS）。|`2020100513000`|
|competition_busy_time|クローリングの加速開始時刻（yyyyMMddHHmmSS）。当該時刻〜終了時刻の間、クローリング速度が2倍になる。|`20201005153000`|
|competition_end_time|クローリング終了時刻（yyyyMMddHHmmSS）。|`20201005160000`|

タイマーは**クローラが稼働するシステムの時刻**をチェックしているため、タイマー使用の際はシステム時刻がズレていないことを確認すること。  

## コーポレートサイトのURLを変更する場合  
デフォルト値は`127.0.0.1`。　  
URLを変更したい場合は、設定ファイル`config.ini`の`Common`セクションのパラメータ`web_host`を変更する。  
また、各サイトのポート番号やPathを変更したい場合は、以下のセクションのパラメータ`url`を変更する。  
  * コーポレート：`[WEB_Corporate]`  
  デフォルト値：`http://{}/`  
  * ファンサイト：`[WEB_FanSite]`  
  デフォルト値：`http://{}/matzbank/`  
  * 採用サイト：`[WEB_Saiyo]`  
  デフォルト値：`http://{}/saiyou/`  
  * 掲示板：`[WEB_BBS]`  
  デフォルト値：`http://{}/bbs/`  
  * お問い合わせ：`[WEB_INQUIRY]`  
  デフォルト値：`http://{}/inquiry/`  

## リポジトリサーバのURLを変更する場合  
デフォルト値は以下の通り。  
* equipment.csv  
`url_csv : http://repository.{}.mini.local/gitbucket/repomaster/gameinfo/raw/{}/equipment.csv`  
* README.md  
`url_readme: http://repository.{}.mini.local/gitbucket/repomaster/gameinfo/raw/{}/README.md`  

URLを変更する場合は、設定ファイル`config.ini`の`REPO_SRV`セクションの各パラメータを変更する。  
また、URLにはリポジトリサーバの構築毎に変化するハッシュ値が含まれるため、パラメータ`repo_url_hash`の値は適宜変更すること。  

## ゲームAPIのURLを変更する場合
URLを変更する場合は、設定ファイル`config.ini`の各APIセクションのパラメータ`url`を変更する。  
  * ユーザ作成：`[API_NewUser]`  
  * ログイン：`[API_Login]`  
  * ユーザID取得：`[API_GetUserId]`  
  * 画像アップロード：`[API_Upload]`（クローラでは未使用）  
  * 退会：`[API_Delete]`  
  * コース一覧取得：`[API_Course]`  
  * コース選択：`[API_CoursePost]`  
  * 戦闘：`[API_Battle]`  
  * スタミナ回復：`[API_Recovery]`  
  * ガチャ：`[API_Gatya]`  
  * プレイヤーデータ取得：`[API_Player]`  
  * 課金：`[API_Charge]`  
  * ランキング：`[API_Ranking]`  

## プレイヤー数を変更する場合
デフォルト値は`1`  
変更したい場合は、設定ファイル`config.ini`の`[Common]`セクションのパラメータ`max_player_num`を変更する。  

## Local Proxyの設定  
クローラ<->APIの通信を確認したい場合、Local Proxyを設定する。  
設定ファイル`config.ini`の`[Common]`セクションのパラメータ`proxy_addr`にProxyアドレスを入力する。  
例）`http://127.0.0.1:8088`  

## クローラのLocal DB
クローラのLocal DB（SQLite3）は以下に格納されている。  
`{crawler root}/sqlite3/mini_v4.db`  

現在はユーザステータスを管理するテーブル`UserInfoTBL`のみ保持している。  

|カラム名|説明|
|:--|:--|
|id|クローラが一意に採番するID。API側のidとは非同期。|
|status|ユーザの活性状態（1:アクティブなユーザ、0：退会したユーザ）|
|charge|ユーザの課金額（リアルマネー）|
|injustice_num|不正行為の回数。3回の不正でBanされる。|
|user_id|ユーザID。|
|パスワード|パスワード。|
|nickname|ニックネーム（クローラは未使用）。|
|created_at|ユーザ作成時刻（クローラは未使用）。|
|level|レベル。|
|exp|経験値。|
|gold|ゴールド。|
|max_hp|最大HP。|
|max_stamina|最大スタミナ。|
|max_str|最大str（クローラは未使用）。|
|need_exp|need_exp（クローラは未使用）。|
|stamina|現スタミナ。|
|staminaupdated_at|スタミナ更新時刻（クローラは未使用）。|
|weapon_id|武器ID（クローラは未使用）。|
|armor_id|防具ID（クローラは未使用）。|

## プレイ履歴の確認
クローラを起動すると、1エポック毎に各ユーザの情報をCSVファイルに出力（追記）する。  
`{crawler root}/history.csv`  

レベルや経験値などの上昇過程を確認できる。  

|カラム名|説明|
|:--|:--|
|epoch|エポック数。|
|user_id|ユーザID。|
|level|レベル。|
|exp|経験値。|
|gold|ゴールド。|
|max_stamina|最大スタミナ。|
|stamina|カレント・スタミナ。|
|weapon_id|武器ID（クローラは未使用）。|
|armor_id|防具ID（クローラは未使用）。|
|charge_sum|ユーザの課金額（リアルマネー）。|
|date|レコードの作成時刻。|

## ログの確認
プレイヤー毎の実行履歴が記録される。  
`{crawler root}/logs/mini-crawler_{チーム名}.log`  

ログ中の`id`にてプレイヤーを特定する。  
※`id`はクローラのLocal DB上のid。API側のidとは非同期であることに注意。

以上
