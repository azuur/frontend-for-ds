from frontend_for_ds.backend import reply


def main():
    session_id = 1
    print(50 * "-")
    print("AI assistant demo!")
    print(50 * "-")
    while True:
        user_message_text = input("Enter a message: ")
        ai_message_text = reply(session_id, user_message_text)
        print(f"AI: {ai_message_text}")
