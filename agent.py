def main():
    print("🤖 Hello! Ask me anything.")
    while True:
        try:
            user = input("You: ").strip()
            if not user:
                continue

            if user.lower() == "exit":
                print("🤖 Goodbye!")
                break

            if user.lower() == "!fix":
                print("🤖 To fix me, please run the main program again.")
                continue

            # Basic hardcoded Q&A for demo
            if user.lower() == "what are you?":
                print("🤖 I am AI Infinity, your assistant.")
            elif user.lower() == "say i don't know":
                print("🤖 I'm still learning.")
            else:
                print(f"🤖 Sorry, I don't know how to answer '{user}'.")
        except KeyboardInterrupt:
            print("\n🤖 Exiting.")
            break

if __name__ == "__main__":
    main()
