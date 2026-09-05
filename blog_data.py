#!/usr/bin/env python3
# Aggregates all blog articles from the batch files into one ARTICLES list.
# Each article: slug, title, category, description, date, read_time, body (HTML).
from blog_data_1 import ARTICLES_1
from blog_data_2 import ARTICLES_2

ARTICLES = ARTICLES_1 + ARTICLES_2

if __name__ == "__main__":
    slugs = [a["slug"] for a in ARTICLES]
    dupes = {s for s in slugs if slugs.count(s) > 1}
    print(f"Total articles: {len(ARTICLES)}")
    print(f"Unique slugs: {len(set(slugs))}")
    if dupes:
        print("DUPLICATE SLUGS:", dupes)
    else:
        print("No duplicate slugs - OK")