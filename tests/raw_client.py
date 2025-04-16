import msgpack
import uuid
import zmq
import time 
import json
import copy

req_data = [{'message_id': str(uuid.uuid4()), 'v': 3}, 'hello', ['John']]

def bytes_to_obj(bs):
    with open('receive_bs.dat', 'wb') as wfl:
        wfl.write(bs)
    ret = msgpack.unpackb(bs)
    with open('receive_bs.json', 'w') as wfl:
        ret1 = copy.deepcopy(ret)
        ret1[0]['message_id'] = str(ret1[0]['message_id'])
        json.dump(ret1, wfl)
    return ret      

def obj_to_bytes(obj):
    with open('sent_bs.json', 'w') as wfl:
        json.dump(obj, wfl)    
    ret = msgpack.packb(obj)
    with open('sent_bs.dat', 'wb') as wfl:
        wfl.write(ret)
    return ret

def send_receive_dealer(endpoint, data):
    context = zmq.Context()
    socket = context.socket(zmq.DEALER)
    socket.connect(endpoint)
    
    try:
        send_data = obj_to_bytes(data)
        
        socket.send(send_data)
        print(f"Sent {len(send_data)} bytes")
        
        while True:
            reply = socket.recv()
            print(f"Received {len(reply)} bytes")
            if reply: 
                return reply
        
    finally:
        socket.close()
        context.term()

# Example usage
if __name__ == "__main__":
    endpoint = "tcp://localhost:4242"
    
    # Test with different data types
    test_data = [req_data]
    
    for data in test_data:
        print(f"\nSending: {data} (type: {type(data)})")
        reply = send_receive_dealer(endpoint, data)
        
        if reply:
            decoded = bytes_to_obj(reply)
            print(f"Received reply: {decoded}")