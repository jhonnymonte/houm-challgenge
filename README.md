
# Real Estate Management API

## Description

This project is an API to manage employees, properties and property visits. It is developed using FastAPI and follows the Repository design pattern.

## Configuration and Execution

### Prerequisites

- Docker
- Docker Compose

### Steps to Run

1. Clone this repository.
2. Navigate to the project directory.
3. Build and run the containers using Docker Compose:
   ```sh
   docker-compose up --build
   
4. To run the project go to
      ```sh
   http://localhost:8000/
   
## API Reference
#### these are the APIs for testing basic functionality to better understand the APIs and their crud functions you can look at the documentation in '/docs'.

#### Register an Employee

```http
  POST/auth/register-employee
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `name` | `string` | **Required**. |
| `email` | `string` | **Required**.|
| `password` | `string` | **Required**|

#### Get item

```http
  POST /auth/token
```
### Headers
#### Content-Type = application/x-www-form-urlencoded
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`      | `string` | **Required**. email of the registered user|
| `password`      | `string` | **Required**. password |


#### Register a Property

```http
  POST/properties/
```
| Headers | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` | `bearer` | **Required**. your access token |

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `address` | `string` | **Required**. |
| `location` | `string` | **Required**.|
| `price` | `int` | **Required**|
| `description` | `string` | **Required**|

#### it's import the correct format of the address here are 3 examples
##### address = "Pío Nono 450, Recoleta, Región Metropolitana, Chile"
##### address = "Plaza de Armas, Santiago, Región Metropolitana, Chile"
##### address = "Av. Andrés Bello 2425, Providencia, Región Metropolitana, Chile",
##### for more information about the format of the address need to check the oficial page of the GEO API "https://opencagedata.com"

#### Register a Visit

```http
  POST/visits/
```

| Headers | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` | `bearer` | **Required**. your access token |

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `employee_id` | `string` | **Required**|
| `property_id` | `int` | **Required**. |
| `visit_date` | `date` | **Required**.|
| `visitor_name` | `string` | **Required**|
| `visitor_email` | `string` | **Required**|
| `feedback` | `string` | **Required**|

#### Register an Employee

```http
  GET/visits/employee/{employee_id}
```

#### Get analytics for an employee
##### this API returns the total number of visits made by the employee and the total km traveled in meters.


```http
  GET/analytics/visits/employee/{employee_id}
```

### To Do more easier the testing i create a postman json collection to import and run the test. just import the file in your postman browser