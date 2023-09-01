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


## データ登録



## 検索

## まだよくわからないこと

* どんなコンポーネントが存在しているのか？
* Vespaの外でやるほうがいいか、document-processorのようなところでやるのがいいのか？
* どの設定値が動的に変更可能か？
* コンテントのIDに対して、複数のドキュメントのタイプのデータを入れた場合に、内部のデータ構造がどんな感じで構築されるのか？
* 親子関係とかJoinのようなものはあるのか？
* VS Code用の設定ファイル系のプラグインがほしい

