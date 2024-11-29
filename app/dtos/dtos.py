from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class SummaryDTO:
    order_item:str
    quantity:int
    bill_amount:float

    def __str__(self):
        return f"Order Item: {self.order_item} Quantity: {self.quantity} Bill Amount: ₹{self.bill_amount}"

@dataclass
class PreviousOrderDTO:
    summary_dtos:List[SummaryDTO]
    ordered_at:datetime
    grand_total:float
    
    def __str__(self):
        # Create a string for each order item in the summary
        order_details = ", ".join([f"{item.order_item} (Quantity: {item.quantity}) (Total: {item.bill_amount})" for item in self.summary_dtos])
        return f"{order_details}\n placed on {self.ordered_at.strftime('%Y-%m-%d %H:%M')}\n Grand Total: ₹{self.grand_total} "

    