from fastapi import APIRouter, HTTPException
import json
import os

router = APIRouter(prefix="/products", tags=["products"])

# Путь к файлу с данными
DATA_FILE = "shoes.json"

# Начальные данные, если файла нет
INITIAL_DATA = [
    {"id": 1, "name": "Кроссовки Nike", "size": 42, "price": 5000},
    {"id": 2, "name": "Ботинки Timberland", "size": 43, "price": 8000},
    {"id": 3, "name": "Кеды Converse", "size": 39, "price": 4000}
]

def get_data():
    """Читает данные из файла"""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(INITIAL_DATA, f, ensure_ascii=False)
        return INITIAL_DATA.copy()
    
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    """Сохраняет данные в файл"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Получить все товары
@router.get("/")
async def get_products(sort: str = None):
    shoes = get_data()
    
    if sort == "asc":
        shoes.sort(key=lambda x: x["name"])
    elif sort == "desc":
        shoes.sort(key=lambda x: x["name"], reverse=True)
    
    return shoes

# Получить один товар
@router.get("/{id}")
async def get_product(id: int):
    shoes = get_data()
    for shoe in shoes:
        if shoe["id"] == id:
            return shoe
    raise HTTPException(status_code=404, detail="Товар не найден")

# Создать товар
@router.post("/")
async def create_product(name: str, size: int, price: float):
    shoes = get_data()
    new_id = max([s["id"] for s in shoes]) + 1 if shoes else 1
    
    new_shoe = {
        "id": new_id,
        "name": name,
        "size": size,
        "price": price
    }
    
    shoes.append(new_shoe)
    save_data(shoes)
    return new_shoe

# Обновить товар
@router.put("/{id}")
async def update_product(id: int, name: str, size: int, price: float):
    shoes = get_data()
    
    for i, shoe in enumerate(shoes):
        if shoe["id"] == id:
            shoes[i] = {
                "id": id,
                "name": name,
                "size": size,
                "price": price
            }
            save_data(shoes)
            return shoes[i]
    
    raise HTTPException(status_code=404, detail="Товар не найден")

# Удалить товар
@router.delete("/{id}")
async def delete_product(id: int):
    shoes = get_data()
    
    for i, shoe in enumerate(shoes):
        if shoe["id"] == id:
            deleted = shoes.pop(i)
            save_data(shoes)
            return {"message": "Товар удален", "item": deleted}
    
    raise HTTPException(status_code=404, detail="Товар не найден")