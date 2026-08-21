# Pizza Delivery Pipeline — Apache Airflow Assignment

## Overview

This project implements an automated pizza order-to-delivery workflow using Apache Airflow.

The pipeline models the flow of a pizza order from the time it is received until it is dispatched for delivery. The workflow is designed to run without manual intervention and includes order validation, status-based control flow, pizza preparation, baking, quality checking, and delivery dispatch.

The project is implemented using Apache Airflow 2.9.3 running through Docker, with PostgreSQL used as the Airflow metadata database.

The DAG is designed with seven tasks and demonstrates:

- PythonOperator
- BashOperator
- ShortCircuitOperator
- XCom-based communication between tasks
- Conditional task skipping
- Airflow task logging
- Cron-based scheduling
- REST API-based DAG triggering
- Runtime configuration through API request data

---

## Project Structure

```
Airflow_assignment/
│
├── Dag/
│   └── pizza_delivery_dag.py
│
├── screenshots/
│   ├── requestapi.png
│   ├── requestapi (2).png
│   ├── responseapi.png
│   ├── responseapi (2).png
│   ├── successfulgraph.png
│   ├── Skippedgraph.png
│   └── xcom.png
│
├── docker-compose.yaml
└── README.md
```

### Main Components

**pizza_delivery_dag.py**

Contains the complete Airflow DAG, task definitions, task functions, XCom handling, logging, scheduling, and task dependencies.

**docker-compose.yaml**

Defines the Docker-based Airflow environment used to run the assignment.

