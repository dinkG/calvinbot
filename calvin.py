import socket

# Chatbot Client for interacting with John Calvin bot
class ChatbotClient:
    def __init__(self, host='127.0.0.1', port=5001):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

    def start(self):
        print("Connected to the John Calvin chatbot server.")
        
        while True:
            # Get the user input (question)
            question = input("Ask John Calvin: ")

            if question.lower() == 'exit':
                print("Exiting the chat.")
                break

            # Send the question to the server
            self.client.send(question.encode('utf-8'))

            # Receive the response from the server
            response = self.client.recv(1024).decode('utf-8')
            print(f"John Calvin's Response: {response}")

        self.client.close()

if __name__ == "__main__":
    client = ChatbotClient()
    client.start()
