import psycopg2, re


hostname = 'localhost'
database = 'demo'
username = 'postgres'
pwd = '1234'
port_id = 5432

conn = psycopg2.connect(
     host = hostname,
        dbname = database,
        user = username,
        password = pwd,
        port = port_id
)
cur = conn.cursor()



cur.execute(
    '''CREATE OR REPLACE FUNCTION search_from_bk(a VARCHAR, b VARCHAR)
      RETURNS SETOF book 
   AS
   $$
      SELECT * FROM book WHERE name = a AND phone = b;
   $$
   language sql;
   '''
)

cur.execute(
   '''CREATE OR REPLACE PROCEDURE insert_list_of_users(
  IN users TEXT[][]
)

LANGUAGE plpgsql

AS $$

DECLARE
  i TEXT[];

BEGIN 

   Foreach i slice 1 in array users
   LOOP
      INSERT INTO book (name, phone) VALUES (i[1], i[2]);
   END LOOP;
 

END
$$;
'''
)

cur.execute(
   '''CREATE OR REPLACE PROCEDURE insert_to_book(nm VARCHAR, phon VARCHAR)
      LANGUAGE plpgsql
      AS $$
      DECLARE 
         cnt INTEGER;
      BEGIN
         SELECT INTO cnt (SELECT count(*) FROM book WHERE name = nm);
         IF cnt > 0 THEN
            UPDATE book
               SET phone = phon
               WHERE name = nm;
         ELSE
            INSERT INTO book(name, phone) VALUES (nm, phon);
            END IF;
      END;
      $$;''')




cur.execute("""CREATE OR REPLACE PROCEDURE delete_from_book(nm VARCHAR)
LANGUAGE plpgsql
AS $$
DECLARE cnt INTEGER;
BEGIN
    SELECT into cnt (SELECT count(*) FROM book WHERE name = nm);
	IF cnt IS NOT NULL THEN
        DELETE FROM book
		WHERE name=nm;
    END IF;
END;
$$;""")

cur.execute("""CREATE OR REPLACE FUNCTION paginating(a integer, b integer)
RETURNS SETOF book
AS $$
   SELECT * FROM book
	ORDER BY name
	LIMIT a OFFSET b;
$$
language sql;""")


a = input('search\ninsert\ninsertloop\ndelete\npaginating\n')
if a == 'search':
   cur.execute("SELECT search_from_bk('John Doe', '87076002321')")
   result = cur.fetchall()
   print(result)
if a == 'insert':
   cur.execute("CALL insert_to_book('Nurtaza Nurasyl','87774545505')")
if a == 'insertloop':
  cur.execute('''CALL insert_list_of_users(ARRAY[
    ARRAY['Neymar JR', '87076052769'],
    ARRAY['Vini JR', '87079815569'],
    ARRAY['Raphinha', '87074793780']
]);''')  
if a == 'delete':
   cur.execute("CALL delete_from_book('Leo Messi')")
if a == 'paginating':
   cur.execute(
      '''SELECT * FROM paginating(6, 2);'''
   )
   print(cur.fetchall())
conn.commit()
cur.close()
conn.close()