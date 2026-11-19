
from pathlib import Path


# Find our knowledge file
DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "about_me.md"
)


def load_knowledge():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Knowledge file not found: {DATA_FILE}"
        )

    content = DATA_FILE.read_text(encoding="utf-8").strip()

    if not content:
        raise ValueError("The knowledge file is empty.")

    return content


if __name__ == "__main__":
    knowledge = load_knowledge()

    print("Knowledge file loaded successfully!")
    print("------------------------------")
    print(knowledge)
