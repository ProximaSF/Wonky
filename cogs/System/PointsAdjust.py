import disnake
from disnake.ext import commands

class Adjust_WobbleBBits(commands.Cog):
    def __init__(self):
        pass

    def add_WobbleBits(self, user_id, wobbleBits):
        with open("txt/playerpoints.txt", "r+", encoding="utf-8-sig") as f:
            lines = f.readlines()
            user_found = False
            for i, line in enumerate(lines):
                if line.startswith(f"[{user_id}]"):
                    user_found = True
                elif user_found and line.strip().startswith("Current WobbleBits:"):
                    current_WobbleBits = int(line.strip().split(': ')[1])
                    new_wobbleBits = current_WobbleBits + wobbleBits
                    lines[i] = f"\tCurrent WobbleBits: {new_wobbleBits}\n"
                    break
            f.seek(0)
            f.writelines(lines)
            f.truncate()

    def sub_WobbleBits(self, user_id, wobbleBits):
        with open("txt/playerpoints.txt", "r+", encoding="utf-8-sig") as f:
            lines = f.readlines()
            f.seek(0)
            user_found = False
            for i, line in enumerate(lines):
                if line.startswith(f"[{user_id}]"):
                    user_found = True
                elif user_found and line.strip().startswith("Current WobbleBits:"):
                    current_wobbleBits = int(line.strip().split(': ')[1])
                    new_wobbleBits = current_wobbleBits - wobbleBits
                    lines[i] = f"\tCurrent WobbleBits: {new_wobbleBits}\n"
                    break
            f.seek(0)
            f.writelines(lines)
            f.truncate()

    def get_WobbleBits(self, user_id):
        with open("txt/playerpoints.txt", "r", encoding="utf-8-sig") as f:
            lines = f.readlines()
            found_user = False
            for line in lines:
                if line.startswith(f"[{user_id}]"):
                    found_user = True
                elif found_user and line.strip().startswith("Current WobbleBits:"):
                    return int(line.strip().split(': ')[1])
        return None

    def sub_steal_attempts(self, user_id, reduce_steal_attempts):
        with open("txt/playerpoints.txt", "r+", encoding="utf-8-sig") as f:
            lines = f.readlines()
            f.seek(0)
            user_found = False
            for i, line in enumerate(lines):
                if line.startswith(f"[{user_id}]"):
                    user_found = True
                elif user_found and line.strip().startswith("Steal Attempts:"):
                    current_steal_attempts = int(line.strip().split(': ')[1])
                    new_steal_attempts = current_steal_attempts - reduce_steal_attempts
                    lines[i] = f"\tSteal Attempts: {new_steal_attempts}\n"
                    break
            f.seek(0)
            f.writelines(lines)
            f.truncate()

    def get_steal_attempts(self, user_id):
        with open("txt/playerpoints.txt", "r", encoding="utf-8-sig") as f:
            lines = f.readlines()
            found_user = False
            for line in lines:
                if line.startswith(f"[{user_id}]"):
                    found_user = True
                elif found_user and line.strip().startswith("Steal Attempts:"):
                    return int(line.strip().split(': ')[1])
        return None


def setup(client):
    client.add_cog(Adjust_WobbleBBits())
