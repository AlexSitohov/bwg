Мне удалось успешно настроить обмен курсами через WebSocket, сохранение данных в PostgreSQL через Kafka и вывод через 
exchange_rate_service. К сожалению, несмотря на все усилия, я не смог достичь целевого показателя 
RPS, получив чуть менее 500 RPS. Хотя использование небольшого кластера Kubernetes было бы идеальным решением, но для его 
реализации потребовалось бы уже слишком много времени.

Документация API:
Документация моего API доступна по ссылке http://localhost:8000/exchange_rate/api/docs.

Команды для запуска:
Вы можете использовать следующие команды для запуска моего сервиса:


Команды для запуска:
cd exchange_rate_service/ && source env.sh && docker-compose -f docker/docker-compose.yml up -d && cd src/app && alembic upgrade head

По всем вопросам - https://t.me/extendo_merc