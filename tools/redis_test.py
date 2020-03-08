import redis

r = redis.Redis(host="localhost",port=6379,db=0,charset="utf-8",decode_responses=True)

r.set("mobile","123123123")
r.expire("mobile",1)
print(r.get("mobile"))



