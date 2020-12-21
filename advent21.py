from functools import reduce


def parse_input(f):
    return (parse_ingredients(l.rstrip("\n)").rstrip()) for l in f)


def parse_ingredients(l):
    ingredients, allergens = l.split("(contains ")
    ingredients = set(ingredients.split())
    allergens = set(allergens.split(", "))
    return ingredients, allergens


def all_items(items):
    return reduce(set.union, items)


def check_ingredient_allergen(allergen, data):
    ingredient_data = filter(lambda x: allergen in x[1], data)
    return reduce(set.intersection, (x[0] for x in ingredient_data))


def get_ingredients_allergens(allergens, data):
    return {
        allergen: check_ingredient_allergen(allergen, data) for allergen in allergens
    }


def part_1(data):
    ingredients, allergens = map(all_items, zip(*data))
    matches_allergens = get_ingredients_allergens(allergens, data)
    all_allergen_ingredients = reduce(set.union, matches_allergens.values())
    non_allergen_ingredients = ingredients - all_allergen_ingredients
    return sum(len(recipe.intersection(non_allergen_ingredients)) for recipe, _ in data)


def reduce_to_one_allergen(matched_allergens):
    by_len = sorted(matched_allergens.items(), key=lambda x: len(x[1]))
    visited = set()
    result = {}
    for k, v in by_len:
        value = v.difference(visited).pop()
        result[k] = value
        visited.add(value)
    return result


def part_2(data):
    ingredients, allergens = map(all_items, zip(*data))
    matches_allergens = get_ingredients_allergens(allergens, data)
    all_allergen_ingredients = reduce(set.union, matches_allergens.values())

    matched_ingredients = {
        ingredient: set(allergen for allergen, ingredients in matches_allergens.items() if ingredient in ingredients)
        for ingredient in all_allergen_ingredients
    }

    matched_to_one_allergen = reduce_to_one_allergen(matched_ingredients)
    return ",".join(
        x[0] for x in sorted(matched_to_one_allergen.items(), key=lambda x: x[1])
    )


if __name__ == "__main__":
    with open("./input/advent21.txt") as f:
        data = list(parse_input(f))
        print(part_1(data))
        print(part_2(data))
