import web

db = web.database(dbn='mysql', db='bumscrape', user="bumui", pw="iamthebumui")

def get_listings(active_only):
    query = [
        "SELECT url, l.spider, c.last_crawled, max(visited) as last_seen, date_format(MAX(visited), '%c/%e') AS last_seen_fmt, min(visited) as first_seen, date_format(MIN(visited), '%c/%e') AS first_seen_fmt, COUNT(*) AS visits, title, concat('$', format(price, 2)) AS price, num_tickets, posted",
        "FROM listings AS l JOIN crawls AS c ON l.spider = c.spider",
        "GROUP BY url"]

    query.append("ORDER BY spider DESC, first_seen DESC")

    if active_only:
        query.append("HAVING last_seen >= last_crawled")

    listings = db.query(" ".join(query))
    return listings
