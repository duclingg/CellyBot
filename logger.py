class CellyBotLogger:
    def __init__(self, name="CellyBot"):
        self.name = name

    def start_log(self, user, user_id):
        print("\n" + "-" * 70)
        print(f"[{self.name}] INFO - Logged in as {user} (ID: {user_id})")
        print("-" * 70 + "\n")

    def info(self, message: str):
        print(f"[{self.name}] INFO - {message}")
        
    def debug(self, message: str):
        print(f"[{self.name}] DEBUG - {message}")

    def error(self, message: str):
        print(f"[{self.name}] ERROR - {message}")