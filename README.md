# Python Shopify Discount API Manager:

---
#### Note: Based off https://github.com/anduslim/Shopify-Discount-Codes, with original work https://github.com/MartinAmps/Shopify-Private-APIs
---

## Requirements

refer to requirements.txt. To install dependencies, run `pip install -r requirements.txt`

## Usage

After cloning, 
```python
import json
from shopify_discount_manager import ShopifyDiscountManager

# Initialize a manager for your store: shopify_shop_name.myshopify.com
discount_manager = ShopifyDiscountManager(shopify_shop_name, login_email, password)

# Create a discount for 10% off all order items
response = discount_manager.create_discount_code(**{'code': "TestMagicCode", 'discount_type': 'percentage', 'value':10})

content = json.loads(response.content)
shopify_discount_id = content['discount']['id']

# Disable discount code
discount_manager.disable_discount_code(shopify_discount_id)
 ```
