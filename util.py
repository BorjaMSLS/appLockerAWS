import psycopg2


class DatabaseConnection:
    def __init__(self, host, database, user, password):
        self.connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        self.cursor = self.connection.cursor()

    def query(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()


def createUsersAPI(api_name, api_email):
    # Connect to the database
    conn = psycopg2.connect(
        host="lockerdbdev.c34qmeqy6kui.eu-north-1.rds.amazonaws.com",
        database="postgres",
        user="borja_db",
        password="Extremoduro85!"
    )

    # Create a cursor
    cur = conn.cursor()

    # Collect the data
    name = api_name
    email = api_email

    # Build the SQL insert statement
    insert_stmt = "INSERT INTO users (name, email) VALUES (%s, %s)"

    # Execute the insert statement
    cur.execute(insert_stmt, (name, email))

    # Commit the transaction
    if not conn.commit():
        print('Inserted successfully in the DB')
        cur.close()
        conn.close()
        return "User created"

    # Close the cursor and connection
    cur.close()
    conn.close()
    return "Error inserting in DB"

def getUsersAPI():
    conn = DatabaseConnection("lockerdbdev.c34qmeqy6kui.eu-north-1.rds.amazonaws.com", "postgres", "borja_db", "Extremoduro85!")
    results = conn.query("SELECT * FROM users")
    conn.close()
    users = []
    for row in results:
        user = {
            "id": row[0],
            "name": row[1],
            "email": row[2]
            # add other columns here
        }
        users.append(user)
    return users


def getLockersAPI(center):
    conn = DatabaseConnection("lockerdbdev.c34qmeqy6kui.eu-north-1.rds.amazonaws.com", "postgres", "borja_db", "Extremoduro85!")
    results = conn.query("SELECT * FROM lockers l LEFT JOIN users u ON l.owner = u.id WHERE l.center ='" + center + "' ORDER BY l.id")
    conn.close()
    lockers = []
    for row in results:
        locker = {
            "id": row[0],
            "center": row[1],
            "owner_id": row[2],
            "owner_name": row[5],
            "status": row[3]
            # add other columns here
        }
        lockers.append(locker)

    return lockers

def findByEmailAPI(search):
    conn = DatabaseConnection("lockerdbdev.c34qmeqy6kui.eu-north-1.rds.amazonaws.com", "postgres", "borja_db", "Extremoduro85!")
    results = conn.query("SELECT * FROM users u WHERE u.email LIKE'%" + search + "%' ORDER BY u.id")
    conn.close()
    users = []
    for row in results:
        user = {
            "id": row[0],
            "name": row[1],
            "email": row[2]
            # add other columns here
        }
        users.append(user)

    return users

def getLockerAttAPI(locker_id):
    conn = DatabaseConnection("lockerdbdev.c34qmeqy6kui.eu-north-1.rds.amazonaws.com", "postgres", "borja_db", "Extremoduro85!")
    if conn.query("SELECT * FROM lockers l WHERE l.id =" + locker_id):
        results = conn.query(
            "SELECT * FROM lockers l LEFT JOIN users u ON l.owner = u.id WHERE l.id ='" + locker_id + "' ORDER BY l.id")

        conn.close()
        lockers = []
        for row in results:
            locker = {
                "id": row[0],
                "center": row[1],
                "owner_id": row[2],
                "owner_name": row[5],
                "status": row[3]
                # add other columns here
            }
            lockers.append(locker)

        return lockers
    else:
        return "Locker does not exist"

def getPersonLockersAPI(pers_email):
    conn = DatabaseConnection("lockerdbdev.c34qmeqy6kui.eu-north-1.rds.amazonaws.com", "postgres", "borja_db", "Extremoduro85!")
    results = conn.query("SELECT * FROM lockers l JOIN facilities f ON l.center = f.id JOIN users u ON l.owner = u.id WHERE u.email ='" + pers_email + "' ORDER BY l.id")
    conn.close()
    lockers = []
    for row in results:
        locker = {
            "id": row[0],
            "center": row[1],
            "center_name": row[5],
            "owner_id": row[2],
            "status": row[3]
            # add other columns here
        }
        lockers.append(locker)

    return lockers

def authenticateAPI(email, pwd):
    conn2 = DatabaseConnection("lockerdbdev.c34qmeqy6kui.eu-north-1.rds.amazonaws.com", "postgres", "borja_db", "Extremoduro85!")
    if conn2.query("SELECT * FROM staff s WHERE s.email ='" + email + "'"):
        res_pwd = conn2.query("SELECT * FROM staff s WHERE s.email ='" + email + "'")

        for row in res_pwd:
            pwd_str = row[3]

        if pwd == pwd_str:
            return 'Staff access granted'
        else:
            return 'Access denied: wrong credentials'

    elif conn2.query("SELECT * FROM users u WHERE u.email ='" + email + "'"):
        res_pwd = conn2.query("SELECT * FROM users u WHERE u.email ='" + email + "'")
        for row in res_pwd:
            pwd_str = row[3]

        if pwd == pwd_str:
            return 'User access granted'
        else:
            return 'Access denied: wrong credentials'
    else:
        return 'Person does not exist'


def assignLockerAPI(in_user_id, in_locker):
    user_id = in_user_id
    locker_id = in_locker

    conn2 = DatabaseConnection("lockerdbdev.c34qmeqy6kui.eu-north-1.rds.amazonaws.com", "postgres", "borja_db", "Extremoduro85!")
    if conn2.query("SELECT * FROM users u WHERE u.id =" + user_id ):
        result_id_list = conn2.query("SELECT * FROM users u WHERE u.id =" + user_id )
        tmp = str(result_id_list[0])
        print(tmp)
        user_id_str = tmp[1:tmp.find(",")]

        # Connect to the database
        conn = psycopg2.connect(
            host="lockerdbdev.c34qmeqy6kui.eu-north-1.rds.amazonaws.com",
            database="postgres",
            user="borja_db",
            password="Extremoduro85!"
        )

        # Create a cursor
        cur = conn.cursor()

        # Collect the data

        # Build the SQL insert statement
        if locker_id:
            insert_stmt_assign = "UPDATE lockers SET owner = %s, status = %s WHERE id=" + locker_id

        else:
            available_lockers = conn2.query("SELECT * FROM lockers l WHERE l.status ='FREE'")
            tmp1 = str(available_lockers[0])
            print(tmp1)
            locker_id = tmp1[1:tmp.find(",")]
            print(locker_id)
            insert_stmt_assign = "UPDATE lockers SET owner = %s, status = %s WHERE id=" + locker_id

        owner = user_id_str
        status = 'RENTED'

        # Execute the insert statement
        cur.execute(insert_stmt_assign, (owner, status))

        # Commit the transaction
        if not conn.commit():
            print('Inserted successfully in the DB')

        # Close the cursor and connection
        cur.close()
        conn.close()

        return "Locker successfully assigned"
    else:
        return "Wrong data provided"

def releaseLockerAPI(in_locker):

    locker_id = in_locker

    conn2 = DatabaseConnection("lockerdbdev.c34qmeqy6kui.eu-north-1.rds.amazonaws.com", "postgres", "borja_db", "Extremoduro85!")
    if conn2.query("SELECT * FROM lockers l WHERE l.id ='" + locker_id + "' AND l.status ='RENTED'"):



        # Connect to the database
        conn = psycopg2.connect(
            host="lockerdbdev.c34qmeqy6kui.eu-north-1.rds.amazonaws.com",
            database="postgres",
            user="borja_db",
            password="Extremoduro85!"
        )

        # Create a cursor
        cur = conn.cursor()

        # Collect the data

        locker_id = int(in_locker)
        insert_stmt_assign = "UPDATE lockers SET owner = NULL, status = %s WHERE id=%s"
        status = 'FREE'
        cur.execute(insert_stmt_assign, (status, locker_id))

        # Commit the transaction
        if not conn.commit():
            print('Inserted successfully in the DB')

        # Close the cursor and connection
        cur.close()
        conn.close()
        return "Locker released"

    else:
        return "Invalid locker ID"


def createFacilityAPI(in_name, in_address, in_city, in_country, in_capacity):
    # Connect to the database
    conn = psycopg2.connect(
        host="lockerdbdev.c34qmeqy6kui.eu-north-1.rds.amazonaws.com",
        database="postgres",
        user="borja_db",
        password="Extremoduro85!"
    )

    # Create a cursor
    cur = conn.cursor()

    # Collect the data
    name = in_name
    address = in_address
    city = in_city
    country = in_country
    capacity = in_capacity

    # Build the SQL insert statement
    insert_stmt = "INSERT INTO facilities (name, address, city, country) VALUES (%s, %s, %s, %s)"

    # Execute the insert statement
    cur.execute(insert_stmt, (name, address, city, country))

    # Commit the transaction
    if not conn.commit():
        print('Inserted successfully in the DB')

    # Close the cursor and connection
    cur.close()
    conn.close()

    conn2 = DatabaseConnection("lockerdbdev.c34qmeqy6kui.eu-north-1.rds.amazonaws.com", "postgres", "borja_db", "Extremoduro85!")
    result_id_list = conn2.query("SELECT fa.id FROM facilities fa WHERE fa.name =" + "'" + name + "'")
    tmp = str(result_id_list[0])
    center_id_str = tmp[1:-2]

    conn3 = psycopg2.connect(
        host="lockerdbdev.c34qmeqy6kui.eu-north-1.rds.amazonaws.com",
        database="postgres",
        user="borja_db",
        password="Extremoduro85!"
    )

    # Create a cursor
    cur = conn3.cursor()

    # Collect the data
    center = center_id_str
    owner = None
    status_init = "FREE"

    # Build the SQL insert statement
    for i in range(int(in_capacity)):
        insert_stmt2 = "INSERT INTO lockers (center, owner,status) VALUES (%s, %s, %s)"

        # Execute the insert statement
        cur.execute(insert_stmt2, (center, owner, status_init))

        # Commit the transaction
        if not conn3.commit():
            print('Inserted successfully in the DB')

    # Close the cursor and connection
    cur.close()
    conn3.close()
    return "Facility successfully created"
