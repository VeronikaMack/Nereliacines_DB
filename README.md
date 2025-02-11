## Garage Management API
### A service that allows you to track free and occupied spots in the garage. <br>

1. **Register a new garage**<br>
   URL: `/garage`<br>
   Method: `PUT`<br>
   Parameters: <br>

   | **Parameter** | **Type**  | **In**  | **Required** |
   |---------------|----------|--------|--------------|
   | `id`          | string   | body   | yes          |
   | `spots`       | integer  | body   | yes          |
   | `address`     | string   | body   | yes          |

   Responses: <br>
   | Response   | Description                                 |
   |------------|---------------------------------------------|
   | `201`      | Garage registered successfully.             |
   | `400`      | Invalid input, mising id, address or spots. |

2. **Get garage details** <br>
   URL: `/garage/{garageId}`<br>
   Method: `GET`<br>
   Parameters: <br>

   | **Parameter** | **Type** | **In**  | **Required** |
   |---------------|----------|---------|--------------|
   | `garageId`    | string   | path    | yes          |

   Responses: <br>
   | Response   | Description       |
   |------------|-------------------|
   | `200`      | Garage details.   |
   | `404`      | Garage not found. |

3. **Get number of spots in garage** <br>
   URL: `/garage/{garageId}/configuration/spots`<br>
   Method: `GET`<br>
   Parameters: <br>

   | **Parameter** | **Type** | **In**  | **Required** |
   |---------------|----------|---------|--------------|
   | `garageId`    | string   | path    | yes          |

   Responses: <br>
   | Response   | Description        |
   |------------|--------------------|
   | `200`      | Number of spots.   |
   | `404`      | Garage not found.  |

4. **Change number of spots** <br>
   URL: `/garage/{garageId}/configuration/spots`<br>
   Method: `POST`<br>
   Parameters: <br>

   | **Parameter** | **Type** | **In**  | **Required** |
   |---------------|----------|---------|--------------|
   | `garageId`    | string   | path    | yes          |
   | `spots`       | integer  | body    | yes          |

   Responses: <br>
   | Response   | Description                                 |
   |------------|---------------------------------------------|
   | `200`      | Number of spots changed.                    |
   | `400`      | Invalid number (must be a positive integer).|
   | `404`      | Garage not found.                           |

5. **Occupy a spot in a garage** <br>
   URL: `/garage/{garageId}/spots/{spotNo}`<br>
   Method: `POST`<br>
   Parameters: <br>

   | **Parameter** | **Type** | **In**  | **Required** |
   |---------------|----------|---------|--------------|
   | `garageId`    | string   | path    | yes          |
   | `spotNo`      | integer  | path    | yes          |
   | `licenseNo`   | string   | body    | yes          |

   Responses: <br>
   | Response   | Description                            |
   |------------|----------------------------------------|
   | `200`      | Spot occupied successfully.            |
   | `404`      | Garage or spot not found.              |

6. **Get license plate number of spot occupant** <br>
   URL: `/garage/{garageId}/spots/{spotNo}`<br>
   Method: `GET`<br>
   Parameters: <br>

   | **Parameter** | **Type** | **In**  | **Required** |
   |---------------|----------|---------|--------------|
   | `garageId`    | string   | path    | yes          |
   | `spotNo`      | integer  | path    | yes          |

   Responses: <br>
   | Response   | Description                            |
   |------------|----------------------------------------|
   | `200`      | License plate number of occupant.      |
   | `204`      | Spot is unoccupied.                    |
   | `404`      | Garage not found.                      |

7. **Free a spot in a garage** <br>
   URL: `/garage/{garageId}/spots/{spotNo}`<br>
   Method: `DELETE`<br>
   Parameters: <br>

   | **Parameter** | **Type** | **In**  | **Required** |
   |---------------|----------|---------|--------------|
   | `garageId`    | string   | path    | yes          |
   | `spotNo`      | integer  | path    | yes          |

   Responses: <br>
   | Response   | Description           |
   |------------|-----------------------|
   | `200`      | Spot freed.           |
   | `400`      | Spot not found.       |
   | `404`      | Garage not found.     |

8. **Get garage occupancy statistics** <br>
   URL: `/garage/{garageId}/status`<br>
   Method: `GET`<br>
   Parameters: <br>

   | **Parameter** | **Type** | **In**  | **Required** |
   |---------------|----------|---------|--------------|
   | `garageId`    | string   | path    | yes          |

   Responses: <br>
   | Response   | Description                            |
   |------------|----------------------------------------|
   | `200`      | Number of free and occupied spots.     |
   | `404`      | Garage not found.                      |
