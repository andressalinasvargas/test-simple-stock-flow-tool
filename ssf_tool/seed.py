"""Database seeder via HTTP API for demo data."""

import os
import sys
from typing import Dict, List
from .client import ApiClient

DEMO_PRODUCTS = [
    {"name": "Martillo Galponero 20oz", "price": 38000.00, "stock": 25, "category": "Herramientas"},
    {"name": "Juego Destornilladores 6 Piezas", "price": 42000.00, "stock": 18, "category": "Herramientas"},
    {"name": "Cinta Aislante 20m Negra", "price": 4500.00, "stock": 100, "category": "Electricidad"},
    {"name": "Breaker Monopolar 20A", "price": 18500.00, "stock": 40, "category": "Electricidad"},
    {"name": "Tubo PVC Presión 1/2 pulgada 6m", "price": 16000.00, "stock": 30, "category": "Fontanería"},
    {"name": "Llave de Paso 1/2 pulgada", "price": 12500.00, "stock": 22, "category": "Fontanería"},
    {"name": "Pintura Vinilo Blanco Tipo 1 Galón", "price": 68000.00, "stock": 15, "category": "Pinturas"},
    {"name": "Brocha Monamur 3 pulgadas", "price": 9500.00, "stock": 35, "category": "Pinturas"},
    {"name": "Caja Organizadora 15 Compartimentos", "price": 28000.00, "stock": 12, "category": "General"},
]


def run_seed() -> None:
    base_url = os.environ.get("API_BASE_URL", "http://localhost:8000")
    admin_email = os.environ.get("ADMIN_EMAIL", "admin@stockflow.local")
    admin_password = os.environ.get("ADMIN_PASSWORD", "Admin123*!")

    print(f"[*] Conectando a Simple Stock Flow API en {base_url}...")
    client = ApiClient(base_url)

    # 1. Autenticar como Administrador
    print(f"[*] Iniciando sesión como administrador ({admin_email})...")
    login_res = client.request("POST", "/api/auth/login", {
        "username": admin_email,
        "password": admin_password,
    })
    admin_token = login_res["accessToken"]
    client.set_token(admin_token)
    print("    [+] Sesión de administrador iniciada con éxito.")

    # 2. Obtener categorías existentes
    print("[*] Consultando categorías disponibles...")
    categories = client.request("GET", "/api/categories")
    cat_map: Dict[str, str] = {cat["name"].lower(): cat["id"] for cat in categories}
    print(f"    [+] {len(categories)} categorías encontradas.")

    # 3. Consultar productos existentes para garantizar idempotencia
    print("[*] Verificando productos existentes (idempotencia)...")
    existing_products_res = client.request("GET", "/api/products?page=1&size=100")
    existing_names = {p["name"].lower() for p in existing_products_res.get("items", [])}

    # 4. Crear productos no existentes
    created_product_ids: List[str] = []
    for p in DEMO_PRODUCTS:
        p_name = p["name"]
        if p_name.lower() in existing_names:
            print(f"    [-] Omitiendo '{p_name}': ya existe en catálogo.")
            continue

        cat_id = cat_map.get(p["category"].lower())
        if not cat_id:
            cat_id = list(cat_map.values())[0]

        created = client.request("POST", "/api/products", {
            "name": p_name,
            "price": p["price"],
            "stock": p["stock"],
            "categoryId": cat_id,
        })
        p_id = created["id"]
        created_product_ids.append(p_id)
        print(f"    [+] Creado producto: '{p_name}' (ID: {p_id})")

    # 5. Registrar o usar vendedor de demostración
    seller_username = "vendedor.demo"
    seller_password = "Password123*!"
    print(f"[*] Asegurando usuario vendedor ('{seller_username}')...")
    try:
        client.request("POST", "/api/auth/register", {
            "username": seller_username,
            "password": seller_password,
            "role": "seller",
        })
        print("    [+] Vendedor registrado.")
    except Exception as e:
        if "ya existe" in str(e):
            print("    [-] El vendedor ya existía.")
        else:
            print(f"    [!] Registro de vendedor: {e}")

    # Iniciar sesión como vendedor
    seller_client = ApiClient(base_url)
    seller_login = seller_client.request("POST", "/api/auth/login", {
        "username": seller_username,
        "password": seller_password,
    })
    seller_client.set_token(seller_login["accessToken"])

    # 6. Registrar una venta de demostración si hay productos disponibles
    catalog = seller_client.request("GET", "/api/products?page=1&size=10")
    items = catalog.get("items", [])
    if items:
        prod1 = items[0]
        print(f"[*] Registrando venta de demostración para '{prod1['name']}'...")
        sale_res = seller_client.request("POST", "/api/sales", {
            "lines": [
                {"productId": prod1["id"], "quantity": 1}
            ]
        })
        print(f"    [+] Venta registrada con éxito (ID: {sale_res['id']}).")

    print("[*] Proceso de siembra finalizado exitosamente.")
