import os
import pudb
import psycopg2
import urlparse

#for heroku:
#urllib.parse.uses_netloc.append("postgres")
#url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
url = urlparse.urlparse("postgres://pcqikrsnnyjuqa:-lyhpVlpycUQlf_HwyzrA1a0ep@ec2-54-83-46-91.compute-1.amazonaws.com:5432/d6idunnmsvk671")

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

output  = "DATABASE_URL value:" +str(url) +"\n"
output += "scheme: " + str(url.scheme) +"\n"
output += "netloc: " + str(url.netloc) +"\n"
output += "  path: " + str(url.path[1:]) +"\n"
output += "  user: " + str(url.username) +"\n"
output += "passwd: " + str(url.password) +"\n"

conn = psycopg2.connect(
database=url.path[1:],
user=url.username,
password=url.password,
host=url.hostname,
port=url.port
)

print output

def insert_email_and_zip(zip_code, email):
    #pu.db
    cur = conn.cursor()
    query = "INSERT INTO weather_users (zip_code, email) VALUES (%s, %s);"
    data = (zip_code, email)
    cur.execute(query, data)
    conn.commit()

def query_hits_and_url_for_link(key):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        key = str(key)
        cur.execute("SELECT * FROM link WHERE key=?", (key,))
        link_data = cur.fetchall()
        print link_data
        return link_data

def update_hits(key):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE link SET hits = (hits + 1) WHERE key=key")
        con.commit()