import zmq
import random

celebration_messages = [
    "All tasks are complete! You did that.",
    "Look at you go! Everything on your list is complete!",
    "You showed up, you focused, and you finished. Great job!",
    "Every single task is checked off. You earned this win.",
    "You just turned your to-do list into a ta-da list.",
    "You honored your commitments to to yourself today. Nicely done.",
    "You made progress where it mattered. Be proud of that.",
    "Everything you planned is done. Time to celebrate!",
    "That's it! Your work for today is officially complete.",
]

celebration_visuals = [
    r"""
     ⊂_ヽ         
        ＼＼     
            ＼( •_•)  F
             /  ⌒    A
            /  /\\  B
           /  /  \\   U
          L___)   ＼_つ L
          /  /        0
         /  /       U
        ( ( \     S
         | \ \
         | /` \
         ||   \ )
        /  ) (_/
       ( /___
    """,
    r"""                               
    ▄▄ ▄▄  ▄▄▄   ▄▄▄  ▄▄▄▄   ▄▄▄  ▄▄ ▄▄ 
    ██▄██ ██▀██ ██▀██ ██▄█▄ ██▀██ ▀███▀ 
    ██ ██ ▀███▀ ▀███▀ ██ ██ ██▀██   █   
    """,
    r"""
    ╔═══════════════════════════╗
    ║     ★★ YOU DID IT! ★★     ║
    ╚═══════════════════════════╝
    """,
    r"""
        ___________
       '._==_==_=_.'
       .-\:      /-.
      | (|:.     |) |
       '-|:.     |-'
         \::.    /
          '::. .'
            ) (
          _.'_'._
    """
]

def get_celebration():
    """Returns a combined celebratory message and visual."""
    message = random.choice(celebration_messages)
    visual = random.choice(celebration_visuals)
    return f"{message}{visual}"

def main():
    """Sets up and runs Celebration Service."""

    # set up zmq context and reply socket
    context = zmq.Context()
    socket = context.socket(zmq.REP)

    # set 1s receive-timeout to periodically check for shutdown
    socket.setsockopt(zmq.RCVTIMEO, 1000)

    # bind socket to port
    address = "tcp://*:5558"
    socket.bind(address)
    print(f"Celebration Microservice listening on {address}\n")

    try:
        # infinite loop to receive messages from client
        while True:
            try:
                message = socket.recv_string()
            except zmq.Again:
                continue

            # normalize input, get message/visual, and send response to client
            print(f"Received event from a client: {message}")
            event = message.strip().lower()

            if event == "all-tasks-complete":
                response = get_celebration()
            else:
                response = "Invalid request. Try: all-tasks-complete"

            socket.send_string(response)
            print(f"Sent message to client: {response}\n")

    # allow microservice to shut down via keyboard interrupt
    except KeyboardInterrupt:
        print("Celebration Microservice shutting down...")

    # make a clean exit
    finally:
        socket.close()
        context.term()
        print("Celebration Microservice stopped.\n")

if __name__ == "__main__":
    main()