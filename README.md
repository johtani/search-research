# 検索エンジンなどの調査用リポジトリ

johtaniが個人的に検索エンジンの利用方法などを調べるための個人プロジェクトのリポジトリ。
ベクトル検索などを試す予定です。

## セットアップ

おもにPythonを利用します。
VS CodeのDev Containerの設定が追加してあるので、VS Code + Dev Container拡張 + Dockerの環境があれば、以下のセットアップは不要です。

ローカル環境で構築する場合は以下の実行が必要になります。

バックエンド用（Python環境）
```
python3 -m venv .venv
source .venv/bin/activate
pip install poetry
poetry install --no-root
pip install japanese-clip
```

> `pip install japanese-clip`は依存関係にあるモジュールのインストールがpoetryだけではできなかったので暫定対処として実行する必要があります。

フロントエンド用（Node、React環境）
```
cd frontend
. ${NVM_DIR}/nvm.sh
nvm install
yarn
```

## データについて

[AmazonのShopping Queries Dataset](https://github.com/amazon-science/esci-data)を利用します。
なお、esci-dataの中のparquetのデータは1GB以上あるので、git-lfsを利用してcloneする必要があります。
手元の環境にgit-lfsがインストールされていることを確認してください。

```
git clone https://github.com/amazon-science/esci-data.git
```

[shuttie/esci-s： Extra product metadata for the Amazon ESCI dataset](https://github.com/shuttie/esci-s)も利用予定です。

サンプルデータを利用する場合はリポジトリをクローンします。

```
git clone https://github.com/shuttie/esci-s.git
```

全データを利用する場合は、[esci-sのリポジトリ](https://github.com/shuttie/esci-s)に記載のある`zst`ファイルをダウンロードして、`esci-s-full`というディレクトリを作って保存してください。
このファイル用の前処理のプログラム（`tools/extract-esci-s.py`）で想定しているディレクトリになります。


## 対象検索エンジン

検索エンジンは[docker-compose.yml](./docker-compose.yml)でそれぞれサービスとして定義します。
Docker Desktop、docker composeがインストールされていることを想定しています。

```
docker compose up <サービス名>
```

で起動します。

### 対応済み

* Elasticsearch：サービス名 `es`
  * kuromojiプラグインをインストール済み

### 対応予定？ 
 
* OpenSearch
* Vespa
* Apache Solr
* Weaviate
* Qdrant

## データの準備 

### JSONデータの生成

esci-dataをgit cloneした後にまずは、JSONLのデータを生成します。
あとで加工したり、他のシーンでの利用の容易さを考えていったん1データ（1行）1JSONの形で出力しておきます。

```
python -m tools.extract-products
```

`esci-jsonl/raw-products`にロケールごとのjsonファイルとして出力されます。内容としては、1行1JSONの形式となっています。


### 中間データの生成

検索エンジンにインデックス登録する前に、データに何かしらの追加データを付与することがあります。
`esci-jsonl/raw-products`のデータをもとにLLMを利用してembeddingsのベクトルを生成するなどです。
ただし、これらの処理は計算コストが高いため、検索エンジンのインデキシングの処理とは切り離しておきたい場合（インデキシングの時間だけを計測したいなどの目的もあるため）があるので、
事前にデータ生成を行えるプログラムを用意しています。

以下のコマンドでオプションが表示されます。

```
python -m tools.make-extra-products-data -h
```

### 検索エンジンへのデータ登録

上記のJSONデータをElasticsearchにデータを登録する処理は以下の通りです。
現時点では、esci-dataのpruductデータのうち、`product_locale=jp`のものだけが登録されます。
「中間データの生成」処理で作成したデータをproductデータにマージしながら追加する処理もあります。

```
python -m tools.bulk-index-products elasticsearch raw
```

そのほかのオプションに関しては`-h`を実行してください。

```
python -m tools.bulk-index-products -h
```

データ登録処理はElasticsearchのI/Fを元に作っていることもあり、他の検索エンジンでは使いにくい点があるかも知れないです。
また、用語の違いもあります。

## サンプル画面で検索

フロントエンド（React + Search UI）からバックエンド（Fast API/Python）を経由して、検索エンジンに検索をするサンプル画面を用意してあります。以下の手順で、バックエンド、フロントエンドを起動して、`http://localhost:3000/`にアクセスすると検索できるようになります。


* バックエンドの起動
```
uvicorn backend.server:app --reload
```

* フロントエンドの起動
```
cd frontend
yarn start
```

## License

MITライセンス