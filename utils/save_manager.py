import json
import os

class SaveManager:
    """Singleton to manage player progression and economy."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SaveManager, cls).__new__(cls)
            # Find the absolute path to the data folder
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            cls._instance.save_path = os.path.join(base_dir, 'data', 'player_save.json')
            cls._instance.data = {"coins": 50, "max_level_unlocked": 1}
            cls._instance._load()
        return cls._instance

    def _load(self):
        if os.path.exists(self.save_path):
            try:
                with open(self.save_path, 'r') as f:
                    content = f.read().strip()
                    if content:
                        loaded_data = json.loads(content)
                        self.data.update(loaded_data)
            except Exception as e:
                print(f"Error loading save: {e}")

    def save(self):
        """Save current data to file."""
        try:
            os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
            with open(self.save_path, 'w') as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")

    def get_coins(self):
        return self.data.get("coins", 0)

    def add_coins(self, amount):
        self.data["coins"] = self.get_coins() + amount
        self.save()

    def spend_coins(self, amount):
        """Returns True if successful, False if not enough coins."""
        current = self.get_coins()
        if current >= amount:
            self.data["coins"] = current - amount
            self.save()
            return True
        return False

    def get_max_level(self):
        return self.data.get("max_level_unlocked", 1)

    def unlock_level(self, level_num):
        """Unlocks level if it's higher than current max."""
        if level_num > self.get_max_level():
            self.data["max_level_unlocked"] = level_num
            self.save()
