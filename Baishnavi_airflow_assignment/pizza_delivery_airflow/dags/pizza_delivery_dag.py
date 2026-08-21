"""
Pizza Delivery Pipeline
-----------------------

This DAG simulates an automated pizza order-to-delivery workflow.

Flow:
    Receive Order
        -> Validate Order
        -> Check Order Status
        -> Prepare Pizza
        -> Bake Pizza
        -> Quality Check
        -> Dispatch Order

The order ID and status are passed between tasks using XCom.
If an order is cancelled, the ShortCircuitOperator stops the
downstream pizza preparation and delivery tasks.
"""

from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, ShortCircuitOperator



# Configuration


DAG_ID = "pizza_delivery_pipeline"

DEFAULT_ORDER_STATUS = "CANCELLED"
DEFAULT_TOPPING = "Pepperoni"

LUNCH_HOUR = 11
DINNER_HOUR = 18
RUSH_MINUTE = 30

PIZZA_PREPARATION_MINUTES = 8
PIZZA_BAKING_MINUTES = 12

def receive_order(**context):
    """
    Receive a pizza order.

    Order information can be supplied through dag_run.conf when the DAG
    is triggered through the Airflow REST API.

    Example:
        {
            "order_id": "PZ-1001",
            "order_status": "CONFIRMED",
            "topping": "Pepperoni"
        }

    The returned dictionary is automatically stored in XCom.
    """

    dag_run = context["dag_run"]
    order_details = dag_run.conf or {}

    order_id = order_details.get(
        "order_id",
        f"PZ-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
    )

    order_status = order_details.get(
        "order_status",
        DEFAULT_ORDER_STATUS,
    )

    topping = order_details.get(
        "topping",
        DEFAULT_TOPPING,
    )

    log = context["ti"].log

    log.info("New pizza order received.")
    log.info("Order ID: %s", order_id)
    log.info("Order status: %s", order_status)
    log.info("Requested topping: %s", topping)

    return {
        "order_id": order_id,
        "order_status": order_status,
        "topping": topping,
    }


def validate_order(**context):
    """
    Validate the order received from the previous task.

    The order details are retrieved from XCom.
    """

    ti = context["ti"]
    log = ti.log

    order_details = ti.xcom_pull(
        task_ids="receive_order"
    )

    if not order_details:
        log.error("No order details were received through XCom.")
        raise ValueError("Order details are missing.")

    order_id = order_details["order_id"]
    order_status = order_details["order_status"]
    topping = order_details["topping"]

    log.info("Validating order %s.", order_id)
    log.info("Order status: %s.", order_status)
    log.info("Topping requested: %s.", topping)

    if not order_id:
        log.error("Order validation failed: missing order ID.")
        raise ValueError("Order ID cannot be empty.")

    if not topping:
        log.error(
            "Order %s validation failed: no topping selected.",
            order_id,
        )
        raise ValueError("Pizza topping cannot be empty.")

    log.info("Order %s passed validation.", order_id)

    return order_details


def check_order_status(**context):
    """
    Decide whether the order should continue through the pipeline.

    Returns True for confirmed orders.
    Returns False for cancelled orders.

    ShortCircuitOperator uses this return value to determine whether
    downstream tasks should execute.
    """

    ti = context["ti"]
    log = ti.log

    order_details = ti.xcom_pull(
        task_ids="receive_order"
    )

    if not order_details:
        log.critical(
            "Order status check failed because order details are missing."
        )
        return False

    order_id = order_details["order_id"]
    order_status = order_details["order_status"].upper()

    log.info(
        "Checking status for order %s: %s.",
        order_id,
        order_status,
    )

    if order_status == "CANCELLED":
        log.warning(
            "Order %s has been cancelled. "
            "Pizza preparation and delivery will be skipped.",
            order_id,
        )
        return False

    if order_status != "CONFIRMED":
        log.warning(
            "Order %s has unsupported status '%s'. "
            "The pipeline will not continue.",
            order_id,
            order_status,
        )
        return False

    log.info(
        "Order %s is confirmed. Continuing with pizza preparation.",
        order_id,
    )

    return True


def bake_pizza(**context):
    """
    Simulate baking the pizza.
    """

    ti = context["ti"]
    log = ti.log

    order_details = ti.xcom_pull(
        task_ids="receive_order"
    )

    order_id = order_details["order_id"]

    log.info(
        "Starting oven process for order %s.",
        order_id,
    )

    log.info(
        "Pizza baking time configured for %s minutes.",
        PIZZA_BAKING_MINUTES,
    )

    log.info(
        "Pizza for order %s has finished baking.",
        order_id,
    )

    return {
        "order_id": order_id,
        "bake_status": "COMPLETED",
    }


def quality_check(**context):
    """
    Perform a basic quality check after baking.
    """

    ti = context["ti"]
    log = ti.log

    bake_result = ti.xcom_pull(
        task_ids="bake_pizza"
    )

    if not bake_result:
        log.error("No baking result received.")
        raise ValueError("Baking result is missing.")

    order_id = bake_result["order_id"]
    bake_status = bake_result["bake_status"]

    log.info(
        "Running quality check for order %s.",
        order_id,
    )

    if bake_status != "COMPLETED":
        log.error(
            "Quality check failed for order %s.",
            order_id,
        )
        raise ValueError("Pizza was not baked successfully.")

    log.info(
        "Quality check passed for order %s.",
        order_id,
    )



# DAG definition
with DAG(
    dag_id=DAG_ID,
    start_date=datetime(2026, 8, 1),
    schedule=f"{RUSH_MINUTE} {LUNCH_HOUR},{DINNER_HOUR} * * *",
    catchup=False,
    tags=["pizza", "delivery", "assignment"],
    description="Automated pizza order-to-delivery pipeline",
) as dag:

    receive_order_task = PythonOperator(
        task_id="receive_order",
        python_callable=receive_order,
    )

    validate_order_task = PythonOperator(
        task_id="validate_order",
        python_callable=validate_order,
    )

    check_order_status_task = ShortCircuitOperator(
        task_id="check_order_status",
        python_callable=check_order_status,
    )

    prepare_pizza_task = BashOperator(
        task_id="prepare_pizza",
        bash_command=(
            "echo 'Preparing pizza for order "
            "{{ ti.xcom_pull(task_ids='receive_order')['order_id'] }}' "
            "&& echo 'Preparation time: 8 minutes' "
            "&& echo 'Pizza preparation completed.'"
        ),
    )

    bake_pizza_task = PythonOperator(
        task_id="bake_pizza",
        python_callable=bake_pizza,
    )

    quality_check_task = PythonOperator(
        task_id="quality_check",
        python_callable=quality_check,
    )

    dispatch_order_task = BashOperator(
        task_id="dispatch_order",
        bash_command=(
            "echo 'Preparing delivery dispatch for order "
            "{{ ti.xcom_pull(task_ids='receive_order')['order_id'] }}' "
            "&& echo 'Delivery partner assigned.' "
            "&& echo 'Order dispatched successfully.'"
        ),
    )

    (
        receive_order_task
        >> validate_order_task
        >> check_order_status_task
        >> prepare_pizza_task
        >> bake_pizza_task
        >> quality_check_task
        >> dispatch_order_task
    )