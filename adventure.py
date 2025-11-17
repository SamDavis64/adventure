import random
import math

# ----- Global Variables -----
NUM_LOCATIONS = 5
NUM_ITEMS = 5


# ----- Function to calc number of locations and items -----
def calc_num_locations_items(difficulty):
    """set global NUM_LOCATIONS and NUM_ITEMS."""
    global NUM_LOCATIONS, NUM_ITEMS
    NUM_LOCATIONS = difficulty
    NUM_ITEMS = min(int(math.sqrt(difficulty)) + 5, difficulty)


# ----- Item Class -----
class Item:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description

    def __str__(self):
        return self.name


# ----- Location Class -----
class Location:
    def __init__(self, name):
        self.name = name
        self.items = []
        self.neighbors = {}

    def connect(self, other, direction):
        opposites = {'north': 'south', 'south': 'north',
                     'east': 'west', 'west': 'east'}
        self.neighbors[direction] = other
        other.neighbors[opposites[direction]] = self

    def describe(self):
        print(f"\nYou are at {self.name}.")
        if self.items:
            print("You see the following items:")
            for item in self.items:
                print(f" - {item}")
        else:
            print("There is nothing of interest here.")
        if self.neighbors:
            print("Exits:", ", ".join(self.neighbors.keys()))
        else:
            print("There are no visible exits.")


# ----- Character Class -----
class Character:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.inventory = []

    def move(self, direction):
        if direction in self.location.neighbors:
            self.location = self.location.neighbors[direction]
            print(f"You move {direction}.")
        else:
            print("You can't go that way.")

    def take_item(self, item_name):
        for item in self.location.items:
            if item.name.lower() == item_name.lower():
                self.inventory.append(item)
                self.location.items.remove(item)
                print(f"You picked up: {item.name}")
                return
        print("That item is not here.")

    def inventory_list(self):
        if self.inventory:
            print("You have collected:")
            for item in self.inventory:
                print(f" - {item}")
        else:
            print("You are carrying nothing.")


