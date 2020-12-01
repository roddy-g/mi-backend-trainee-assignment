<a href="https://codeclimate.com/github/roddy-g/mi-backend-trainee-assignment/maintainability"><img src="https://api.codeclimate.com/v1/badges/6f2481708c58d3261406/maintainability" /></a> <a href="https://codeclimate.com/github/roddy-g/mi-backend-trainee-assignment/test_coverage"><img src="https://api.codeclimate.com/v1/badges/6f2481708c58d3261406/test_coverage" /></a>
# mi-backend-trainee-assignment
Реализован JSON API cервис для сбора информации по количеству обьявлений по определенному запросу.

Запуск: uvicorn api.main:app

/add POST

Принимает пару значений - поисковую фразу и id города, регистрирует ее в базе данных и возвращает id для этой пары значений.
Запускает фоновый процесс сбора данных с авито с интервалом один час.

| Параметр  | Тип | Описание |
| ------------- | ------------- |------------- |
| phrase  | String  |Поисковый запрос  |
| location_id  | Int  |Id региона  |

Возвращаемое значение – id поискового запроса.

| Параметр  | Тип | Описание |
| ------------- | ------------- |------------- |
| id  | Int  |Id запроса |

/stat POST

Принимает id пары значений и интервал в днях. Возращает краткую статистику за этот период.

 Параметр  | Тип | Описание |
| ------------- | ------------- |------------- |
| id  | Int  |Id запроса |
| interval  | Int  |Интервал в днях |
