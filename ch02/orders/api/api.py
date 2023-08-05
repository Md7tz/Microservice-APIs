import uuid
from datetime import datetime
from http import HTTPStatus
from uuid import UUID

from fastapi import HTTPException
from starlette.responses import Response
from starlette import status

from orders.app import app
from orders.api.schemas import CreateOrderSchema, GetOrderSchema, GetOrdersSchema

orders = []


@app.get("/orders", response_model=GetOrdersSchema)
def get_orders():
    return orders


@app.post("/orders", response_model=GetOrderSchema, status_code=status.HTTP_201_CREATED)
def create_order(order_details: CreateOrderSchema):
    order = order_details.dict()
    order["id"] = uuid.uuid4()
    order["created"] = datetime.utcnow()
    order["status"] = "created"
    orders.append(order)
    return order


@app.get("/orders/{order_id}", response_model=GetOrderSchema)
def get_orders(order_id: UUID):
    for order in orders:
        if order[id] == order_id:
            return order
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Order with ID {order_id} not found",
    )


@app.put("/orders/{order_id}", response_model=GetOrderSchema)
def update_order(order_id: UUID, order_details: CreateOrderSchema):
    for order in orders:
        if order[id] == order_id:
            order.update(order_details.dict())
            return order
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Order with ID {order_id} not found",
    )


@app.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: UUID):
    for index, order in enumerate(orders):
        if order[id] == order_id:
            orders.pop(index)
            return Response(status_code=HTTPStatus.NO_CONTENT.value)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Order with ID {order_id} not found",
    )


@app.post("/orders/{order_id}/cancel", response_model=GetOrderSchema)
def cancel_order(order_id: UUID):
    for order in orders:
        if order[id] == order_id:
            order["status"] = "cancelled"
            return order
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Order with ID {order_id} not found",
    )


@app.post("/orders/{order_id}/pay", response_model=GetOrderSchema)
def pay_order(order_id: UUID):
    for order in orders:
        if order[id] == order_id:
            order["status"] = "progress"
            return order
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Order with ID {order_id} not found",
    )
