from cassandra.cluster import Cluster
import time

'''
DPB - 11. cvičení Cassandra

Use case: Discord server - reálně používáno pro zprávy, zde pouze zjednodušená varianta.

Instalace python driveru: pip install cassandra-driver

V tomto cvičení se budou následující úlohy řešit s využitím DataStax driveru pro Cassandru.
Dokumentaci lze nalézt zde: https://docs.datastax.com/en/developer/python-driver/3.25/getting_started/


Optimální řešení (nepovinné) - pokud něco v db vytváříme, tak první kontrolujeme, zda to již neexistuje.


Pro uživatele PyCharmu:

Pokud chcete zvýraznění syntaxe, tak po napsání prvního dotazu se Vám u něj objeví žlutá žárovka, ta umožňuje vybrat 
jazyk pro tento projekt -> vyberte Apache Cassandra a poté Vám nabídne instalaci rozšíření pro tento typ db.
Zvýraznění občas nefunguje pro příkaz CREATE KEYSPACE.

Také je možné do PyCharmu připojit databázi -> v pravé svislé liště najděte Database a připojte si lokální Cassandru.
Řešení cvičení chceme s využitím DataStax driveru, ale s integrovaným nástrojem pro databázi si můžete pomoct sestavit
příslušně příkazy.


Pokud se Vám nedaří připojit se ke Cassandře v Dockeru, zkuste smazat kontejner a znovu spustit:

docker run --name dpb_cassandra -p 127.0.0.1:9042:9042 -p 127.0.0.1:9160:9160 -d cassandra:latest

'''


def print_delimiter(n):
    print('\n', '#' * 10, 'Úloha', n, '#' * 10, '\n')


def print_result(result):
    for row in result:
        print(row)


cluster = Cluster()  # automaticky se připojí k localhostu na port 9042
session = cluster.connect()

"""
1. Vytvořte keyspace 'dc' a přepněte se do něj (SimpleStrategy, replication_factor 1)
"""

print_delimiter(1)

# create keyspace dc
# with replication = {'class': 'SimpleStrategy', 'replication_factor': 1}

session.execute("""
    CREATE KEYSPACE IF NOT EXISTS dc
    WITH replication = {
        'class': 'SimpleStrategy',
        'replication_factor': '1'
    };
""")
session.set_keyspace('dc')

"""
2. V csv souboru message_db jsou poskytnuta data pro cvičení. V prvním řádku naleznete názvy sloupců.
   Vytvořte tabulku messages - zvolte vhodné datové typy (time bude timestamp)
   Primárním klíčem bude room_id a time
   Data chceme mít seřazené podle času, abychom mohli rychle získat poslední zprávy

   Jako id v této úloze zvolíme i time - zdůvodněte, proč by se v praxi time jako id neměl používat.

   Pokud potřebujeme použít čas, tak se v praxi používá typ timeuuid nebo speciální identifikátor, tzv. Snowflake ID
   (https://en.wikipedia.org/wiki/Snowflake_ID). Není potřeba řešit v tomto cvičení.
"""

print_delimiter(2)

# import data from message_db.csv
# Keyspace and table names
keyspace = 'dc'
table = 'message'

# Create the keyspace if it doesn't exist
session.execute(f"CREATE KEYSPACE IF NOT EXISTS {keyspace} WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': '1'}}")
session.set_keyspace(keyspace)

# Create the table
create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table} (
        room_id INT,
        speaker_id INT,
        time timestamp,
        message text,
        PRIMARY KEY (time)
    );
"""
session.execute(create_table_query)

"""for line in file:
        values = line.strip().split(';')
        insert_query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES (?, ?, ?, ?);"
        session.execute(insert_query, tuple(values))
3. Do tabulky messages importujte message_db.csv
   COPY není možné spustit pomocí DataStax driveru ( 'copy' is a cqlsh (shell) command rather than a CQL (protocol) command)
   -> 2 možnosti:
      a) Nakopírovat csv do kontejneru a spustit COPY příkaz v cqlsh konzoli uvnitř dockeru
      b) Napsat import v Pythonu - otevření csv a INSERT dat
CSV soubor může obsahovat chybné řádky - COPY příkaz automaticky přeskočí řádky, které se nepovedlo správně parsovat
"""

print_delimiter(3)

# Read the CSV file and insert data into the table
csv_file = 'message_db.csv'  # Replace with the actual path to your CSV file

with open(csv_file, 'r') as file:
    header = file.readline().strip()
    columns = header.split(';')

    for line in file:
        values = line.strip().split(';')
        if len(values) != len(columns):
            print(f"Skipping line: {line}")
            continue

        try:
            insert_query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES (?, ?, ?, ?);"
            params = {column: value for column, value in zip(columns, values)}
            session.execute(insert_query, params)
        except Exception as e:
            print(f"Error inserting data: {e}")
            continue



"""
4. Kontrola importu - vypište 1 zprávu
"""

print_delimiter(4)

"""
5. Vypište posledních 5 zpráv v místnosti 1 odeslaných uživatelem 2
    Nápověda 1: Sekundární index (viz přednáška) 
    Nápověda 2: Data jsou řazena již při vkládání
"""

print_delimiter(5)

"""
6. Vypište počet zpráv odeslaných uživatelem 2 v místnosti 1
"""

print_delimiter(6)

"""
7. Vypište počet zpráv v každé místnosti
"""

print_delimiter(7)

"""
8. Vypište id všech místností (3 hodnoty)
"""

print_delimiter(8)

"""
Bonusové úlohy:

1. Pro textovou analýzu chcete poskytovat anonymizovaná textová data. Vytvořte Materialized View pro tabulku messages,
který bude obsahovat pouze čas, room_id a zprávu.

Vypište jeden výsledek z vytvořeného view

Před začátkem řešení je potřeba jít do souboru cassandra.yaml uvnitř docker kontejneru a nastavit enable_materialized_views=true

docker exec -it dpb_cassandra bash
sed -i -r 's/enable_materialized_views: false/enable_materialized_views: true/' /etc/cassandra/cassandra.yaml

Poté restartovat kontejner

2. Chceme vytvořit funkci (UDF), která při výběru dat vrátí navíc příznak, zda vybraný text obsahuje nevhodný výraz.

Vyberte jeden výraz (nemusí být nevhodný:), vytvořte a otestujte Vaši funkci.

Potřeba nastavit enable_user_defined_functions=true v cassandra.yaml

sed -i -r 's/enable_user_defined_functions: false/enable_user_defined_functions: true/' /etc/cassandra/cassandra.yaml

3. Zjistěte čas odeslání nejnovější a nejstarší zprávy.

4. Zjistěte délku nejkratší a nejdelší zprávy na serveru.	

5. Pro každého uživatele zjistěte průměrnou délku zprávy.		

V celém cvičení by nemělo být použito ALLOW FILTERING.
"""
cluster.shutdown()
#%%



