import zmq

def main():
    """Connect to Celebration Microservice and send sample category requests."""

    # set up zmq context and request socket, connect to Celebration Microservice endpoint
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5558")

    # Test 1: send "all-tasks-complete" event, print response
    print("Calling Celebration Microservice with 'all-tasks-complete' request...")
    socket.send_string("all-tasks-complete")
    response = socket.recv_string()
    print(f"Response: {response}\n")

    # Test 2: send "all-tasks-complete" event, print response
    print("Calling Celebration Microservice with 'all-tasks-complete' request...")
    socket.send_string("all-tasks-complete")
    response = socket.recv_string()
    print(f"Response: {response}\n")

    # make a clean exit
    socket.close()
    context.term()

if __name__ == "__main__":
    main()