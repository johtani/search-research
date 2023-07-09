import dataclasses
import tomllib


@dataclasses.dataclass(frozen=True)
class Config:
    """
    url: 接続文字列。「https://url」の形式の文字列
    index: インデックス名
    schema_path: スキーマファイル（schema/es/product-index-schema.json）
    """

    url: str
    index: str
    schema_path: str


def load_config() -> Config:
    """
    設定ファイル読み込み用関数。
    ファイル名固定
    """
    # TODO ファイルのパスをどうするか？
    with open("./config/es/config.toml", "rb") as f:
        tmp = tomllib.load(f)
        config: Config = Config(**tmp)
    return config
