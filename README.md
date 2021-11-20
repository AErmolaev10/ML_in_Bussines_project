# python-flask-docker
Итоговый проект (пример) курса "Машинное обучение в бизнесе"

Стек:

ML: sklearn, pandas, numpy
API: flask

Задача: предсказать заинтересует ли клиента предложение банка (поле Exited). Бинарная классификация

Используемые признаки:

categorical_columns = ['Geography', 'Gender', 'Tenure', 'HasCrCard', 'IsActiveMember']
continuous_columns = ['CreditScore', 'Age', 'Balance', 'NumOfProducts', 'EstimatedSalary']

Модель: RandomForestClassifier

### Клонируем репозиторий и создаем образ
```
$ git clone https://github.com//AErmolaev10/ML_in_Bussines_project.git
$ cd ML_in_Bussines_project
$ docker build -t /AErmolaev10/ML_in_Bussines_project .
```

### Запускаем контейнер

Здесь Вам нужно создать каталог локально и сохранить туда предобученную модель (<your_local_path_to_pretrained_models> нужно заменить на полный путь к этому каталогу)
```
$ docker run -d -p 8180:8180 -p 8181:8181 -v <your_local_path_to_pretrained_models>:/app/app/models aermolaev10/ml_in_bussines_project
```

### Переходим на localhost:8181
