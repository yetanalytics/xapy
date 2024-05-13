import xapi

# testing
response = xapi.post_file('sample-xapi.json', 'http://localhost:8080/xapi', 'username', 'password')
print(response)
