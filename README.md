# Irasutoya Scraper
Program to scrape all the illustrations on [いらすとや](https://www.irasutoya.com/).

The responsibility of scraping the website lies in the users running the program. Please read <https://www.irasutoya.com/p/terms.html>.

# Installation
- Python 3.10
- scrapy (2.11.1)
- beautifulsoup4 (4.12.3)
- pillow (10.3.0)
- python-dotenv (1.0.1)
- SQLAlchemy (2.0.29)
- psycopg2 (2.9.9)

# Run
To scrape the entire website, run commands in following order:

## 1. 詳細カテゴリー
```sh
scrapy crawl irasutoya__shosai_categories -O out/irasutoya/shosai_categories.csv
```

## 2. irasuto lists
Scrape the lists corresponding to each 詳細カテゴリー by reading `shosai_categories.csv` produced in previous step.
```sh
scrapy crawl irasutoya__label_lists \
    -a shosai_categories_csv=out/irasutoya/shosai_categories.csv \
    -O out/irasutoya/label_lists_categories.csv 2>&1 | tee -a logs/label_lists.txt
```
TODO dump results to an actual database

## 3. irasutos
```sh
#!/bin/sh
export DB_CONNECTION_STRING="sqlite:///out/irasutoya/irasutos.sqlite"
scrapy crawl irasutoya__irasutos \
    -a irasuto_lists_csv=out/irasutoya/label_lists_categories.csv \
    -s USE_DB=1
```
Can also modify `IRASUTOYA_IRASUTOS_SAVE_DIR` in `settings` to change the locations wherein images are saved.

## 4. category details
Collect additional information in regards to categories of irasutos. Scrape hierarchical category information.
```sh
scrapy crawl irasutoya__category_details -a json_save_path=out/irasutoya/category_details.json
```

