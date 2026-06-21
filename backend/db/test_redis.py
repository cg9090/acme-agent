print("Starting test")

from db.redis_client import redis_client

print("Connected object created")

redis_client.set("test", "hello")
print("Value set")

value = redis_client.get("test")
print("Value retrieved")

print(value)