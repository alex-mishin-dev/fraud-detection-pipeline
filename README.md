# Real-Time Fraud Detection Pipeline

This project implements a complete, end-to-end streaming data pipeline for detecting fraudulent transactions in real-time. It serves as a comprehensive demonstration of modern data engineering principles, from data ingestion and processing to orchestration and visualization.

The entire system is containerized using Docker and automated with Ansible, allowing for a one-command deployment of the entire infrastructure.

## Architecture & Data Flow

The pipeline follows a modern, event-driven architecture. The flow of data is as follows:

1.  **Data Generation**: A Python script (`src/data_generator.py`) continuously produces simulated transaction data and streams it into an Apache Kafka topic named `transactions`.
2.  **Stream Processing**: An Apache Spark streaming job (`src/spark_consumer.py`) subscribes to the Kafka topic. It reads transactions in micro-batches, filters them to identify potentially fraudulent activities (where `is_fraud == 1`), and writes the results directly to a PostgreSQL database.
3.  **Orchestration**: An Apache Airflow DAG (`dags/03_run_spark_job_dag.py`) is responsible for orchestrating the Spark job. It can be triggered manually or set to run on a schedule, ensuring the processing job is always running and reliable.
4.  **Data Storage**: A PostgreSQL database (`fraud_db`) serves two purposes: it stores the metadata for the Airflow instance and, more importantly, it houses the `fraudulent_transactions` table where the results of our analysis are persisted.
5.  **Visualization & BI**: Metabase, a business intelligence tool, connects directly to the PostgreSQL database, allowing for the creation of real-time dashboards and visualizations to monitor fraudulent activity as it is detected.

## Tech Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Orchestration** | **Apache Airflow** | Manages, schedules, and monitors the Spark data processing job. |
| **Stream Processing** | **Apache Spark** | Consumes data from Kafka, performs transformations, and filters for fraud. |
| **Message Broker** | **Apache Kafka** | Ingests and buffers the high-throughput stream of transaction data. |
| **Database** | **PostgreSQL** | Stores the final, processed fraudulent transaction data. |
| **BI / Visualization** | **Metabase** | Provides a web-based UI for building dashboards on top of the results. |
| **Containerization** | **Docker & Docker Compose** | Encapsulates every service into a reproducible, isolated container. |
| **Deployment** | **Ansible** | Automates the entire infrastructure setup with a single command. |

## Quick Start & Project Management

This project is fully automated. The primary method for managing the environment is through the `Makefile`, which provides a set of convenient commands.

### One-Command Deployment

To deploy the entire infrastructure from scratch, including building custom Docker images, starting all services, and initializing the Kafka topic, run:

```bash
make deploy
```

This command uses the Ansible playbook (`playbook.yml`) to perform all necessary setup steps automatically.

### Other Useful Commands

The `Makefile` also provides granular control over the environment for development and debugging purposes.

| Command | Description |
| :--- | :--- |
| `make up` | Starts all services in the background without rebuilding images. |
| `make down` | Stops all running services. |
| `make clean` | Stops and removes all containers, networks, and data volumes. |
| `make run-producer` | Starts the Python data generator to send transactions to Kafka. |
| `make db-shell` | Opens an interactive `psql` shell to the PostgreSQL database. |
| `make open-bi` | Opens the Metabase web interface in your default browser. |
| `make logs service=` | Shows the logs for a specific service (e.g., `make logs service=spark-master`). |

## How to Run the Pipeline

1.  **Deploy the Infrastructure:**
    ```bash
    make deploy
    ```
2.  **Start the Data Producer:** Open a new terminal and run:
    ```bash
    make run-producer
    ```
3.  **Trigger the Spark Job via Airflow:**
    *   Open the Airflow UI at `http://localhost:8088`.
    *   Log in with `admin` / `admin`.
    *   Enable and trigger the `03_run_spark_job_dag`.
4.  **Visualize the Results:**
    *   Open Metabase using `make open-bi` (`http://localhost:3000`).
    *   Connect Metabase to the `fraud_db` PostgreSQL database (Host: `fraud_db`, DB: `airflow`, User: `airflow`, Pass: `airflow`).
    *   Create questions and dashboards based on the `fraudulent_transactions` table.
