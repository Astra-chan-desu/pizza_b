from django.db import migrations
import random

def create_initial_pizzas(apps, schema_editor):
    Pizza = apps.get_model('pizza_b', 'Pizza')

    pizzas = [
        ("Маргарита", "Классическая пицца с томатами, моцареллой и базиликом.", "margherita.png"),
        ("Пепперони", "Пикантная пицца с ломтиками пепперони и расплавленным сыром.", "pepperoni.png"),
        ("Четыре сыра", "Сливочная пицца с моцареллой, горгонзолой, пармезаном и эмменталем.", "four_cheese.png"),
        ("Гавайская", "Пицца с ананасом, ветчиной и расплавленным сыром.", "hawaiian.png"),
        ("BBQ Чикен", "Пицца с курицей, красным луком и барбекю-соусом.", "bbq_chicken.png"),
        ("Мясная (Meat Lovers)", "Пицца с пепперони, колбасками, беконом и ветчиной.", "meat_lovers.png"),
        ("Вегетарианская", "Пицца с перцем, маслинами, грибами и томатами.", "vegetarian.png"),
        ("Капричоза", "Пицца с ветчиной, артишоками, грибами и оливками.", "capricciosa.png"),
        ("Диабло", "Острая пицца с салями, перцем чили и острым соусом.", "diablo.png"),
        ("Трюфельная", "Пицца с белым соусом, грибами и трюфельным маслом.", "truffle.png"),
        ("Морская", "Пицца с креветками, мидиями и кальмарами.", "seafood.png"),
        ("Белая пицца (Bianca)", "Пицца без томатного соуса, с сыром, чесноком и оливковым маслом.", "bianca.png"),
        ("Песто", "Пицца с соусом песто, черри и сыром.", "pesto.png"),
        ("Грибная", "Пицца с грибами и сливочным соусом.", "mushroom.png"),
        ("Чикен Ранч", "Пицца с курицей, беконом и соусом ранч.", "chicken_ranch.png"),
        ("Шпинат и рикотта", "Пицца со шпинатом, рикоттой и чесноком.", "spinach_ricotta.png"),
        ("Овощная с баклажанами", "Пицца с баклажанами, цукини и перцем.", "vegetable_eggplant.png"),
        ("Карбонара", "Пицца с беконом, сливочным соусом и яйцом.", "carbonara.png"),
        ("Мексиканская", "Пицца с острым перцем, кукурузой, фасолью и говядиной.", "mexican.png"),
        ("Сладкая (десертная)", "Пицца с нутеллой, клубникой и бананом.", "dessert.png"),
    ]

    for name, description, image in pizzas:
        Pizza.objects.create(
            name=name,
            description=description,
            cost=random.randint(300, 600),
            image=f"pizzas/{image}",
        )

class Migration(migrations.Migration):

    dependencies = [
        ('pizza_b', '0003_remove_driver_current_location_branch_coordinates_and_more'),
    ]

    operations = [
        migrations.RunPython(create_initial_pizzas),
    ]
