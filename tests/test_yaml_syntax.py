from pathlib import Path

import pytest
from ruamel.yaml import YAML

YAML_DIR = Path(__file__).resolve().parent.parent / "src" / "netbox_initializers" / "initializers" / "yaml"

yaml_files = sorted(YAML_DIR.glob("*.yml"))


@pytest.mark.parametrize("yaml_path", yaml_files, ids=[f.name for f in yaml_files])
def test_yaml_syntax(yaml_path: Path) -> None:
    yaml = YAML(typ="safe")
    with yaml_path.open("r", encoding="utf-8") as stream:
        data: object = yaml.load(stream)  # pyright: ignore[reportAny]

    # Initializer YAML files should contain either a list of items, a dict, or be empty
    assert data is None or isinstance(data, (list, dict)), (
        f"{yaml_path.name} must parse to None, list, or dict, got {type(data).__name__}"
    )

    # If it's a list, every item should be a dict
    if isinstance(data, list):
        items: list[object] = data
        for idx, item in enumerate(items):
            assert isinstance(item, dict), f"{yaml_path.name}[{idx}] must be a dict, got {type(item).__name__}"
