# ML Enginner Code Challenge


This project is a simple e-commerce platform where users can browse products, add them to their cart, and place orders. Admin users can manage the product listings by adding, editing, and removing products from the platform.

## Features

- **Regular Users**:
  - Browse available products.
  - Add products to the cart.
  - View cart and place orders.
  
- **Admin Users**:
  - Manage (add, edit, remove) product listings.
  - Cannot place orders or add products to the cart.

## User Accounts

The platform comes with pre-configured user accounts for demonstration purposes:

1. **Admin Account**:
   - **Username**: `admin`
   - **Password**: `admin`
   - Admin users have the ability to add, edit, and remove products but cannot place orders.

2. **Regular User Account**:
   - **Username**: `teste1`
   - **Password**: `12345`
   - Regular users can browse products, add items to their cart, and place orders.


## How to Run
1. Clone the repository.
2. Install dependencies by running `pip install -r requirements.txt`.
3. Run the `app.py` file using `python app.py`.
4. Run tests using `python -m unittest tests.py`.


## Assumptions Made
- **Admin vs. Regular User Roles**: 
  - Admin users are restricted from making purchases, and this distinction was critical in determining both the user experience and permissions. 
  - Admins focus solely on product management.

- **Stock Management**: 
  - For simplicity, stock management decreases after an order is placed.


## Learnings and Challenges
- **Session Management**: 
  - Implementing role-based session management was critical to ensuring the correct user experience. I had to ensure the admin could only manage products, while regular users could add items to the cart and place orders.

- **Cart and Order Flow**: 
  - Understanding the flow between adding items to a cart and placing an order was crucial, and required handling edge cases like cart clearing post-order.


## Approach Taken
- **Role-Based Access**: 
  - The system differentiates between admins and regular users, with customized experiences and restrictions. For example, only admins can manage products, while regular users can place orders.

- **Separation of Responsibilities**: 
  - Admins handle product management, while regular users manage their shopping experience. This clear separation helped avoid feature bloat and made user actions more predictable.


## Trade-offs and Decisions
- **Simple Authentication**: 
  - Instead of implementing a more complex authentication system (e.g., OAuth or token-based), I opted for basic username-password authentication to focus on core functionality of the platform.
