# Todolist APIs

---

## Header Parameters

The following header parameters are required across all APIs:

|  Parameter  |  Type  | Required |          Description           |
|:-----------:|:------:|:--------:|:------------------------------:|
| X-User-Code | String |   Yes    | Unique identifier for the user |

---

## List of APIs

1. [Get Categories](#get-categories)
2. [Add Category](#add-category)
3. [Update Category](#update-category)
4. [Delete Category](#delete-category)

---

## Get Categories

- This API returns a list of all categories belonging to the authenticated user.
- Categories are filtered by authenticated user and only active categories are returned.

### Endpoint

```http request
GET /v1/categories
```

### Query Parameters

None

### Response

```json
{
  "success": true,
  "code": 200,
  "message": "",
  "data": [
    {
      "code": "C1642123456789",
      "label": "Work"
    },
    {
      "code": "C1642123456790",
      "label": "Personal"
    },
    {
      "code": "C1642123456791",
      "label": "Shopping"
    }
  ]
}
```

### Error Response

```json
{
  "success": false,
  "code": 500,
  "message": "Sorry, something went wrong on our side"
}
```

---

## Add Category

- This API creates a new category for the authenticated user.
- The category label must be alphanumeric.
- A unique category code is automatically generated based on the current timestamp.

### Endpoint

```http request
POST /v1/categories
```

### Request Body Parameters

| Parameter |  Type  | Required |                   Description                    |
|:---------:|:------:|:--------:|:------------------------------------------------:|
|   label   | String |   Yes    | Category label (must be alphanumeric characters) |

### Payload

```json
{
  "label": "Work"
}
```

### Response

```json
{
  "success": true,
  "code": 200,
  "message": "Category added successfully!",
  "data": {}
}
```

### Error Response

```json
{
  "success": false,
  "code": 400,
  "message": "label must be alphanumeric"
}
```

---

## Update Category

- This API updates an existing category belonging to the authenticated user.
- Users can only update categories they own.
- The category must exist and be active.

### Endpoint

```http request
PUT /v1/categories/{code}
```

### Path Parameters

| Parameter |  Type  | Required |         Description         |
|:---------:|:------:|:--------:|:---------------------------:|
|   code    | String |   Yes    | Unique code of the category |

### Request Body Parameters

| Parameter |  Type  | Required |    Description     |
|:---------:|:------:|:--------:|:------------------:|
|   label   | String |   Yes    | New category label |

### Payload

```json
{
  "label": "Work Tasks"
}
```

### Response

```json
{
  "success": true,
  "code": 200,
  "message": "Category updated successfully!",
  "data": {}
}
```

### Error Response

```json
{
  "success": false,
  "code": 400,
  "message": "Category C1642123456789 does not exist!"
}
```

```json
{
  "success": false,
  "code": 403,
  "message": "Forbidden action"
}
```

---

## Delete Category

- This API deletes a category belonging to the authenticated user.
- Users can only delete categories they own.
- The category must exist and be active.

### Endpoint

```http request
DELETE /v1/categories/{code}
```

### Path Parameters

| Parameter |  Type  | Required |         Description         |
|:---------:|:------:|:--------:|:---------------------------:|
|   code    | String |   Yes    | Unique code of the category |

### Response

```json
{
  "success": true,
  "code": 200,
  "message": "Category deleted successfully!",
  "data": {}
}
```

### Error Response

```json
{
  "success": false,
  "code": 400,
  "message": "Category C1642123456789 does not exist!"
}
```

```json
{
  "success": false,
  "code": 403,
  "message": "Forbidden action"
}
```

---
## Add task

- This API creates a new task for the authenticated user.
- A unique task code is automatically generated based on the current timestamp.

### Endpoint

```http request
POST /v1/tasks
```

### Request Body Parameters

|   Parameter   |  Type  | Required | Description |
|:-------------:|:------:|:--------:|:-----------:|
|     title     | String |   Yes    |             |        
|  description  | String |    No    |             |        
| priority_code | String |    No    |             |        
|  status_code  | String |    No    |             |        
| category_code | String |    No    |             |        


### Payload

```json
{
  "title": "Home work",
  "description": "Home work",
  "priority_code": "High",
  "status_code": "Pending",
  "category_code": "C1752504942590"
}
```

### Response

```json
{
  "success": true,
  "code": 200,
  "message": "Task added successfully!",
  "data": {}
}
```

### Error Response

```json
{
  "success": false,
  "code": 400,
  "message": "title must not be empty"
}
```
