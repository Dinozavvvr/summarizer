```json
{
  "original": {
    "title": "Заголовок документа",
    "value": "Первое предложение. ...",
    "sentences": [
      {
        "id": 1,
        "value": "Первое предложение",
        "words": [
          {
            "value": "Первое",
            "sentence": 1
          },
          {
            "value": "Предложение",
            "sentence": 1
          }
        ]
      }
    ]
  },
  "processed": {
    "title": "заголовок документ",
    "value": "первый предложение. ...",
    "sentences": [
      {
        "id": 2,
        "original": 1,
        "value": "первый предложение",
        "words": [
          {
            "original": "Первое",
            "value": "первый",
            "sentence": 2
          },
          {
            "original": "Предложение",
            "value": "предолжение",
            "sentence": 2
          }
        ]
      }
    ]
  }
}
```