import xapi
import json
from base64 import b64encode
import uuid
import concurrent.futures

# testing. Use LRS details below
# response = xapi.post_file('sample-xapi.json', 'localhost', 'username', 'password', port=8080, protocol='http', batch=5)

f = open('template-xapi.json')
template_data = json.load(f)

def push_batch():
    batch = []
    for x in range(0, 150):
        new_data = template_data
        new_data['actor']['account']['name'] = str(uuid.uuid4())
        batch.append(new_data)
    response = xapi.post_xapi(batch, 'localhost', 'my_key', 'my_secret', port=8080, protocol='http', batch=150)
    print('finished batch of 150')


print("got here")

threads = 20

for y in range(0, 1000):
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        for x in range(0, threads):
            executor.submit(push_batch)
    print('finished loop:' + str(y))

print("got here1")
