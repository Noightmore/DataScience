import pymongo

from init import collection
from datetime import datetime

print(collection.find_one())

'''
DPB - 5. Cvičení

Implementujte jednotlivé body pomocí PyMongo knihovny - rozhraní je téměř stejné jako v Mongo shellu.
Před testováním Vašich řešení si nezapomeňte zapnout Mongo v Dockeru.

Pro pomoc je možné např. použít https://www.w3schools.com/python/python_mongodb_getstarted.asp

Funkce find vrací kurzor - pro vypsání výsledku je potřeba pomocí foru iterovat nad kurzorem:

cursor = collection.find(...)
for restaurant in cursor:
    print(restaurant) # případně print(restaurant['name'])

Všechny výsledky limitujte na 10 záznamů. Nepoužívejte české názvy proměnných!
'''


def print_delimiter(n):
    print('\n', '#' * 10, 'Úloha', n, '#' * 10, '\n')


def main():
    # 1. Vypsání všech restaurací
    print_delimiter(1)

    cursor = collection.find().limit(10)
    for restaurant in cursor:
        print(restaurant)

    # 2. Vypsání všech restaurací - pouze názvů, abecedně seřazených
    print_delimiter(2)
    cursor = collection.find({}, {'name': 1, '_id': 0}).sort('name', 1).limit(20)
    for restaurant in cursor:
        print(restaurant)

    # 3. Vypsání pouze 10 záznamů z předchozího dotazu
    print_delimiter(3)
    cursor = collection.find({}, {'name': 1, '_id': 0}).sort('name', 1).limit(10)
    for restaurant in cursor:
        print(restaurant)

    # 4. Zobrazte dalších 10 záznamů
    print_delimiter(4)
    cursor = collection.find({}, {'name': 1, '_id': 0}).sort('name', 1).skip(10).limit(10)
    for restaurant in cursor:
        print(restaurant)

    # 5. #Vypsání restaurací ve čtvrti Bronx (čtvrť = borough)
    print_delimiter(5)
    cursor = collection.find({'borough': 'Bronx'}).limit(10)
    for restaurant in cursor:
        print(restaurant)

    # 6. Vypsání restaurací, jejichž název začíná na písmeno M
    print_delimiter(6)
    cursor = collection.find({'name': {'$regex': '^M'}}).limit(10)
    for restaurant in cursor:
        print(restaurant)

    # 7. Vypsání restaurací, které mají skóre větší než 80
    print_delimiter(7)
    cursor = collection.find({'grades.score': {'$gt': 80}}).limit(10)
    for restaurant in cursor:
        print(restaurant)

    # 8. Vypsání restaurací, které mají skóre mezi 80 a 90
    print_delimiter(8)
    cursor = collection.find({"grades": {"$elemMatch": {"score": {"$gt": 80, "$lt": 90}}}}).limit(10)
    for restaurant in cursor:
        print(restaurant)

    '''
    Bonusové úlohy:
    '''

    # 9. Vypsání všech restaurací, které mají skóre mezi 80 a 90 a zároveň nevaří americkou (American ) kuchyni
    print_delimiter(9)
    cursor = collection.find({
        "grades": {"$elemMatch": {"score": {"$gt": 80, "$lt": 90}}},
        "cuisine": {"$ne": "American "}
    }).limit(10)

    for restaurant in cursor:
        print(restaurant)

    # 10. Vypsání všech restaurací, které mají alespoň osm hodnocení
    print_delimiter(10)
    cursor = collection.find({'grades': {'$size': 8}}).limit(10)
    for restaurant in cursor:
        print(restaurant)

    # 11. Vypsání všech restaurací, které mají alespoň jedno hodnocení z roku 2014
    print_delimiter(11)
    start_date = datetime(2014, 1, 1)
    end_date = datetime(2015, 1, 1)

    query = {"grades": {"$elemMatch": {"date": {"$gte": start_date, "$lt": end_date}}}}

    cursor = collection.find(query).limit(10)

    for restaurant in cursor:
        print(restaurant)

    '''
    V této části budete opět vytvářet vlastní restauraci.
    
    Řešení:
    Vytvořte si vaši restauraci pomocí slovníku a poté ji vložte do DB.
    restaurant = {
        ...
    }
    '''

    # 12. Uložte novou restauraci (stačí vyplnit název a adresu)
    print_delimiter(12)
    new_restaurant = {
        "address": {
            "building": "1234",
            "coord": [-73.987414, 40.757803],
            "street": "Broadway",
            "zipcode": "10001"
        },
        "borough": "Manhattan",
        "cuisine": "Italian",
        "grades": [
            {"date": datetime.utcnow(), "grade": "A", "score": 12},
            {"date": datetime.utcnow(), "grade": "B", "score": 8},
            {"date": datetime.utcnow(), "grade": "C", "score": 4}
        ],
        "name": "Mario's Pizza",
        "restaurant_id": "12345678"
    }

    collection.insert_one(new_restaurant)

    # 13. Vypište svoji restauraci
    print_delimiter(13)
    print("New restaurant added with ID:", new_restaurant["_id"])

    # 14. Aktualizujte svoji restauraci - změňte libovolně název
    print_delimiter(14)
    query = {"restaurant_id": "12345678"}
    new_values = {"$set": {"name": "Mario's Pasta"}}

    result = collection.update_one(query, new_values)

    print(result.modified_count, "documents updated.")


# 15. Smažte svoji restauraci
    # 15.1 pomocí id (delete_one)
    # 15.2 pomocí prvního nebo druhého názvu (delete_many, využití or)
    print_delimiter(15)
    query = {"restaurant_id": "12345678"}

    result = collection.delete_one(query)

    print(result.deleted_count, "document deleted.")


    '''
    Poslední částí tohoto cvičení je vytvoření jednoduchého indexu.
    
    Použijte např. 3. úlohu s vyhledáváním čtvrtě Bronx. První použijte Váš již vytvořený dotaz a na výsledek použijte:
    
    cursor.explain()['executionStats'] - výsledek si vypište na výstup a všimněte si položky 'totalDocsExamined'
    
    Poté vytvořte index na 'borough', zopakujte dotaz a porovnejte hodnoty 'totalDocsExamined'.
    
    S řešením pomůže https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.create_index
    '''
    print_delimiter(16)
    cursor = collection.find({'borough': 'Bronx'}).limit(10).explain()['executionStats']
    print(cursor)
    index_name = "borough_index"
    result = collection.create_index([("borough", pymongo.ASCENDING)], name=index_name)

    print("Index created:", result)


if __name__ == '__main__':
    main()