# ----- GameMap Class -----
class GameMap:
    def __init__(self, num_locations, num_items):
        self.locations = []
        self.item_names = []

        self.locations = self.create_locations(num_locations)
        self.connect_locations()
        self.starting_location = self.locations[0]
        self.item_names = self.generate_item_names(num_items)
        self.distribute_items()


    def create_locations1(self, num):
        prefixes = [
            "Whispering", "Crimson", "Foggy", "Azure", "Twilight",
            "Echoing", "Glowing", "Howling", "Sunken", "Obsidian",
            "Silver", "Ember", "Frosted", "Verdant", "Hidden"
        ]

        suffixes = [
            "Hollow", "Tower", "Dunes", "Pass", "Keep",
            "Caverns", "Marsh", "Ridge", "Vale", "Point",
            "Spire", "Forest", "Glade", "Sanctum", "Reach"
        ]

        names = set()
        while len(names) < num:
            names.add(random.choice(prefixes) + " " + random.choice(suffixes))

        names = list(names) # Convert set to a list

        locations = []
        for name in names:  # Loop through each name in the 'names' collection
            location = Location(name)
            locations.append(location)
        return locations

    def create_locations(self, num):
        """Create and return a list of unique Location objects."""
        prefixes = [
            "Whispering", "Crimson", "Foggy", "Azure", "Twilight",
            "Echoing", "Glowing", "Howling", "Sunken", "Obsidian",
            "Silver", "Ember", "Frosted", "Verdant", "Hidden"
        ]

        suffixes = [
            "Hollow", "Tower", "Dunes", "Pass", "Keep",
            "Caverns", "Marsh", "Ridge", "Vale", "Point",
            "Spire", "Forest", "Glade", "Sanctum", "Reach"
        ]

        # ----- Generate all possible prefix-suffix combinations -----
        all_names = []
        for p in prefixes:
            for s in suffixes:
                name = p + " " + s
                all_names.append(name)

        # Shuffle the full list of names
        random.shuffle(all_names)

        # Select only as many as needed for this game
        selected_names = all_names[:num]

        # Create Location objects
        locations = []
        for name in selected_names:
            location = Location(name)
            locations.append(location)

        return locations

    def connect_locations(self):
        # Connect all locations into a simple tree structure
        directions = ['north', 'south', 'east', 'west']

        unconnected = self.locations[:]
        connected = [unconnected.pop(0)]

        while unconnected:
            # Pick a connected location that still has available exits
            available = [loc for loc in connected if len(loc.neighbors) < len(directions)]
            if not available:
                # all connected locations are full; stop connecting
                break

            loc1 = random.choice(available)
            loc2 = unconnected.pop(0)

            # choose a direction that is still free
            free_dirs = [d for d in directions if d not in loc1.neighbors]
            if not free_dirs:
                continue  # just in case, skip if somehow no free directions

            dir = random.choice(free_dirs)
            loc1.connect(loc2, dir)
            connected.append(loc2)


    def generate_item_names(self, num):
        adjectives = [
            "Glowing", "Ancient", "Silver", "Mystic", "Cracked",
            "Golden", "Dark", "Frozen", "Burning", "Silent",
            "Cursed", "Radiant", "Enchanted", "Shadowed", "Blessed"
        ]
        nouns = [
            "Orb", "Key", "Crystal", "Ring", "Tome",
            "Stone", "Amulet", "Lantern", "Scroll", "Gem",
            "Blade", "Crown", "Mask", "Chalice", "Feather"
        ]
        names = set()
        while len(names) < num:
            names.add(random.choice(adjectives) + " " + random.choice(nouns))
        return list(names)

    def distribute_items(self):
        items = [Item(name) for name in self.item_names]
        for item in items:
            location = random.choice(self.locations)
            location.items.append(item)

    def display_map(self):
        """Display a readable table of all locations, their items, and directions."""
        print("\n=== GAME MAP ===")
        print(f"{'Location':30} | {'Items':35} | {'N':^3} | {'S':^3} | {'E':^3} | {'W':^3}")
        print("-" * 85)
        for loc in self.locations:
            items_str = ", ".join([item.name for item in loc.items]) if loc.items else "-"
            dirs = {d: "✓" if d in loc.neighbors else " " for d in ['north', 'south', 'east', 'west']}
            print(f"{loc.name:30} | {items_str:35} | {dirs['north']:^3} | {dirs['south']:^3} | {dirs['east']:^3} | {dirs['west']:^3}")
        print("-" * 85)


# ----- Initialize Game -----
def initialise_game(difficulty):
    """Initializes and returns the game map and player."""
    print("Welcome to Adventure!")
    calc_num_locations_items(difficulty)
    game_map = GameMap(NUM_LOCATIONS, NUM_ITEMS)
    player = Character("Adventurer", game_map.starting_location)
    print(f"Collect {NUM_ITEMS} items and return to {player.location.name} to win!")
    return game_map, player


# ----- Process Player Command -----
def process_command(command, player, game_map):
    """Process the player's input command."""
    if command.startswith("go "):
        direction = command[3:]
        if direction in ["north", "south", "east", "west"]:
            player.move(direction)
        else:
            print("Invalid direction. Use north, south, east, or west.")
    elif command.startswith("take "):
        item_name = command[5:]
        player.take_item(item_name)
    elif command == "inventory":
        player.inventory_list()
    elif command == "look":
        player.location.describe()
    elif command == "map":
        game_map.display_map()
    elif command == "quit":
        print("Thanks for playing!")
        return False
    else:
        print("Unknown command. Try: go <direction>, take <item>, inventory, look, map, quit")
    return True


# ----- Main Game -----
def main():

    difficulty = int(input("Enter difficulty level (1–100): "))
    game_map, player = initialise_game(difficulty)
    running = True
    won = False

    while running and not won:
        player.location.describe()
        command = input("\nWhat do you want to do? ").strip().lower()
        running = process_command(command, player, game_map)
        won = len(player.inventory) == NUM_ITEMS and player.location is game_map.starting_location

    if won:
        print(f"\nCongratulations! You collected all items and returned to {game_map.starting_location.name}. Your quest is complete!")

if __name__ == "__main__":
    main()
