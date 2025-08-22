import yaml
from pathlib import Path
import sys
from utils import FetchAllData, DivideTLEs


if __name__ == '__main__':
    config_file = Path("./config.yaml")
    if not config_file.exists():
        sys.exit("config.yaml 未找到")
    
    with open(config_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    FetchAllData(config)

    folder = Path('./data')
    fileList = [p for p in folder.iterdir() if p.suffix == '.tle']
    for file in fileList:
        DivideTLEs(file)
