import pandas as pd

class Wardrobe:
    def __init__(self, path="closet.csv"):
        self.path = path
        self.state = pd.read_csv(path)
        self.state.fillna("", inplace=True)

    def add_item(self, item):
        row = {
            "name": item["name"],
            "type": item["type"],
            "color": item["color"],
            "tags": ";".join(item["tags"]),
            "brand": item["brand"]
        }
        self.state = pd.concat([self.state, pd.DataFrame([row])], ignore_index=True)
        self.state.to_csv(self.path, index=False)

    def get_items(self):
        items = []
        for _, row in self.state.iterrows():
            items.append({
                "name": row["name"],
                "type": row["type"],
                "color": row["color"],
                "tags": [tag.strip() for tag in row["tags"].split(";") if tag.strip()],
                "brand": row["brand"]
            })
        return items