**screenshots/**

Contains evidence of the completed DAG runs, XCom usage, Graph View, and REST API request/response.

---

## 1. Pipeline Architecture

The pipeline consists of seven tasks:

```
                  Receive Order
                       │
                       ▼
                 Validate Order
                       │
                       ▼
                Check Order Status
                       │
                ┌──────┴──────┐
                │             │
            CONFIRMED      CANCELLED
                │             │
                ▼             X
          Prepare Pizza      SKIP
                │
                ▼
            Bake Pizza
                │
                ▼
           Quality Check
                │
                ▼
          Dispatch Order
```

The seven tasks are:

| Task | Operator | Responsibility |
|---|---|---|
| receive_order | PythonOperator | Receives order information and creates/passes order details |
| validate_order | PythonOperator | Validates the received order |
| check_order_status | ShortCircuitOperator | Determines whether the order should continue |
| prepare_pizza | BashOperator | Simulates pizza preparation |
| bake_pizza | PythonOperator | Simulates the baking process |
| quality_check | PythonOperator | Verifies the baking result |
| dispatch_order | BashOperator | Simulates delivery dispatch |

The assignment requires between six and eight tasks, so the final implementation uses seven tasks. It also requires both a PythonOperator and a BashOperator, which are included in the workflow.

---

## 2. Task Flow

### 2.1 Receive Order

The pipeline begins with `receive_order`.

This task uses a PythonOperator.

It receives order information from the DAG run configuration and creates the order details.

The order contains:

- Order ID
- Order status
- Requested topping

Example:

```json
{
  "order_id": "PZ-1001",
  "order_status": "CONFIRMED",
  "topping": "Pepperoni"
}
```

If values are not provided through the DAG run configuration, default values are used to allow the pipeline to run normally.

The task also writes meaningful information to the Airflow task log.

### 2.2 Validate Order

The `validate_order` task uses a PythonOperator.

It retrieves the order details produced by `receive_order` through XCom and validates:

- Whether order information exists
- Whether an order ID is available
- Whether a topping has been selected

If the required information is missing, the task raises an error and the order does not proceed.

If validation succeeds, the workflow continues to the order-status decision.

### 2.3 Check Order Status

The `check_order_status` task is the decision point of the pipeline.

It uses a ShortCircuitOperator.

The task checks the order status retrieved from XCom.

**Confirmed order**

If:

```
order_status = CONFIRMED
```

the task returns `True`.

The downstream pizza-processing tasks are allowed to execute.

**Cancelled order**

If:

```
order_status = CANCELLED
```

the task returns `False`.

The downstream tasks are deliberately skipped.

The pipeline therefore behaves as:

```
receive_order       SUCCESS
validate_order      SUCCESS
check_order_status  SUCCESS
prepare_pizza       SKIPPED
bake_pizza          SKIPPED
quality_check       SKIPPED
dispatch_order      SKIPPED
```

This provides a realistic cancellation scenario and demonstrates Airflow's conditional execution capabilities.

The assignment specifically requires at least one task to be deliberately skipped under a defined condition and allows ShortCircuitOperator as one of the mechanisms for achieving this.

---

## 3. XCom Usage

XCom is used to transfer order information between tasks.

The `receive_order` task returns an order details dictionary containing:

- `order_id`
- `order_status`
- `topping`

The returned value is stored by Airflow as an XCom value.

The downstream `validate_order` and `check_order_status` tasks retrieve this information using the task instance:

```python
ti.xcom_pull(task_ids="receive_order")
```

The resulting flow is:

```
receive_order
      │
      │ order details
      ▼
     XCom
      │
      ▼
validate_order
      │
      ▼
check_order_status
```

XCom was chosen because order information is genuinely required by downstream tasks. The order ID provides a consistent identifier throughout the workflow, while the order status is required to determine whether processing should continue.

This satisfies the assignment requirement to pass meaningful data between tasks using XCom.

---

## 4. Scheduling

The DAG uses the following cron schedule:

```
30 11,18 * * *
```

This schedules the pipeline for:

- **11:30 AM** — Lunch rush
- **6:30 PM** — Dinner rush

The schedule was chosen to represent the two major daily periods when pizza orders are expected to increase.

Instead of using a generic `@daily` schedule, the cron expression reflects the actual business scenario described by the assignment.

The DAG also uses:

```python
catchup=False
```

This prevents Airflow from creating historical DAG runs for previous scheduled intervals when the DAG is first enabled.

The assignment specifically asks for a schedule that reflects pizza-shop activity rather than a generic daily schedule.

---

## 5. Logging

Each Python-based task uses Airflow's task logger rather than bare `print()` statements.

Examples of information recorded in the logs include:

```
New pizza order received.
Order ID: PZ-1001.
Order status: CONFIRMED.
Requested topping: Pepperoni.
```

For a cancelled order, the log explains the reason for the skipped downstream processing:

```
Order PZ-1002 has been cancelled.
Pizza preparation and delivery will be skipped.
```

Different log levels are used according to the situation, including informational, warning, error, and critical messages where appropriate.

BashOperator output is also captured by Airflow and is available through the corresponding task logs.

This makes the task logs useful for understanding what happened during a DAG run without having to inspect the source code.

The assignment specifically requires meaningful Airflow logging and asks that skipped processing be explained in the logs.

---

## 6. Docker-Based Airflow Environment

Airflow is not installed directly on the host machine.

The project uses Docker to run the Airflow environment.

The environment consists of:

```
Docker
   │
   ├── Airflow Webserver
   │
   ├── Airflow Scheduler
   │
   └── PostgreSQL
```

The Airflow image used for the assignment is:

```
apache/airflow:2.9.3
```

The DAG directory is mounted into the Airflow container so that the scheduler can detect:

```
/opt/airflow/dags/pizza_delivery_dag.py
```

The Airflow webserver is exposed locally through:

```
http://localhost:8085
```

This setup keeps the assignment environment isolated from the host Python installation.

---

## 7. REST API Trigger

The assignment requires the DAG to be triggered through the Airflow REST API instead of using the Airflow UI's "Trigger DAG" button.

The Airflow Swagger UI was used to interact with the REST API.

The DAG is triggered using:

```
POST /api/v1/dags/pizza_delivery_pipeline/dagRuns
```

The request uses the DAG ID:

```
pizza_delivery_pipeline
```

Runtime order information can be passed through the `conf` object.

Example request:

```json
{
  "dag_run_id": "pizza_api_confirmed_001",
  "conf": {
    "order_id": "PZ-1001",
    "order_status": "CONFIRMED",
    "topping": "Pepperoni"
  }
}
```

The DAG reads this configuration through:

```python
dag_run = context["dag_run"]
order_details = dag_run.conf or {}
```

This allows the same DAG to receive different order information for different runs.

---

## 8. API Trigger and Response

The Swagger API interface was used to send the DAG-run request.

The request contains:

- **DAG ID:** `pizza_delivery_pipeline`
- The request body containing the runtime order configuration

The API response provides information about the created DAG run, including the run identifier and current state.

The screenshots in the `screenshots` directory provide evidence of:

- API trigger request
- API request body
- API response
- DAG run information

The API screenshots are included as part of the assignment evidence.

The assignment specifically requires a screenshot of the API request and response showing the run identifier and state.

---

## 9. Successful Pipeline Run

For a confirmed order, the expected execution path is:

```
receive_order
      ↓
validate_order
      ↓
check_order_status
      ↓
prepare_pizza
      ↓
bake_pizza
      ↓
quality_check
      ↓
dispatch_order
```

All seven tasks complete successfully.

The completed Graph View is available in:

```
screenshots/successfulgraph.png
```

This provides visual evidence of the normal execution path.

---

## 10. Cancelled Order / Skipped Pipeline

The pipeline also supports a cancelled-order scenario.

Example API configuration:

```json
{
  "order_id": "PZ-1002",
  "order_status": "CANCELLED",
  "topping": "Pepperoni"
}
```

The workflow reaches `check_order_status`, which identifies the cancelled order.

The ShortCircuitOperator returns `False`, causing downstream tasks to be skipped.

The resulting state is:

```
receive_order       SUCCESS
validate_order      SUCCESS
check_order_status  SUCCESS
prepare_pizza       SKIPPED
bake_pizza          SKIPPED
quality_check       SKIPPED
dispatch_order      SKIPPED
```

The corresponding Graph View evidence is available in:

```
screenshots/Skippedgraph.png
```

This demonstrates the conditional behavior required by the assignment.

---

## 11. Verification Performed

The DAG was verified using Airflow's CLI from the Docker environment.

The DAG was checked for successful discovery by the scheduler.

The available task IDs were verified as:

```
receive_order
validate_order
check_order_status
prepare_pizza
bake_pizza
quality_check
dispatch_order
```

The DAG dependency structure was also checked to ensure that tasks execute in the intended order.

The project was additionally tested through the Airflow API and the resulting DAG runs were inspected through Airflow.

---

## 12. Assignment Requirement Mapping

| Assignment Requirement | Implementation |
|---|---|
| 6–8 tasks | 7 tasks |
| PythonOperator | receive_order, validate_order, bake_pizza, quality_check |
| BashOperator | prepare_pizza, dispatch_order |
| XCom | Order details passed from receive_order to downstream tasks |
| Deliberate skip | ShortCircuitOperator with cancelled-order condition |
| Pizza-specific schedule | `30 11,18 * * *` |
| Airflow logging | Task logger used throughout Python tasks |
| Clean task IDs | Meaningful snake_case task IDs |
| REST API trigger | Swagger UI using DAGRun POST endpoint |
| Successful Graph View | Included in screenshots |
| Skipped Graph View | Included in screenshots |
| API request/response evidence | Included in screenshots |
| README | This document |

The implementation follows the assignment's stated requirements and deliverables.

---

## 13. Key Airflow Concepts Demonstrated

This assignment demonstrates the following Airflow concepts:

### DAG

Defines the complete pizza delivery workflow and its schedule.

### Operators

Different operators are used according to the type of work being performed:

- PythonOperator
- BashOperator
- ShortCircuitOperator

### Dependencies

The `>>` operator defines the order in which tasks execute.

```python
receive_order_task \
    >> validate_order_task \
    >> check_order_status_task \
    >> prepare_pizza_task \
    >> bake_pizza_task \
    >> quality_check_task \
    >> dispatch_order_task
```

### XCom

Used for transferring small pieces of order information between tasks.

### Short Circuiting

Used to stop downstream execution when an order is cancelled.

### Scheduling

Cron is used to represent the lunch and dinner rush.

### Logging

Airflow task logs provide execution details and explain conditional behavior.

### REST API

The API provides a programmatic way of creating DAG runs and passing runtime configuration.

---

## 14. Final Workflow

The final system can be summarized as:

```
                    ┌───────────────────────┐
                    │   Airflow Scheduler   │
                    │                       │
                    │ 11:30 AM / 6:30 PM    │
                    └───────────┬───────────┘
                                │
                                ▼
                      Pizza Delivery DAG
                                │
                                ▼
                         Receive Order
                                │
                               XCom
                                │
                                ▼
                        Validate Order
                                │
                                ▼
                       Check Order Status
                         /             \
                        /               \
                CONFIRMED            CANCELLED
                    │                    │
                    ▼                    X
              Prepare Pizza           SKIP
                    │
                    ▼
                Bake Pizza
                    │
                    ▼
              Quality Check
                    │
                    ▼
              Dispatch Order
                    │
                    ▼
                 CUSTOMER

External Trigger:
Swagger / REST API
        │
        │ POST /dagRuns
        ▼
Airflow API
        │
        ▼
Pizza Delivery DAG
```

---

## 15. Conclusion

The Pizza Delivery Pipeline demonstrates how Apache Airflow can be used to orchestrate a multi-stage data/workflow process with dependencies, inter-task communication, conditional execution, scheduling, logging, and API-based execution.

The workflow is intentionally designed around the pizza-delivery scenario rather than simply reproducing a list of example stages. The cancellation path provides a realistic reason for skipping downstream work, while XCom allows order information to move between tasks.

The project also demonstrates the difference between an automatically scheduled workflow and a workflow that can be started programmatically through the Airflow REST API.

All required implementation and execution evidence is maintained in the project screenshots directory.