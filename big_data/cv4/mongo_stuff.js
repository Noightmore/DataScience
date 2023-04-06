mongo

use cv04

$comment: "add new restaurant"

db.restaurants.insertOne({
  "address": {
    "building": "1234",
    "coord": [-74.005941, 40.712784],
    "street": "Broadway",
    "zipcode": "10001"
  },
  "borough": "Manhattan",
  "cuisine": "Italian",
  "grades": [
    {
      "date": {"$date": 1648694400000},
      "grade": "A",
      "score": 12
    },
    {
      "date": {"$date": 1620000000000},
      "grade": "B",
      "score": 9
    }
  ],
  "name": "Tony's Pizza",
  "restaurant_id": "12345678"
})

$comment: "print the newly added restaurant"

db.restaurants.findOne({ "restaurant_id": "12345678" })

$comment: "update the newly added restaurant"
$comment: "we can also use updateMany() to update multiple documents"
db.restaurants.updateOne({ "restaurant_id": "12345678" }, { "$set": { "name": "Tony's Pizzeria" } })

$comment: "add a new grade into the grades array"
db.restaurants.updateOne(
  { "restaurant_id": "12345678" },
  { "$push": { "grades": { "date": new Date(), "grade": "A", "score": 8 } } }
)

$comment: "delete the new record"
db.restaurants.deleteOne({ "restaurant_id": "98765432" })

$comment: "print all records"
db.restaurants.find()

$comment: "print all restaurant names in alhpabetial order"
db.restaurants.find({}, { "name": 1, "_id": 0 }).sort({ "name": 1 })

$comment: "print all restaurant names in alhpabetial order - just the first 10"
db.restaurants.find({}, { "name": 1, "_id": 0 }).sort({ "name": 1 }).limit(10)

$comment: "print all restaurant names in alhpabetial order - skip the first 10 and print the next 10"
db.restaurants.find({}, { "name": 1, "_id": 0 }).sort({ "name": 1 }).skip(10).limit(10)

$comment: "print all restaurants that reside in the burough of Bronx"
db.restaurants.find({ "borough": "Bronx" })

$comment: "print all restaurants that start with letter M"
db.restaurants.find({ "name": { "$regex": "^M" } })

$comment: "print all restarants that reside in the burough of Mannhaton and provide Italian cuisine"
db.restaurants.find({ "borough": "Manhattan", "cuisine": "Italian" })

$comment: "print all restaurants that have got score higher than 80"
db.restaurants.find({ "grades.score": { "$gt": 80 } })

$comment: "get the amount of existing documents inside of the database"
db.restaurants.countDocuments()

$comment: "Bonus part"

$comment: "print all restaurants with score between 80 and 90"
db.restaurants.find({
    "grades": {
        "$elemMatch": {
            "score": {
                "$gte": 80,
                "$lte": 90
            }
        },
        "$not": {
            "$elemMatch": {
                "score": {
                    "$lt": 80,
                    "$gt": 90
                }
            }
        }
    }
})

$text: {
taky moznost:
db.restaurants.find({
    "grades": {
        "$elemMatch": {
            "score": {
                "$gte": 80,
                "$lte": 90
            }
        }
    }
})

}


$comment: "add a new parameter called \"popular: 1 \"to restaurant record which have score that is higher than 80 and add new parameter \"trash: 1\" to restaurants with score lower than 1"
db.restaurants.updateMany({ "grades.score": { "$gt": 80 } }, { "$set": { "popular": 1 } })
db.restaurants.find({ "grades.score": { "$gt": 80 } })

db.restaurants.updateMany({ "grades.score": { "$lt": 1 } }, { "$set": { "trash": 1 } })
db.restaurants.find({ "grades.score": { "$lt": 1 } })


$comment: "print all restaurants that are popular and trash"
db.restaurants.find({ "$and": [{ "trash": 1 }, { "popular": 1 }] })

db.restaurants.updateMany({ "grades.score": { "$gt": 90 } }, { "$set": { "top_score": 1 } })
db.restaurants.find({ "grades.score": { "$gt": 80 } })

$comment: "add a new parameter called \"top_score: 1 \"to all grades that have score higher than 90"
db.restaurants.updateMany({"grades.score": {$gt: 90}}, {$set: {"grades.$[elem].top_score": 1}}, {arrayFilters: [{"elem.score": {$gt: 90}}]})
db.restaurants.find({ "grades.score": { "$gte": 90 } })







