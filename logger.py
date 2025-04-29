class CellyBotLogger:
    def __init__(self, name="CellyBot"):
        self.name = name

    def start_log(self, user, user_id):
        """
        Starts the logger for the Bot.

        Args:
            user (str): unique user of the bot
            user_id (int): unique id of the bot
        """
        print("\n" + "-" * 70)
        print(f"[{self.name}] INFO - Logged in as {user} (ID: {user_id})")
        print("-" * 70 + "\n")

    def info(self, message: str):
        """
        Information log. Used to provide information about script actions as it runs.

        Args:
            message (str): message of the action
        """
        print(f"[{self.name}] INFO - {message}")
        
    def debug(self, message: str):
        """
        Debug log. Used to help debug.

        Args:
            message (str): message of the action to debug
        """
        print(f"[{self.name}] DEBUG - {message}")

    def error(self, message: str):
        """
        Error log. CellyBot specific error logger.

        Args:
            message (str): message of the error
        """
        print(f"[{self.name}] ERROR - {message}")