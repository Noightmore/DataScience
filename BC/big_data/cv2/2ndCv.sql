-- enter 5 new records
set chair 1
set table 2
set sink 3
set basin 4
set toilet 5

-- get all the above records
get chair
get table
get sink
get basin
get toilet
-- or get all
-- or keys all
-- exist chair -> returns 1
-- exist bed -> returns 0

-- update 1 record
set chair 6

-- delete 1 record
del chair

-- delete table element in 60 seconds
expire table 60
ttl table

-- create list with name of todo-list
lpush todo-list "buy table"
lpush todo-list "buy chair"
rpush todo-list "buy sink"

-- print the contents of the list
lrange todo-list 0 -1

-- print the amount of elements in the list
llen todo-list

-- remove and print the first element of the list
lpop todo-list

-- print the contents of the list
lrange todo-list 0 -1

-- add players
zadd players 888 "alfred"
zadd players 999 "bob"
zadd players 777 "charlie"
zadd players 666 "david"
zadd players 555 "edward"
zadd players 444 "frank"
zadd players 333 "george"
zadd players 222 "harry"
zadd players 111 "ian"
zadd players 000 "james"

-- print top 3 players
zrevrange players 0 2 withscores

-- get the worst score
zrange players 0 0 withscores

-- print amount of players with less than 100 points
zcount players 0 100

-- print all player names with more than 850 points
zrangebyscore players 850 +inf

-- get alfreds position
zrevrank players "alfred"

-- increment alfreds score by 12
zincrby players 12 "alfred"
-- print his position again
zrevrank  players "alfred"

-- set dialect to be redis
set dialect redis





