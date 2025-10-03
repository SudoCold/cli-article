import os
import sys
import keyboard

ARTICLES_DIR = "articles"

def ensure_articles_dir():
    if not os.path.exists(ARTICLES_DIR):
        os.makedirs(ARTICLES_DIR)

def write_article():
    title = input("Enter article title: ").strip()
    if not title:
        print("Invalid title.")
        return
    filepath = os.path.join(ARTICLES_DIR, f"{title}.txt")

    print("\nStart writing your article. Press Ctrl+S to save & exit. Press Ctrl+C to cancel.\n")
    content_lines = []
    current_line = []

    def on_key(event):
        nonlocal current_line, content_lines
        if event.name == "enter":
            content_lines.append("".join(current_line))
            current_line = []
            print()  # move to new line
        elif event.name == "space":
            current_line.append(" ")
            print(" ", end="", flush=True)
        elif event.name == "backspace":
            if current_line:
                current_line.pop()
                sys.stdout.write("\b \b")
                sys.stdout.flush()
        elif event.name == "s" and keyboard.is_pressed("ctrl"):
            # Save file
            content_lines.append("".join(current_line))
            text = "\n".join(content_lines)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"\n\nArticle saved as {filepath}\n")
            keyboard.unhook_all()
            raise SystemExit
        elif event.name == "c" and keyboard.is_pressed("ctrl"):
            print("\nCancelled. Nothing saved.\n")
            keyboard.unhook_all()
            raise SystemExit
        elif len(event.name) == 1:  # regular characters
            current_line.append(event.name)
            print(event.name, end="", flush=True)

    keyboard.on_press(on_key)
    keyboard.wait()  # keep listening until exit

def list_articles():
    files = [f for f in os.listdir(ARTICLES_DIR) if f.endswith(".txt")]
    if not files:
        print("No articles found.\n")
        return []
    print("\nAvailable Articles:")
    for i, file in enumerate(files, start=1):
        print(f"{i}. {file}")
    print()
    return files

def read_article():
    files = list_articles()
    if not files:
        return
    try:
        choice = int(input("Select article number to read: "))
        if 1 <= choice <= len(files):
            filepath = os.path.join(ARTICLES_DIR, files[choice-1])
            with open(filepath, "r", encoding="utf-8") as f:
                print("\n" + f.read() + "\n")
        else:
            print("Invalid choice.\n")
    except ValueError:
        print("Please enter a valid number.\n")

def menu():
    ensure_articles_dir()
    while True:
        print("Choose an option:")
        print("(1) Write Article")
        print("(2) Read Article")
        print("(3) Quit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            write_article()
        elif choice == "2":
            read_article()
        elif choice == "3":
            print("Goodbye!")
            sys.exit()
        else:
            print("Invalid option.\n")

if __name__ == "__main__":
    menu()
2
