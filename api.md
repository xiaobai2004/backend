# 小白藏经阅读后端服务API

### 今日藏经阅读列表，经文编号

- Request: https://gwfy3.applinzi.com/wenbai/today_list

- Response
```json
[
		{"id": 9, "display": "\u56db\u5341\u4e8c\u7ae0\u7ecf"}, 
		{"id": 10, "display": "\u5706\u89c9\u7ecf"},
	    {"id": 8, "display": "\u91d1\u521a\u7ecf"}
 ]
```

### 获取指定经文小节编号

- Request: https://gwfy3.applinzi.com/wenbai/scripture/10/section_id_list

- Response:
```json
{
		"section_id_list": [79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91],
		 "scripture_id": 10, 
		 "scripture_display": "\u5706\u89c9\u7ecf"
 }
```

### 获取指定段的经文

- Request https://gwfy3.applinzi.com/wenbai/scripture/10/section/79/sentences

-Response:

```json
{
	"scripture_id": 10, 
	"section_id": 79, 
	"scripture_display": "\u5706\u89c9\u7ecf"
	"sentences": [
				{"sentence_id": 658, 
				"modern": "\u6211\u542c\u4f5b\u8fd9\u6837\u8bf4\u7684\u3002", 
				"annotation": "\u3010\u5982\u662f\u6211\u95fb\u3011\uff1a\u5373", 
				"classic": "\u5982\u662f\u6211\u95fb\u3002"}，
				
				{"sentence_id": 659, 
				"modern": "\u6211\u542c\u4f5b\u8fd9\u6837\u8bf4\u7684\u3002", 
				"annotation": "\u3010\u5982\u662f\u6211\u95fb\u3011\uff1a\u5373", 
				"classic": "\u5982\u662f\u6211\u95fb\u3002"}
			], 
}
```



