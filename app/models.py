import os
import pudb
import psycopg2
import urlparse
from werkzeug import generate_password_hash, check_password_hash

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

'''
d6idunnmsvk671=> CREATE TABLE users (
d6idunnmsvk671(> id SERIAL NOT NULL,
d6idunnmsvk671(> firstname TEXT NOT NULL,
d6idunnmsvk671(> lastname TEXT NOT NULL,
d6idunnmsvk671(> email TEXT NOT NULL,
d6idunnmsvk671(> pwdhash TEXT NOT NULL,
d6idunnmsvk671(> zipcode INT NOT NULL);
'''


class User(object):

    def __init__(self, firstname, lastname, email, password, zipcode):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.set_password(password)
        self.zipcode = zipcode

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    def add_to_db(self):
        #can this be a try/except block?
        cur = conn.cursor()
        query = "INSERT INTO users (firstname, lastname, email, pwdhash, zipcode) VALUES (%s, %s, %s, %s, %s);"
        data = (self.firstname, self.lastname, self.email, self.pwdhash, self.zipcode)
        cur.execute(query, data)
        conn.commit()

    def check_for_duplicate_email(self):
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = %(email)s", {'email': self.email})
        email = cur.fetchone()
        if email is None:
            print "true!"
            return True
        else:
            print "false!"
            return False

    @staticmethod
    #looks up user in postgres by email, returns new user object
    def lookup_email(email):
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM users WHERE email = %(email)s", {'email': email})
            sql_user_data = cur.fetchone()
            new_user = User(sql_user_data[1], sql_user_data[2], sql_user_data[3], sql_user_data[4], sql_user_data[5])
            #set pwdhash to correct value
            new_user.pwdhash = sql_user_data[4]
            return new_user
        except:
            return None


'''
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
'''