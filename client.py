import socket
import json

#getting config
config = json.load(open("config.json"))

REQUEST_BUFFER = config["request_buffer"]
CHUNK_SIZE = config["chunk_size"]

# getting blacklisted domains
blacklist = json.load(open("blacklist.json"))

def handle_http(client:socket.socket):
    http_request = client.recv(REQUEST_BUFFER) # default apache2 BufferSize

    website_address = get_domain_name(http_request)

    if website_address in blacklist["malicious"] or website_address in blacklist["other"]:
        website_address = "hole.cert.pl"

    elif website_address in blacklist["ads"]:
        client.close()
        return

    #getting content of site
    websocket = socket.socket()
    websocket.connect((website_address, 80))
    websocket.send(http_request)

    while True:
        chunk = websocket.recv(CHUNK_SIZE) # default apache2 ChunkSize

        #dynamically sending chunks
        client.send(chunk)

def get_domain_name(request:bytes):
    domain_name = str(request).split()[3].split("\\")[0]

    return domain_name