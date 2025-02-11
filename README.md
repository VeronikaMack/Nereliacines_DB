## E-Shop
### This service stores client information, product catalog and client orders. It also provides basic statistics for shop owners. <br>

1. **Register a new client**<br>
   URL: `/clients`<br>
   Method: `PUT`<br>
   Parameters: <br>

   | **Parameter** | **Type**  | **In**  | **Required** |
   |---------------|-----------|---------|--------------|
   | `id`          | string    | body    | no           |
   | `name`        | string    | body    | yes          |
   | `email `      | string    | body    | yes          |
 
   Responses: <br>
   | Response        | Description                                 |
   |-----------------|---------------------------------------------|
   | `201` `clientId`| Client registered.                          |
   | `400`           | Invalid input, missing name or email.       |

2. **Get client details**<br>
   URL: `/clients/{clientId}`<br>
   Method: `GET`<br>
   Parameters: <br>

   | **Parameter** | **Type**  | **In**  | **Required** |
   |---------------|-----------|---------|--------------|
   | `clientId`    | string    | path    | yes          |
 
   Responses: <br>
   | Response   | Description            |
   |------------|------------------------|
   | `200`      | Client details.        |
   | `404`      | Client not found.      |

3. **Delete a client and their associated orders**<br>
   URL: `/clients/{clientId}`<br>
   Method: `DELETE`<br>
   Parameters: <br>

   | **Parameter** | **Type**  | **In**  | **Required** |
   |---------------|-----------|---------|--------------|
   | `clientId`    | string    | path    | yes          |
 
   Responses: <br>
   | Response   | Description            |
   |------------|------------------------|
   | `204`      | Client deleted.        |
   | `404`      | Client not found.      |

4. **Register a new product**<br>
   URL: `/products`<br>
   Method: `PUT`<br>
   Parameters: <br>

   | **Parameter** | **Type**            | **In**  | **Required** |
   |---------------|---------------------|---------|--------------|
   | `id`          | string              | body    | no           |
   | `name`        | string              | body    | yes          |
   | `category`    | string              | body    | no           |
   | `price`       | number &lt;float&gt;| body    | yes          |
 
   Responses: <br>
   | Response         | Description                          |
   |------------------|--------------------------------------|
   | `201` `productId`| Product registered.                  |
   | `400`            | Invalid input, missing name or price.|

5. **List all products (optionally in category)**<br>
   URL: `/products`<br>
   Method: `GET`<br>
   Parameters: <br>

   | **Parameter** | **Type**  | **In**  | **Required** |
   |---------------|-----------|---------|--------------|
   | `category`    | string    | query   | no           |
 
   Responses: <br>
   | Response   | Description                          |
   |------------|--------------------------------------|
   | `200`      | List of products.                    |

6. **Get product details**<br>
   URL: `/products/{productId}`<br>
   Method: `GET`<br>
   Parameters: <br>

   | **Parameter** | **Type**  | **In**  | **Required** |
   |---------------|-----------|---------|--------------|
   | `productId`   | string    | path    | yes          |
 
   Responses: <br>
   | Response   | Description                          |
   |------------|--------------------------------------|
   | `200`      | Product details.                     |
   | `404`      | Product not found.                   |

7. **Delete a product**<br>
   URL: `/products/{productId}`<br>
   Method: `DELETE`<br>
   Parameters: <br>

   | **Parameter** | **Type**  | **In**  | **Required** |
   |---------------|-----------|---------|--------------|
   | `productId`   | string    | path    | yes          |
 
   Responses: <br>
   | Response   | Description                          |
   |------------|--------------------------------------|
   | `204`      | Product deleted.                     |
   | `404`      | Product not found.                   |

8. **Create a new order**<br>
   URL: `/orders`<br>
   Method: `PUT`<br>
   Parameters: <br>

   | **Parameter**| **Type**         | **In**         | **Required** |
   |--------------|------------------|----------------|--------------|
   | `clientId `  | string           | body           | yes          |
   | `items`      | array of objects | body           | yes          |
   | `productId`  | string           | within `items` for each item| yes|
   | `quantity`   | integer          | within `items` for each item| yes|
 
   Responses: <br>
   | Response       | Description                               |
   |----------------|-------------------------------------------|
   | `201` `orderId`| Order created.                            |
   | `400`          | Invalid input, missing clientId or items. |
   | `404`          | Client not found.                         |

9. **Get client orders**<br>
   URL: `/clients/{clientId}/orders`<br>
   Method: `GET`<br>
   Parameters: <br>

   | **Parameter** | **Type**         | **In**  | **Required** |
   |---------------|------------------|---------|--------------|
   | `clientId `   | string           | path    | yes          |
 
   Responses: <br>
   | Response   | Description                           |
   |------------|---------------------------------------|
   | `200`      | Client orders.                        |

10. **Get top 10 clients by number of orders placed**<br>
    URL: `/statistics/top/clients` <br> 
    Method: `GET`  <br>
    Parameters: `None`  <br>
    
    Responses:  
    
    | Response | Description                             |
    |----------|-----------------------------------------|
    | `200`    | Top clients by number of orders placed. |

11. **Get top 10 products by total quantity ordered**<br>
    URL: `/statistics/top/products` <br> 
    Method: `GET`  <br>
    Parameters: `None`  <br>
    
    Responses:  
    
    | Response | Description                             |
    |----------|-----------------------------------------|
    | `200`    | Top products by total quantity ordered. |

12. **Get total number of orders placed**<br>
    URL: `/statistics/orders/total` <br> 
    Method: `GET`  <br>
    Parameters: `None`  <br>
    
    Responses:  
    
    | Response | Description        |
    |----------|--------------------|
    | `200`    | Orders statistics. |

13. **Get total value of all orders placed**<br>
    URL: `/statistics/orders/totalValue` <br> 
    Method: `GET`  <br>
    Parameters: `None`  <br>
    
    Responses:  
    
    | Response | Description        |
    |----------|--------------------|
    | `200`    | Orders statistics. |

14. **Delete all data from the database**<br>
    URL: `/cleanup` <br> 
    Method: `POST`  <br>
    Parameters: `None`  <br>
    
    Responses:  
    
    | Response | Description       |
    |----------|-------------------|
    | `204`    | Data deleted.     |
    
