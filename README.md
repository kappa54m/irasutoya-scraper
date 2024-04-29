# Installation
- Python 3.10
- scrapy (2.11.1)
- beautifulsoup4 (4.12.3)
- pillow (10.3.0)
- python-dotenv (1.0.1)

# Run

## [いらすとや](https://www.irasutoya.com/)
### 1. 詳細カテゴリー
```sh
scrapy crawl irasutoya__shosai_categories -O out/irasutoya/shosai_categories.csv
```

### 2. irasuto lists
Scrape the lists corresponding to each 詳細カテゴリー by reading `shosai_categories.csv` produced in previous step.
```sh
scrapy crawl irasutoya__label_lists \
    -a shosai_categories_csv=out/irasutoya/shosai_categories.csv \
    -O out/irasutoya/label_lists_categories.csv 2>&1 | tee -a logs/label_lists.txt
```
TODO dump results to an actual database

