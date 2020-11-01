from CrawlRawData import CrawlerLuncher

lunch = CrawlerLuncher(project_url="https://review.opendev.org",base_dir='./opendev_abonndanned',crawl_config={'query' : '/changes/?q=status:abandoned&o=ALL_REVISIONS&o=ALL_FILES&o=ALL_COMMITS&o=MESSAGES&o=DETAILED_ACCOUNTS&o=DETAILED_LABELS'})
lunch.run_crawling()