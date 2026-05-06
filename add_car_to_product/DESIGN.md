# Design Document — Add Car to Product

## Мета

Розширити стандартний Odoo-магазин до формату магазину автозапчастин:
- Прив'язати товари до конкретних моделей авто
- Надати зручний пошук за параметрами автомобіля на сайті

---

## Архітектура

### Нові моделі

#### `fleet.vehicle.engine.volume`
Довідник об'ємів двигунів. Винесений в окрему модель щоб:
- Уникнути дублів (SQL constraint на `value`)
- Забезпечити числову сортировку (`_order = 'value'`)
- Дозволити вибір через Many2one з автодоповненням

### Розширені моделі

#### `fleet.vehicle.model`
Додані поля для більш точного опису автомобіля:
- `model_type` — варіант кузова/серії (наприклад E84, F30)
- `model_year_from` / `model_year_to` — діапазон років випуску з валідацією `from <= to`
- `volume_id` — Many2one на `fleet.vehicle.engine.volume`
- `ovoko_car_id` — зовнішній ідентифікатор для синхронізації з Ovoko (унікальний)

#### `product.template`
- `is_autoparts` (Boolean) — ознака що шаблон є автозапчастиною
- Смарт-кнопка **Variants** відкриває список варіантів (через XML action, без Python-методу)

#### `product.product`
- `is_autoparts` — related від шаблону, store=True для швидкого пошуку
- `compatible_vehicle_ids` — Many2many на `fleet.vehicle.model` (таблиця сумісності)
- `for_all_models` — маркер для універсальних запчастин (лампи, оливи тощо)
- `oem` — номер від неоригінального виробника
- `ovoko_part_id` — зовнішній ID для Ovoko (унікальний)

---

## Ключові рішення

### Чому поля сумісності на `product.product`, а не на `product.template`?

Один шаблон ("Фара передня ліва") може мати кілька варіантів — кожен для своєї моделі авто.
Якби сумісність була на шаблоні, всі варіанти мали б однакові авто, що суперечить логіці магазину.

### Формування назви варіанту

Перевизначено `_compute_display_name` на `product.product`.
Береться перше авто зі списку `compatible_vehicle_ids` і будується рядок:
```
{template.name} {brand} {model_name} {model_type} {year_from}-{year_to}
```
Якщо `is_autoparts=False` або список порожній — викликається стандартна логіка через `super()`.

### Чому використовується XML Action для кнопки Variants?

При використанні `type="object"` (Python-метод) Odoo валідує наявність методу на **обох** моделях
(`product.template` і `product.product`, оскільки друга наслідує view першої).
XML Action (`type="action"`) не потребує Python-методу — домен будується через `active_id` контексту.

### Пошук на сайті

**Хук:** `_shop_lookup_products` — єдине місце де можна фільтрувати результати fuzzy-пошуку.
`_get_shop_domain` не підходить, бо викликається лише при увімкненому price filter.

**Кешування домену:** результат `_compute_vehicle_domain` зберігається на об'єкті `request`
щоб не виконувати SQL двічі (виклики з `_shop_lookup_products` і `_get_shop_domain`).

**Каскадний дропдаун Manufacturer → Model:**
Реалізований через vanilla JS + JSON-RPC endpoint `/add_car_to_product/get_vehicle_models`.
Альтернатива — `onchange="this.form.submit()"` (простіше, але перезавантажує сторінку).

---

## Структура файлів

```
add_car_to_product/
├── __manifest__.py
├── __init__.py
├── models/
│   ├── fleet_vehicle_engine_volume.py   # Довідник об'ємів
│   ├── fleet_vehicle_model.py           # Розширення fleet.vehicle.model
│   ├── product_template.py              # Розширення product.template
│   └── product_product.py              # Розширення product.product + display_name
├── views/
│   ├── fleet_vehicle_model_views.xml    # Form + List views для fleet
│   ├── product_template_views.xml       # Чекбокс + смарт-кнопка на шаблоні
│   ├── product_product_views.xml        # Вкладка Autoparts на варіанті
│   └── website_shop_search.xml          # Блок пошуку на /shop
├── controllers/
│   └── website_sale.py                  # Розширення WebsiteSale
├── security/
│   ├── security.xml                     # Група Car
│   └── ir.model.access.csv             # Права доступу
└── static/src/js/
    └── vehicle_search.js               # Каскадний дропдаун
```

---

## Відомі обмеження

- Пошук на сайті використовує `filtered_domain` (Python-рівень) — при великих каталогах
  ефективніше було б фільтрувати на рівні SQL через зміну `options` fuzzy-пошуку
- `for_all_models=True` товари завжди потрапляють у результати при будь-якому фільтрі авто,
  навіть якщо фільтр не відповідає їх специфіці (наприклад, фільтр по об'єму)
