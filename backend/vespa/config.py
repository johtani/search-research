import dataclasses
import tomllib


@dataclasses.dataclass(frozen=True)
class Config:
    admin_url: str
    document_url: str
    application_package_path: str
    index: str


def load_config() -> Config:
    """
    設定ファイル読み込み用関数。
    ファイル名固定
    """
    # TODO ファイルのパスをどうするか？
    with open("./config/vespa/config.toml", "rb") as f:
        tmp = tomllib.load(f)
        config: Config = Config(**tmp)
    return config
