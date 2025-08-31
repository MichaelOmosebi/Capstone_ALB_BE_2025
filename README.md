# HarvestPlace - Agriculture Marketplace API (MVP)

HarvestPlace is a ***backend API*** for a simple agricultural marketplace. Farmers can list postharvest products, and retailers can browse and place orders quickly and effectively.

It aims to address the global challenge of ***Food Loss***, reducing its impact on Nigerian farmers' welfare.

This MVP demonstrates ***role-based access, authentication, and basic CRUD operations*** using Django & Django REST Framework.

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

- **Wallet**
  - Wallet is created for new users upon registration with a zero balance.
  - Top-up is done without extra authorization (for now).
  - User can check wallet transactions.

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
{localhost:8000/accounts}
| Endpoint          | Method | Description                       |
|-------------------|--------|-----------------------------------|
| `/register/`      | POST   | Create a new user (returns token) |
| `/api-token-auth/`| POST   | Login (returns token)             |

### Market
{localhost:8000/market}
| Endpoint          | Method     | Description                    |
|-------------------|------------|--------------------------------|
| `/products/`      | GET        | List all products              |
| `/products/`      | POST       | Create product (farmers only)  |
| `/products/{id}/` | GET        | Retrieve product details       |
| `/products/{id}/` | PUT/PATCH  | Update product (farmer only)   |
| `/products/{id}/` | DELETE     | Delete product (farmer only)   |
| `/categories/`    | GET        | List categories (Users)        |
| `/categories/`    | POST       | Create categories (Admin only) |

### Orders
{localhost:8000/}
| Endpoint        | Method  | Description               |
|-----------------|---------|---------------------------|
| `/orders/`      | GET     | List user’s orders        |
| `/orders/`      | POST    | Create order (both roles) |
| `/orders/{id}/` | GET     | Retrieve order details    |
| `/orders/{id}/` | DELETE  | Cancel order (owner only) |

### Wallet
{localhost:8000/wallet}
| Endpoint        | Method  | Description                               |
|-----------------|---------|-------------------------------------------|
| `/`             | GET     | Show user wallet balance                  |
| `/deposits/`    | POST    | Make deposits to fund wallet (User)       |
| `/transactions/`| GET     | Retrieve users' history of transactions   |


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

4. **Run Migrations**
python manage.py migrate

# Create superuser & Run Server
python manage.py createsuperuser
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
```    "location": "Akure"```
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

Create Orders (Retailer & Farmer)
POST /orders/
Authorization: Token <### ### ###>
```{```
```  "items": [```
```    {```
```      "product": 3,```
```      "quantity": 2```
```    },```
```    {```
```      "product": 5,```
```      "quantity": 1```
```    }```
```  ]```
```}```

---------------------------------------------------------------------------------------------------------------------------------------------------

✅ Sample Workflow
- Register as farmer or retailer
- Login and copy the token
- Use token to create products (farmer) or place orders (retailer)

---------------------------------------------------------------------------------------------------------------------------------------------------

## License
____________
MIT License
____________