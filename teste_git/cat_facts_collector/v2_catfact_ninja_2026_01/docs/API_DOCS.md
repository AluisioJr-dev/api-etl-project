# 📡 API Documentation - catfact.ninja

## Base URL
```
https://catfact.ninja
```

## Endpoints

### GET /facts
Retorna lista paginada de facts sobre gatos.

**Query Parameters:**
- `limit` (int, optional): Número de facts por página (default: 10, max: 100)
- `page` (int, optional): Número da página (default: 1)

**Response:**
```json
{
  "current_page": 1,
  "data": [
    {
      "fact": "Cats have 32 muscles in each ear.",
      "length": 38
    },
    {
      "fact": "Cats sleep 16 hours a day.",
      "length": 27
    }
  ],
  "first_page_url": "https://catfact.ninja/facts?page=1",
  "from": 1,
  "last_page": 34,
  "last_page_url": "https://catfact.ninja/facts?page=34",
  "next_page_url": "https://catfact.ninja/facts?page=2",
  "path": "https://catfact.ninja/facts",
  "per_page": 10,
  "prev_page_url": null,
  "to": 10,
  "total": 327
}
```

### GET /fact
Retorna um fact aleatório.

**Response:**
```json
{
  "fact": "Cats sleep 16 to 18 hours per day.",
  "length": 35
}
```

## Status
✅ **API ONLINE** e funcional
