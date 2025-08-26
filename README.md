# HarvestPlace - Agriculture Marketplace API (MVP)

HarvestPlace is a **backend API** for a simple agricultural marketplace. Farmers can list postharvest products, and retailers can browse and place orders quickly and effectively.

It aims to address the global challenge on Food Loss, and reducing the impact of this on the welfare of Nigerian farmers.

This MVP demonstrates **role-based access, authentication, and basic CRUD operations** using Django & Django REST Framework.

---------------------------------------------------------------------------------------------------------------------------------------------------

## 🛠️ Tech Stack

- **Backend:** Python, Django, Django REST Framework  
- **Authentication:** Token-based (DRF `rest_framework.authtoken`)  
- **Database:** SQLite
- **Testing:** DRF `APITestCase`  
- **Pillow:** (for image uploads)

---------------------------------------------------------------------------------------------------------------------------------------------------

## ⚡ Features

- **User Management**
  - User registration (`/register/`) with role (`farmer` / `retailer`) and location
  - Login with token authentication (`/api-token-auth/`)

- **Products**
  - CRUD operations for farmers
  - Image upload support
  - Search & filter by `name`, `category`, `location`
  - Role-based permissions (only farmers can create/update/delete products)

- **Orders**
  - Create orders (both roles)
  - Users can only view their own orders
  - Delete own orders

- **Role-Based Access Control**
  - Farmers manage products
  - Retailers can only create orders
  - Permissions enforced at API level

- **Minimal Tests**
  - Authentication
  - Product CRUD
  - Order creation
  - Role-based restrictions
  - Image upload

---------------------------------------------------------------------------------------------------------------------------------------------------

## 📝 API Endpoints

### Authentication
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/register/` | POST | Create a new user (returns token) |
| `/api-token-auth/` | POST | Login (returns token) |

### Products
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/products/` | GET | List all products |
| `/products/` | POST | Create product (farmers only) |
| `/products/{id}/` | GET | Retrieve product details |
| `/products/{id}/` | PUT/PATCH | Update product (owner only) |
| `/products/{id}/` | DELETE | Delete product (owner only) |

### Orders
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/orders/` | GET | List user’s orders |
| `/orders/` | POST | Create order (both roles) |
| `/orders/{id}/` | GET | Retrieve order details |
| `/orders/{id}/` | DELETE | Delete order (owner only) |

---------------------------------------------------------------------------------------------------------------------------------------------------

## ⚙️ Setup Instructions

1. **Clone repo**
```bash```
git clone https://github.com/yourusername/harvestplace.git
cd harvestplace

2. **Create Virtual Environment**
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

3. **Install Dependencies**
pip install -r requirements.txt

4. **Run Migrations & Run Server**
pip install -r requirements.txt
python manage.py runserver

5. **Run Test**
```Ensure that the App behaves as outlined in Features above.```
python manage.py test


## Usage Example
### Register a Farmer
POST /register/
```{```
```    "username": "john",```
```    "email": "john@example.com",```
```    "password": "pass1234",```
```    "role": "farmer",```
```    "location": "Lagos"```
```}```

POST /api-token-auth/
```{```
```    "email": "john@example.com",```
```    "password": "pass1234"```
```}```

Create a Product (Farmer only)
POST /products/
Authorization: Token <### ### ###>
```{```
```    "name": "Tomatoes",```
```    "category": "Vegetable",```
```    "location": "Lagos",```
```    "price": 100,```
```    "image": <file>```
```}```

---------------------------------------------------------------------------------------------------------------------------------------------------

## License
________________________________________________________
MIT License
________________________________________________________