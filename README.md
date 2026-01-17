# Django Stripe Checkout Assignment – VipraTech

This project is a Django-based mini e-commerce application built as part of the **VipraTech Django Developer assignment**.  
It demonstrates product listing, cart management, Stripe (test mode) payment integration, and order tracking — all within a single-page user experience.

---

## 🌐 Live Project URL

The project is deployed and accessible at:

👉 https://ecom.kuldeepsaini.in

Stripe is configured in test mode, so test card details can be used safely.

## 📌 Assumptions

Since the assignment specification was intentionally minimal, the following assumptions were made:

- Products are limited and predefined (stored in the database).
- Users must be authenticated to add items to the cart and place orders.
- Prices displayed on the frontend are for **UX only**; all billing calculations are done on the backend.
- Stripe **Checkout (test mode)** is sufficient and preferred over Payment Intents for simplicity and reliability.
- Each user can have only **one active pending checkout** at a time.
- Orders and cart items are user-scoped.

---

## 🧱 Tech Stack

- **Backend:** Django  
- **Database:** MySQL  
- **Payments:** Stripe (Test Mode)  
- **Frontend:** Django Templates, Bootstrap 5  
- **Auth:** Django Authentication  
- **Utilities:** Django Messages Framework, mathfilters  

---

## 🛒 Application Flow

1. User logs in  
2. Products are displayed on the main page  
3. User selects quantity and adds items to cart  
4. Cart is shown in a modal (no page reload)  
5. User clicks **Checkout**  
6. Backend validates cart and creates Stripe Checkout session  
7. User completes payment on Stripe  
8. After payment:
   - Order is marked **PAID**
   - Order appears in the **My Orders** modal on the same page  

---

## 💳 Stripe Integration

- Stripe is used strictly in **test mode**
- Stripe Checkout is used for payment handling
- Payment amount is **always calculated on the backend**
- Stripe session ID is stored with the order to track payment state

---

## 🔁 Preventing Double Charges & Inconsistent State

### Backend protections
- Checkout blocked if cart is empty
- Only **one PENDING order per user**
- Idempotent delete operations for cart items
- Order marked PAID only once

### Frontend protections
- Buttons disabled after click
- Dynamic pricing used only for display

---

## ▶️ Setup & Run Instructions

```bash
git clone https://github.com/kuldeepsaini65/ECOMM.git
cd ECOMM
python -m venv venv
source venv/bin/activate
pip install -r req.txt
python manage.py migrate
python manage.py runserver
```

---

## 🧪 Stripe Test Card

```
4242 4242 4242 4242
Any future expiry
Any CVC
```

---

## 🕒 Time Spent

**Total time spent:** ~7–8 hours

---

## ⚠️ Known Limitations

- No stock management
- No refunds
- Docker not included

---

## 📄 Notes

This project prioritizes backend correctness, idempotency, and clear design decisions over frontend complexity.
