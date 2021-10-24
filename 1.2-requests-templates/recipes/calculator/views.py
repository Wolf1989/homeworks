from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
}


def show_recipe(request, recipe):
    template_name = 'calculator/index.html'

    ingredients = DATA.get(recipe)
    servings = request.GET.get('servings', default='1')

    if ingredients != None and servings.isdigit() == True:
        servings = int(servings)
        if  servings > 1:
            ingredients = ingredients.copy()
            for name, number in ingredients.items():
                ingredients[name] = number * servings

    context = {
        'recipe': ingredients,
    }

    return render(request, template_name, context)
