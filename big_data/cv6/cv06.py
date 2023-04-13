

'''
DPB - 6. cvičení - Agregační roura a Map-Reduce

V tomto cvičení si můžete vybrat, zda ho budete řešit v Mongo shellu nebo pomocí PyMongo knihovny.

Před testováním Vašich řešení si nezapomeňte zapnout Mongo v Dockeru - používáme stejná data jako v minulých cvičeních.

Pro pomoc je možné např. použít https://api.mongodb.com/python/current/examples/aggregation.html a přednášku.

Všechny výsledky limitujte na 10 záznamů. Nepoužívejte české názvy proměnných!

Struktura záznamu v db:
{
  "address": {
     "building": "1007",
     "coord": [ -73.856077, 40.848447 ],
     "street": "Morris Park Ave",
     "zipcode": "10462"
  },
  "borough": "Bronx",
  "cuisine": "Bakery",
  "grades": [
     { "date": { "$date": 1393804800000 }, "grade": "A", "score": 2 },
     { "date": { "$date": 1378857600000 }, "grade": "A", "score": 6 },
     { "date": { "$date": 1358985600000 }, "grade": "A", "score": 10 },
     { "date": { "$date": 1322006400000 }, "grade": "A", "score": 9 },
     { "date": { "$date": 1299715200000 }, "grade": "B", "score": 14 }
  ],
  "name": "Morris Park Bake Shop",
  "restaurant_id": "30075445"
}
'''


def print_delimiter(n):
    print('\n', '#' * 10, 'Úloha', n, '#' * 10, '\n')


def main():
    '''
    Agregační roura
    Zjistěte počet restaurací pro každé PSČ (zipcode)
     a) seřaďte podle zipcode vzestupně
     b) seřaďte podle počtu restaurací sestupně
    Výpis limitujte na 10 záznamů a k provedení použijte collection.aggregate(...)
    '''
    print_delimiter('1 a)')
    pipeline = [
        {
            "$group": {
                "_id": "$address.zipcode",
                "count": { "$sum": 1 }
            }
        },
        {
            "$sort": { "count": -1 }
        },
        {
            "$limit": 10
        }
    ]

    result = list(collection.aggregate(pipeline))

    for document in result:
        print(f"{document['_id']}: {document['count']}")

    print_delimiter('1 b)')
    pipeline = [
        {
            "$group": {
                "_id": "$address.zipcode",
                "count": { "$sum": 1 }
            }
        },
        {
            "$sort": { "count": 1 }
        },
        {
            "$limit": 10
        }
    ]

    result = list(collection.aggregate(pipeline))

    for document in result:
        print(f"{document['_id']}: {document['count']}")

    '''
    Agregační roura
    
    Restaurace obsahují pole grades, kde jsou jednotlivá hodnocení. Vypište průměrné score pro každou hodnotu grade.
    V agregaci vynechte grade pro hodnotu "Not Yet Graded" (místo A, B atd. se může vyskytovat tento řetězec).
    
    '''
    print_delimiter(2)
    pipeline = [
        {
            "$match": {
                "grades.grade": { "$ne": "Not Yet Graded" }
            }
        },
        {
            "$project": {
                "name": 1,
                "avg_score": {
                    "$avg": "$grades.score"
                }
            }
        },
        {
            "$sort": {
                "avg_score": -1
            }
        },
        {
            "$limit": 10
        }
    ]

    result = list(collection.aggregate(pipeline))

    for document in result:
        print(f"{document['name']}: {document['avg_score']}")

    # bonus
    print_delimiter('bonus')
    pipeline = [
        {
            "$unwind": "$grades"
        },
        {
            "$match": {
                "grades.grade": "A"
            }
        },
        {
            "$group": {
                "_id": "$_id",
                "name": { "$first": "$name" },
                "count": { "$sum": 1 }
            }
        },
        {
            "$sort": {
                "count": -1
            }
        },
        {
            "$limit": 10
        }
    ]

    result = list(collection.aggregate(pipeline))

    for document in result:
        print(f"{document['name']}: {document['count']} A grades")

    print_delimiter('bonus 2')
    pipeline = [
        {"$unwind": "$grades"},
        {"$match": {"grades.grade": "A"}},
        {"$group": {"_id": {"cuisine": "$cuisine", "restaurant_id": "$restaurant_id"},
                    "count": {"$sum": 1}}},
        {"$sort": {"_id.cuisine": 1, "count": -1}},
        {"$group": {"_id": "$_id.cuisine",
                    "best_restaurant": {"$first": "$_id.restaurant_id"},
                    "max_count": {"$first": "$count"}}},
        {"$project": {"_id": 0, "cuisine": "$_id", "best_restaurant": 1, "max_count": 1}},
        {"$limit": 10}
    ]

    result = collection.aggregate(pipeline)
    for doc in result:
        print(doc)

    print_delimiter('bonus 3')
    pipeline = [
        {
            "$match": {
                "name": {"$regex": "\w+\s+\w+"} # match names with at least two words
            }
        },
        {
            "$addFields": {
                "good_grades": {
                    "$filter": {
                        "input": "$grades",
                        "cond": {"$gt": ["$$this.score", 10]}
                    }
                }
            }
        },
        {
            "$match": {
                "$expr": {"$gt": [{"$size": "$good_grades"}, 1]} # match restaurants with at least 2 good grades
            }
        },
        {"$limit": 10}
    ]
    result = collection.aggregate(pipeline)
    for doc in result:
        # print names of restaurants with at least 2 good grades
        print(doc['name'])


if __name__ == '__main__':
    from init import collection
    main()
