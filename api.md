# 小白藏经阅读后端服务API

### 今日藏经阅读列表

- Request: /zangjing/today_list

- Response
```json
{ "date": "20180429 04:30:00",
  "list" : [ { "title" : "妙法莲华经卷1",
               "section" : 1,
               "section_id" : 123456
               
            },
            
            { "title" : "妙法莲华经卷1",
               "section" : 2,
               "section_id" : 123457
            }
        ]
}
```

### 获取藏经小段文章

- Request: /zangjing/section/<section_id>

- Response:
```json
{ "title" : "妙法莲华经卷1",
   "section" : 2,
   "section_id" : 123457,
   "classic " : "base64 encode",
   "morden" : "base64 encode "
}
```

