import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))) 
#telling Pyhton to inlcude src when running the tests 

import pytest
from wardrobe.prototype import suggest_outfit

@pytest.fixture
def sample_wardrobe():
    return [
        {"name": "Blazer", "type": "jacket", "tags": ["formal / elegant", "cold"], "color": "black", "brand": "Zara"},
        {"name": "T-Shirt", "type": "top", "tags": ["sporty", "hot"], "color": "white", "brand": "Nike"},
        {"name": "Jeans", "type": "bottom", "tags": ["day-to-day"], "color": "blue", "brand": "Levi's"},
        {"name": "Raincoat", "type": "jacket", "tags": ["rain"], "color": "yellow", "brand": "Columbia"},
    ]

def test_suggest_outfit_rainy_day(sample_wardrobe):
    result = suggest_outfit("day-to-day", ["rain"], sample_wardrobe)
    assert any(item["name"] == "Raincoat" for item in result)

def test_suggest_outfit_no_match():
    closet = [{"name": "Tank Top", "type": "top", "tags": ["hot"], "color": "red", "brand": ""}]
    result = suggest_outfit("formal / elegant", ["cold"], closet)
    assert result == []
