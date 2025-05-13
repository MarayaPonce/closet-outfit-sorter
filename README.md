# closet-outfit-sorter
Our project consists of a virtual closet. You can uppload your clothing items, by entering their characteristics and an image. You can also ask for suggested outfits base on occasion and weather. 

This app requires an OpenWeatherMap API key. You’ll be prompted to paste it when launching the app.

## Installation

Dependencies are handled with conda, you can install them with:
```sh
conda env create
```
Then activate the environment with
```sh
conda activate wardrobe-env
```
The project can then be installed with pip:
```sh
pip install .
```

## Tests

You can run the tests with pytest by running the following command in the root directory of the project:
```sh
pytest -v
```

## Usage
Our project can be used through streamlit. 

[Launch the app on Streamlit](https://your-app-name.streamlit.app)

If you want to run the project from the terminal use: 
```sh
 streamlit run src/wardrobe/wardrobe.py
```
The main code of the project is in prototype.py (not app.py). app.py is an older version kept as a backup. 

