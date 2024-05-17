# Oricon Ranking Getter

## Overview
- オリコンが発表する週刊シングル・アルバムランキングを取得するツール
- Tool to obtain weekly rankings published by Oricon.
- Only supports weekly rankings for the moment
- Able to print the output into JSON/CSV format for various uses.

## How to use
To get the output directly printed in the console:

```bash
python orikon.py  -t cos -y 2024 -m 4
```

To redirect the output to a file:

```
python orikon.py  -t cos -y 2024 -m -o file.json -f json
```

## Requirements
- Python3.7
- pip install beautifulsoup4
- pip install request

## To do
- implement support for all date types (daily/monthly/yearly)
- support for multiple pages of a ranking
- ability to select specified week from a month
- make file output more elegant
- make the argparser more rigid
- write documentation
- more robust error handling

