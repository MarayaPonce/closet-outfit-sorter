import pandas as pd
class Wardrobe:
    def __init__(self):
        # Read csv file into state
        self.state = pd.read_csv("wardrobe.csv")
    def add_item(self, item):
        self.state[item["name"]] = item["details"]
        self.state.write_csv("wardrobe.csv")
    def get_items(self):
        return self.state.to_dict()