from chatbot.brain import get_response, is_exit_command

BOT_LABEL  = "DEX"
USER_LABEL = "You"


def sanitize_input(raw: str) -> str:

    return raw.strip().lower()


def run():

    print("\n👋 Welcome to DEX!")
    print("I'm here to answer your questions using predefined rules.")
    print("Type 'help' for available commands or 'quit' to exit.\n")

    while True:

        try:
            raw = input(f"  {USER_LABEL}  :  ")
        except (KeyboardInterrupt, EOFError):
            print(f"\n  {BOT_LABEL}  :  Session ended. Keep building!\n")
            break

        clean = sanitize_input(raw)

        if not clean:
            print(f"  {BOT_LABEL}  :  Please type something.\n")
            continue

        if is_exit_command(clean):
            print(f"  {BOT_LABEL}  :  Goodbye! See you next session.\n")
            break

        response = get_response(clean)
        print(f"  {BOT_LABEL}  :  {response}\n")


if __name__ == "__main__":
    run()