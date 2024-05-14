import xapi

# testing. Use LRS details below
response = xapi.post_file('sample-xapi.json', 'localhost', 'username', 'password', port=8080, protocol='http', batch=5)
print(response)
