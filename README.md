# 検索エンジンなどの調査用リポジトリ

johtaniが個人的に検索エンジンの利用方法などを調べるための個人プロジェクトのリポジトリ。
ベクトル検索などを試す予定です。

## setup

おもにPythonを利用します。

```
python3 -m venv .venv
source .venv/bin/activate
pip install poetry
poetry install --no-root
```

## データについて

[AmazonのShopping Queries Dataset](https://github.com/amazon-science/esci-data)を利用します。
なお、esci-dataの中のparquetのデータは1GB以上あるので、git-lfsを利用してcloneする必要があります。
手元の環境にgit-lfsがインストールされていることを確認してください。

```
git clone https://github.com/amazon-science/esci-data.git
```

[shuttie/esci-s： Extra product metadata for the Amazon ESCI dataset](https://github.com/shuttie/esci-s)も利用予定です。

## 対象検索エンジン

検索エンジンは[docker-compose.yml](./docker-compose.yml)でそれぞれサービスとして定義します。

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

Elasticsearchにデータを登録する処理は以下の通りです。
現時点では、esci-dataのpruductデータのうち、`product_locale=jp`のものだけが登録されます。

```
python -m tools.es.bulk-index-products
```

## License

MITライセンス