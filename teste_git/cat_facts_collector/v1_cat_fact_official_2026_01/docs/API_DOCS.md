# 📡 API Documentation - Cat-Fact Heroku

## Base URL
```
https://cat-fact.herokuapp.com
```

## Endpoints

### GET /facts
Retorna lista de facts sobre gatos.

**Response:**
```json
[
  {
    "_id": "58e008800aac31001185ed05",
    "text": "The Egyptian Mau is probably the oldest breed of cat.",
    "type": "cat",
    "user": {
      "_id": "58e007480aac31001185ecef"
    },
    "upvotes": 5,
    "userUpvoted": false,
    "createdAt": "2018-01-04T01:10:54.673Z",
    "updatedAt": "2020-08-23T20:20:01.611Z"
  }
]
```

### GET /facts/random
Retorna um fact aleatório.

**Response:**
```json
{
  "_id": "58e008800aac31001185ed05",
  "text": "The Egyptian Mau is probably the oldest breed of cat.",
  "type": "cat",
  "upvotes": 5
}
```

## Status
⚠️ **API OFFLINE** desde 2024
