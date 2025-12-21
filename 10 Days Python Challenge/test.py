import re
import json

products = ["WF- PASTA SAUCE CHESSY16X10X30GM-32", "WF- PASTA SAUCE CHESSY8X20X20GM"]

product_list = []

for product in products:
    # Remove "WF- " prefix
    cleaned = product.replace("WF- ", "")
    
    # Extract text parts (PASTA SAUCE CHESSY)
    text_parts = re.match(r"([A-Z]+)\s+([A-Z]+)\s+([A-Z]+)", cleaned)
    if text_parts:
        pasta = text_parts.group(1)      # PASTA
        sauce = text_parts.group(2)      # SAUCE
        chessy = text_parts.group(3)     # CHESSY
        
        # Create name with proper capitalization
        name = f"{pasta.capitalize()} {sauce.capitalize()} {chessy.capitalize()}"
        
        # Extract quantity (e.g., 30GM -> 30g)
        quantity_match = re.search(r'(\d+)GM', cleaned)
        if quantity_match:
            quantity = quantity_match.group(1) + "g"
        else:
            quantity = "30g"
        
        # Create dictionary for each product
        product_dict = {
            "name": name,
            "quantity": quantity
        }
        product_list.append(product_dict)

# Print in JSON format
print(json.dumps(product_list, indent=3))