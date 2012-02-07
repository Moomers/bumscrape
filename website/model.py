import web

db = web.database(dbn='mysql', db='bumscrape', user="bumui", pw="iamthebumui")

def get_listings(active_only = True):
    query = [
        "SELECT url, l.spider, c.last_crawled, MAX(visited) AS last_seen, MIN(visited) AS first_seen, COUNT(*) AS visits, title, price, num_tickets, posted",
        "FROM listings AS l JOIN crawls AS c ON l.spider = c.spider",
        "GROUP BY url"]

    if active_only:
        query.append("HAVING last_seen >= last_crawled")

    query.append("ORDER BY spider DESC, first_seen DESC")

    listings = db.query(query)
    return listings
