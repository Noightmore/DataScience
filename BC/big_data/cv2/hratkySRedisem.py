import redis

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Add players
r.zadd('players', {'alfred': 888, 'bob': 999, 'charlie': 777, 'david': 666, 'edward': 555,
                   'frank': 444, 'george': 333, 'harry': 222, 'ian': 111, 'james': 0})

# Print top 3 players
top_players = r.zrevrange('players', 0, 2)
print(top_players)

# get the worst score
worst_score = r.zrange('players', 0, 0)
print(worst_score)

# Print amount of players with less than 100 points
less_than_100 = r.zcount('players', 0, 100)
print(less_than_100)

# Print all player names with more than 850 points
more_than_850 = r.zrangebyscore('players', 850, '+inf')
print(more_than_850)

# Get Alfred's position in the list by descending score
alfreds_position = r.zrevrank('players', 'alfred')
print(alfreds_position)

# Increment Alfred's score by 12
r.zincrby('players', 12, 'alfred')

# Print his position again
alfreds_position = r.zrevrank('players', 'alfred')
print(alfreds_position)
