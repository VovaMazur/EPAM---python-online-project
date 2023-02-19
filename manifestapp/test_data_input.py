"""Script to populate database with the test data"""
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="app",
  password="password",
  database="manifestapp"
)

mycursor = mydb.cursor()

# first table
SQL = "INSERT INTO passengers (id, fname, lname, seatno, address, " \
      "dob, status) VALUES (%s, %s, %s, %s, %s, %s, %s)"

val = [
    ('1', 'Ben', 'Stone', '12C', 'NY, Some place', '1980-01-23', 'live'),
    ('2', 'Mac', 'Stone', '12A', 'NY, Some other place', '1985-04-19', 'live'),
    ('3', 'Kel', 'Stone', '12B', 'NY, Some place', '2000-07-15', 'live'),
    ('4', 'Mike', 'Jordan', '20F', None, None, 'unknown'),
    ('5', 'Grace', 'Perry', '31A', 'FL, Hot place & cool', '1984-04-03', 'live')]

mycursor.executemany(SQL, val)
mydb.commit()

print('Table passengers > ', mycursor.rowcount, "was inserted.")


# second table

SQL = "INSERT INTO events (id, date, passengerID, geo_location, " \
      "description, status, other_pass) VALUES (%s, %s, %s, %s, %s, %s, %s)"

val = [
    ('1', '2022-06-03', '1', '-25.344, 131.031', 'I see the volcano errupting', 'unknown', '2,3'),
    ('2', '2022-08-08', '4', '-10.344, 140.031', 'I see the starts shining', 'success', None),
    ('3', '2022-10-10', '5', '-15.344, 120.031',
     'I see the 2 dogs but I feel there are much more', 'failure', '1')
       ]

mycursor.executemany(SQL, val)
mydb.commit()

print('Table events > ', mycursor.rowcount, "was inserted.")
