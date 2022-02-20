def load_token() -> str:
    """Loads the token from the file."""
    with open("token.txt", "r") as token_file:
        token = token_file.read().strip()
    return token