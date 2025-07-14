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

### Payload

```json
{
  "label": "Work"
}
```

### Request Body Parameters

| Parameter |  Type  | Required |                   Description                    |
|:---------:|:------:|:--------:|:------------------------------------------------:|
|   label   | String |   Yes    | Category label (must be alphanumeric characters) |

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

### Payload

```json
{
  "label": "Work Tasks"
}
```

### Request Body Parameters

| Parameter |  Type  | Required |    Description     |
|:---------:|:------:|:--------:|:------------------:|
|   label   | String |   Yes    | New category label |

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

- This API soft deletes a category belonging to the authenticated user.
- Users can only delete categories they own.
- The category must exist and be active.
- This is a soft delete operation (sets is_active = 0).

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