import redis

redis_db = redis.Redis(decode_responses=True)

redis_db.set('caleb', 'porto')
redis_db.delete('caleb')

print(redis_db.get('caleb'))