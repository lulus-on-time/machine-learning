import redis

# Replace with your Redis server's IP address and port
redis_host = 'localhost'
redis_port = 6379

try:
    # Create a Redis client
    client = redis.Redis(host=redis_host, port=redis_port)

    # Ping the server to check if the connection is successful
    if client.ping():
        print("Connected to Redis server successfully")

    # Set a key-value pair
    client.set('test_key', 'test_value')

    # Retrieve the value of the key
    value = client.get('test_key')
    print(f"The value of 'test_key' is: {value.decode('utf-8')}")

except :
    print(f"Could not connect to Redis server")
