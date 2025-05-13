from setuptools import setup, find_packages

setup(
    name='closet-outfit-sorter',
    version='0.1.0',  # Starting version
    description='An online wardrobe where you can insert your clothes and get outfit suggestions based on occasion and weather.',

    packages=find_packages("src"),
    package_dir={"":"src"}, 

)
