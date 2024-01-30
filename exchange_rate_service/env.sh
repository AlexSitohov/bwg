export APP_HOST="0.0.0.0"
export APP_PORT=8000
export POSTGRES_DB_LOGIN='postgres'
export POSTGRES_DB_PASSWORD='postgres_password'
export POSTGRES_DB_HOST='exchange_rates_db'
export POSTGRES_DB_PORT=5432
export POSTGRES_DB_NAME='exchange_rate'
export SQLALCHEMY_ECHO=0
export SQLALCHEMY_POOL_SIZE=20

export KAFKA_BROKERS='kafka:29092'
export KAFKA_CONSUMER_TOPIC='exchange_rate'
export KAFKA_TOPIC='exchange_rate'
export KAFKA_PRODUCER_TOPIC='exchange_rate_failed'
export KAFKA_CONSUMER_GROUP_ID='exchange_rate_consumer_group'
export KAFKA_SASL_MECHANISM='PLAIN'
export KAFKA_SECURITY_PROTOCOL='SASL_PLAINTEXT'
export KAFKA_SASL_PLAIN_USERNAME='user'
export KAFKA_SASL_PLAIN_PASSWORD='password'

export PYTHONPATH=$PWD:$PWD/src:$PWD/src/app
export LOGGING_LEVEL=20

echo "Переменные окружения установлены"
