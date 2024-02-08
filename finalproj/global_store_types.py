from enum import Enum, auto
from typing import Dict, List, TypedDict

class PizzaClassType(TypedDict):
  pizza_class_quantity: str
  pizza_class_flavour: str
  pizza_class_size: str