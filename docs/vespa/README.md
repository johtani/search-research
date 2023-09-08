# Vespa

* [公式サイト](https://vespa.ai/)
* [Getting Started](https://docs.vespa.ai/en/getting-started.html)

## 起動から確認まで

Dockerを利用して起動しています。Vespa自体は複数のコンポーネントから構成されており、それぞれを異なるサーバー上で動作させることも可能ですが、本アプリでは1つのDockerコンテナ上ですべての機能を動作させています（参照：[docker-compose.yml](../../docker-compose.yml)）。

動作確認を行うために、チュートリアルに従い、vespa-cliをインストール(参照：[postCreateCommand.sh](../../.devcontainer/postCreateCommand.sh))して利用しています。
Vespaの管理用のAPIのポートはデフォルトで`19071`、検索用のポートが`8080`となっています。

Dockerコンテナを起動後に、接続確認を行うためにはvespa-cliを利用します。

```
$ vespa status -t http://vespa:19071
```

接続できれば、以下のような表示がされます。

```
Container at http://vespa:19071 is ready
```

「アプリケーションをデプロイする」とデータ登録したり検索ができるようになりそう。
[アプリケーションパッケージ](https://docs.vespa.ai/en/application-packages.html)には、設定や機械学習のモデルなどが含まれる。
最低限、services.xmlが必要。そのほかのものは[Application Package Reference](https://docs.vespa.ai/en/reference/application-packages-reference.html)に一覧がある。

## インデックス作成

### Application Packageの用意

インデックスを作成するために、Appilication Packageを用意する必要がある。含める情報としては以下の通り。

* services.xml：どのクラスターの機能をどのノード（サーバー）で起動するか？それぞれの機能についてのオプションを設定する
* hosts.xml：これは複数台構成の時のみ必要
* schemas/*.sd：スキーマの[設定ファイル](https://docs.vespa.ai/en/reference/schema-reference.html)。どんなフィールドがあって、どんな使い方をするのか？

### スキーマ設計

documentタイプごとに設計できそう？

[フィールドに指定する項目がいくつかある。](https://docs.vespa.ai/en/schemas.html)

### スキーマなどの登録

Application PackageをVespaのクラスターにデプロイすることで、スキーマなどを登録してデータ登録できるようになる。

> ただし、[pyvespa](https://pyvespa.readthedocs.io/en/latest/index.html)はConfig(Deploy) APIを利用するためのクラスがローカル起動した[Dockerコンテナか、VespaCloud](https://github.com/vespa-engine/pyvespa/blob/master/vespa/deployment.py)しか実装されていないように見える。


## データ登録

vespa cliでデータを登録してみる。
サンプルドキュメントを[jsonファイル](./sample.json)として用意した。
登録コマンドは以下の通り（search-researchのディレクトリから実行した場合）。

```
$ vespa document put docs/vespa/sample.json -t http://vespa:8080
```

問題なく登録できれば以下の表示がされる（試しに動作させた時に、WSL2のディスク残量が20%を切っていたため、507のエラーが返ってきた。WSL2のディスクを増やすことで暫定対処をした）。

```
Success: put id:product:product::1
```

登録データの確認にドキュメントの取得を行ってみる。

```
$ vespa document get id:product:product::1 -t http://vespa:8080
```


## 検索


検索もしてみる。まずは、全件取得。

```
$ vespa query "select * from product where true" -t http://vespa:8080
```

条件指定検索もしてみる。

```
$ vespa query "select * from product where product_title contains 'title'" -t http://vespa:8080
```

```
$ vespa query "select * from product where product_color matches 'yellow'" -t http://vespa:8080
```

ファセットクエリも書いてみる。

```
$ vespa query "select * from product where product_title contains 'title' | all(group(product_locale) each(output(count())))"
 -t http://vespa:8080
```

サンプルが1件しかないので複数のデータを登録できるようにして再度試してみる予定。

## 構成

Document APIを利用する際に必要な要素がある。


```
GET http://localhost:8080/document/v1/product/product/docid?cluster=esci-products
```

* cluster : services.xmlのContent ClusterのID
* namespace : /v1/直後の`product`（**schemaの名前？**）
* document-type : 2つ目の`product`(schemaのdocumentにつけた名前)

## まだよくわからないこと

* どんなコンポーネントが存在しているのか？
  * stateless container = 計算資源 = ingest nodeやquery builderなどに相当？返却データの書き換えなどもできそう？
  * contents cluster = データ資源 = shardに相当？
* Vespaの外でやるほうがいいか、document-processorのようなところでやるのがいいのか？
* どの設定値が動的に変更可能か？
* コンテントのIDに対して、複数のドキュメントのタイプのデータを入れた場合に、内部のデータ構造がどんな感じで構築されるのか？
* 親子関係とかJoinのようなものはあるのか？
* VS Code用の設定ファイル系のプラグインがほしい
* attributeとindexの使い分け方、メモリの使用量などはどうやって決めればいいの？
* Exact matchとfull-text searchの使い分け方などがまだよくわからない。
* Application Packageは1つだけが普通なのか？マルチノード構成というものと、マルチテナントの考え方がよくわからない。
  * tenant=appliaction?
  * appliaction=index?
  * schema名、document type、content clusterのIDの関係がよくわかっていない

