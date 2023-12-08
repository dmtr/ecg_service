# ECG Service

## Instructions

To build the service, run the following command:

`docker-compose build`

To start the service, run the following command:

`docker-compose up -d`

You can access the OpenAPI documentation at http://localhost:8000/docs.

To run the tests, run the following command:

`ENVIRONMENT=TESTING docker compose -f docker-compose.yml run app pytest -vv tests`

## Design Notes
### Assumptions
We assume that approximately 8% of the population suffers from heart diseases. Therefore, for a country with a population of 40 million people, there would be around 3,200,000 potential cases. Considering an estimation of 12 ECGs per person per year, we can expect a total of 38,400,000 ECGs per year.

### Database Choice
Given the large amount of data expected, we have chosen MongoDB as the database. Both PostgreSQL and MongoDB are capable of handling this volume, but MongoDB provide easier scalability due to its built-in support for sharding.

### Message Broker
In a production system, it is recommended to use a message broker to distribute analysis calculations among workers. RabbitMQ is a reliable choice for this purpose. In this implementation, we have used FastAPI background tasks for simplicity, but this should be reconsidered in a real system.

## Future Improvements
1. The Dockerfile is not yet production-ready. It should be reviewed and updated accordingly.
2. The docker-compose file is also not yet production-ready. It should be revised and improved.
3. More tests should be added to ensure the reliability and accuracy of the service.
4. Implement linters like pylint and mypy to identify and fix any code issues or mistakes.
