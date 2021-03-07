# 花价

GET /flower

## request params

| key    | desc                     |
| ------ | ------------------------ |
| server | 服务器                   |
| map    | 地图，如：广陵邑         |
| type   | 种类，如：葫芦、一级玫瑰 |

## response

```json
{
    "code": 0,
    "msg": "success",
    "tag": "query-flower",
    "data": [
        {
            "branch": [
                { "number": "86", "timestamp": 1613741480 },
                { "number": "312", "timestamp": 1613737291 },
                { "number": "281", "timestamp": 1613719464 }
            ],
            "date": "2021-02-19",
            "map": "广陵邑",
            "name": "一级牵牛花(红，粉，紫)",
            "server": "蝶恋花",
            "species": "牵牛花"
        },
        {
            "branch": [
                { "number": "160", "timestamp": 1613728047 },
                { "number": "110", "timestamp": 1613706677 },
                { "number": "85", "timestamp": 1613702714 }
            ],
            "date": "2021-02-19",
            "map": "广陵邑",
            "name": "二级牵牛花(黄，蓝)",
            "server": "蝶恋花",
            "species": "牵牛花"
        },
        {
            "branch": [
                { "number": "365", "timestamp": 1613733101 },
                { "number": "274", "timestamp": 1613695915 },
                { "number": "54", "timestamp": 1613690364 }
            ],
            "date": "2021-02-19",
            "map": "广陵邑",
            "name": "一级玫瑰(红，黄，蓝，橙，粉)",
            "server": "蝶恋花",
            "species": "玫瑰"
        },
        {
            "branch": [
                { "number": "284", "timestamp": 1613744410 },
                { "number": "379", "timestamp": 1613718116 },
                { "number": "354", "timestamp": 1613715877 }
            ],
            "date": "2021-02-19",
            "map": "广陵邑",
            "name": "二级玫瑰(黑，白，紫)",
            "server": "蝶恋花",
            "species": "玫瑰"
        },
        {
            "branch": [
                { "number": "432", "timestamp": 1613738515 },
                { "number": "475", "timestamp": 1613707019 },
                { "number": "116", "timestamp": 1613700699 }
            ],
            "date": "2021-02-19",
            "map": "广陵邑",
            "name": "三级玫瑰(绿，混色)",
            "server": "蝶恋花",
            "species": "玫瑰"
        },
        {
            "branch": [
                { "number": "431", "timestamp": 1613735190 },
                { "number": "370", "timestamp": 1613733459 },
                { "number": "146", "timestamp": 1613733219 }
            ],
            "date": "2021-02-19",
            "map": "广陵邑",
            "name": "一级百合(黄，粉，白)",
            "server": "蝶恋花",
            "species": "百合"
        },
        {
            "branch": [
                { "number": "357", "timestamp": 1613703980 },
                { "number": "170", "timestamp": 1613701238 },
                { "number": "98", "timestamp": 1613698304 }
            ],
            "date": "2021-02-19",
            "map": "广陵邑",
            "name": "二级百合(橙，绿)",
            "server": "蝶恋花",
            "species": "百合"
        },
        {
            "branch": [
                { "number": "153", "timestamp": 1613723480 },
                { "number": "294", "timestamp": 1613704546 },
                { "number": "121", "timestamp": 1613698806 }
            ],
            "date": "2021-02-19",
            "map": "广陵邑",
            "name": "一级绣球花(红，白，紫)",
            "server": "蝶恋花",
            "species": "绣球花"
        },
        {
            "branch": [
                { "number": "331", "timestamp": 1613710941 },
                { "number": "267", "timestamp": 1613699520 },
                { "number": "299", "timestamp": 1613698821 }
            ],
            "date": "2021-02-19",
            "map": "广陵邑",
            "name": "二级绣球花(黄，蓝，粉)",
            "server": "蝶恋花",
            "species": "绣球花"
        },
        {
            "branch": [
                { "number": "320", "timestamp": 1613741072 },
                { "number": "460", "timestamp": 1613724797 },
                { "number": "78", "timestamp": 1613716948 }
            ],
            "date": "2021-02-19",
            "map": "广陵邑",
            "name": "一级羽扇豆花(红，白，紫)",
            "server": "蝶恋花",
            "species": "羽扇豆花"
        },
        {
            "branch": [
                { "number": "187", "timestamp": 1613706169 },
                { "number": "514", "timestamp": 1613705428 },
                { "number": "405", "timestamp": 1613701008 }
            ],
            "date": "2021-02-19",
            "map": "广陵邑",
            "name": "二级羽扇豆花(黄，蓝，粉)",
            "server": "蝶恋花",
            "species": "羽扇豆花"
        },
        {
            "branch": [
                { "number": "445", "timestamp": 1613739770 },
                { "number": "446", "timestamp": 1613728535 },
                { "number": "57", "timestamp": 1613725058 }
            ],
            "date": "2021-02-19",
            "map": "广陵邑",
            "name": "三级羽扇豆花(蓝白，黄粉)",
            "server": "蝶恋花",
            "species": "羽扇豆花"
        },
        {
            "branch": [
                { "number": "457", "timestamp": 1613743694 },
                { "number": "532", "timestamp": 1613743275 },
                { "number": "320", "timestamp": 1613741072 }
            ],
            "date": "2021-02-19",
            "map": "广陵邑",
            "name": "芜菁",
            "server": "蝶恋花",
            "species": "芜菁"
        },
        {
            "branch": [
                { "number": "493", "timestamp": 1613736176 },
                { "number": "406", "timestamp": 1613734013 },
                { "number": "433", "timestamp": 1613728816 }
            ],
            "date": "2021-02-19",
            "map": "广陵邑",
            "name": "一级荧光菌(红，黄，白)",
            "server": "蝶恋花",
            "species": "荧光菌"
        },
        {
            "branch": [
                { "number": "264", "timestamp": 1613730478 },
                { "number": "216", "timestamp": 1613723411 },
                { "number": "35", "timestamp": 1613694952 }
            ],
            "date": "2021-02-19",
            "map": "广陵邑",
            "name": "二级荧光菌(蓝，紫)",
            "server": "蝶恋花",
            "species": "荧光菌"
        },
        {
            "branch": [
                { "number": "432", "timestamp": 1613738515 },
                { "number": "155", "timestamp": 1613733511 },
                { "number": "30", "timestamp": 1613725841 }
            ],
            "date": "2021-02-19",
            "map": "广陵邑",
            "name": "葫芦",
            "server": "蝶恋花",
            "species": "葫芦"
        },
        {
            "branch": [
                { "number": "442", "timestamp": 1613731896 },
                { "number": "63", "timestamp": 1613719287 },
                { "number": "251", "timestamp": 1613715942 }
            ],
            "date": "2021-02-19",
            "map": "广陵邑",
            "name": "一级郁金香(红，黄，粉)",
            "server": "蝶恋花",
            "species": "郁金香"
        },
        {
            "branch": [
                { "number": "477", "timestamp": 1613734270 },
                { "number": "422", "timestamp": 1613717660 },
                { "number": "356", "timestamp": 1613712822 }
            ],
            "date": "2021-02-19",
            "map": "广陵邑",
            "name": "二级郁金香(白，混色)",
            "server": "蝶恋花",
            "species": "郁金香"
        },
        {
            "branch": [
                { "number": "224", "timestamp": 1613725430 },
                { "number": "362", "timestamp": 1613724650 },
                { "number": "537", "timestamp": 1613723826 }
            ],
            "date": "2021-02-19",
            "map": "广陵邑",
            "name": "青菜",
            "server": "蝶恋花",
            "species": "青菜"
        },
        {
            "branch": [
                { "number": "493", "timestamp": 1613736176 },
                { "number": "138", "timestamp": 1613734620 },
                { "number": "406", "timestamp": 1613734012 }
            ],
            "date": "2021-02-19",
            "map": "广陵邑",
            "name": "麦子",
            "server": "蝶恋花",
            "species": "麦子"
        }
    ]
}
```
