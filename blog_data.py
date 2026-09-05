#!/usr/bin/env python3
# Aggregates all blog articles from the batch files into one ARTICLES list.
# Each article: slug, title, category, description, date, read_time, body (HTML).
from blog_data_1 import ARTICLES_1
from blog_data_2 import ARTICLES_2
from blog_data_3 import ARTICLES_3
from blog_data_4 import ARTICLES_4
from blog_data_5 import ARTICLES_5
from blog_data_6 import ARTICLES_6
from blog_data_7 import ARTICLES_7
from blog_data_8 import ARTICLES_8

ARTICLES = ARTICLES_1 + ARTICLES_2 + ARTICLES_3 + ARTICLES_4 + ARTICLES_5 + ARTICLES_6 + ARTICLES_7 + ARTICLES_8

if __name__ == "__main__":
    slugs = [a["slug"] for a in ARTICLES]
    dupes = {s for s in slugs if slugs.count(s) > 1}
    print(f"Total articles: {len(ARTICLES)}")
    print(f"Unique slugs: {len(set(slugs))}")
    if dupes:
        print("DUPLICATE SLUGS:", dupes)
    else:
        print("No duplicate slugs - OK")