import csv
from pathlib import Path

from recipes.models import Ingredient

path_to_csv = Path(__file__).parents[1] / '/ingredients.csv'


with open(path_to_csv, "r", encoding="UTF-8") as csvfile:

    reader = csv.DictReader(csvfile, delimiter=",", fieldnames=['name', 'mu'])
    for row in reader:
        Ingredient.objects.get_or_create(
            name=row['name'],
            measurement_unit=row['mu']
        )
