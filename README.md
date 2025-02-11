## Flight Search Service
### This service stores flight information between cities. It allows users to find the best deal to any destination. <br>

1. **Register a new city**<br>
   URL: `/cities`<br>
   Method: `PUT`<br>
   Parameters: <br>

   | **Parameter**        | **Type**  | **In**  | **Required** |
   |----------------------|-----------|---------|--------------|
   | `name` (of the city) | string    | body    | yes          |
   | `country`            | string    | body    | yes          |
 
   Responses: <br>
   | Response         | Description                       |
   |------------------|-----------------------------------|
   | `201`            | City registered successfully.     |
   | `400`            | Could not register the city, it exists or mandatory attributes are missing.   |

2. **Get cities**<br>
   URL: `/cities`<br>
   Method: `GET`<br>
   Parameters: <br>

   | **Parameter** | **Type**  | **In**  | **Required** |
   |---------------|-----------|---------|--------------|
   | `country`     | string    | query   | no           |
 
   Responses: <br>
   | Response         | Description            |
   |------------------|------------------------|
   | `200`            | Registered cities.     |

3. **Get city**<br>
   URL: `/cities/{name}`<br>
   Method: `GET`<br>
   Parameters: <br>

   | **Parameter** | **Type**  | **In**  | **Required** |
   |---------------|-----------|---------|--------------|
   | `name`        | string    | path    | yes          |
 
   Responses: <br>
   | Response         | Description       |
   |------------------|-------------------|
   | `200`            | City details.     |
   | `404`            | City not found.   |

4. **Register an Airport**<br>
   URL: `/cities/{name}/airports`<br>
   Method: `PUT`<br>
   Parameters: <br>

   | **Parameter**       | **Type**  | **In**  | **Required** |
   |---------------------|-----------|---------|--------------|
   | `name` (city)       | string    | path    | yes          |
   | `code`              | string    | body    | no           |
   | `name`  (airport)   | string    | body    | yes          |
   | `numberOfTerminals` | integer   | body    | no           |
   | `address`           | string    | body    | no           |
 
   Responses: <br>
   | Response         | Description       |
   |------------------|-------------------|
   | `201`            | Airport created.  |
   | `400`            | Airport could not be created due to missing data or city the airport is registered in is not registered in the system.   |

5. **Get airports in a city**<br>
   URL: `/cities/{name}/airports`<br>
   Method: `GET`<br>
   Parameters: <br>

   | **Parameter**       | **Type**  | **In**  | **Required** |
   |---------------------|-----------|---------|--------------|
   | `name`              | string    | path    | yes          |
 
   Responses: <br>
   | Response         | Description    |
   |------------------|----------------|
   | `200`            | All airports.  |

6. **Get airport**<br>
   URL: `/airports/{code}`<br>
   Method: `GET`<br>
   Parameters: <br>

   | **Parameter**       | **Type**  | **In**  | **Required** |
   |---------------------|-----------|---------|--------------|
   | `code`              | string    | path    | yes          |
 
   Responses: <br>
   | Response         | Description     |
   |------------------|-----------------|
   | `200`            | Airport details.|
   | `404`            | City not found. |

7. **Register new flight**<br>
   Flights are directional. <br>
   URL: `/flights`<br>
   Method: `PUT`<br>
   Parameters: <br>

   | **Parameter**        | **Type**              | **In**  | **Required** |
   |----------------------|-----------------------|---------|--------------|
   | `number` (of flight) | string                | body    | yes          |
   | `fromAirport`        | string                | body    | yes          |
   | `toAirport`          | string                | body    | yes          |
   | `price`              | number &lt;double&gt; | body    | yes          |
   | `flightTimeInMinutes`| integer               | body    | yes          |
   | `operator`           | string                | body    | yes          |
 
   Responses: <br>
   | Response         | Description     |
   |------------------|-----------------|
   | `201`            | Flight created. |
   | `400`            | Flight could not be created due to missing data. |

8. **Get full flight information**<br>
   URL: `/flights/{flightNo}`<br>
   Method: `GET`<br>
   Parameters: <br>

   | **Parameter**        | **Type**              | **In**  | **Required** |
   |----------------------|-----------------------|---------|--------------|
   | `flightNo`           | string                | path    | yes          |

 
   Responses: <br>
   | Response         | Description     |
   |------------------|-----------------|
   | `200`            | Flight details. |
   | `404`            | Flight not found. |

9. **Find flights to and from city**<br>
   Find flights between two cities. Will not search for flights with more than 3 stops. <br>
   URL: `/search/flights/{fromCity}/{toCity}`<br>
   Method: `GET`<br>
   Parameters: <br>

   | **Parameter**        | **Type**              | **In**  | **Required** |
   |----------------------|-----------------------|---------|--------------|
   | `fromCity`           | string                | path    | yes          |
   | `toCity`             | string                | path    | yes          |

 
   Responses: <br>
   | Response         | Description     |
   |------------------|-----------------|
   | `200`            | Flights between specified cities. |
   | `404`            | Flights not found. |

10. **Cleanup**<br>
    URL: `/cleanup` <br> 
    Method: `POST`  <br>
    Parameters: `None`  <br>
    
    Responses:  
    
    | Response | Description        |
    |----------|--------------------|
    | `200`    | Cleanup successful. |
