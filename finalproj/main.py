from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from my_types import WebhookRequestType, WebhookResponseType, PlatformEnum

from db_conn import db_conn
import json
import uuid

app = Flask(__name__)
app.config["BASIC_AUTH_USERNAME"] = "username"
app.config["BASIC_AUTH_PASSWORD"] = "password"


basic_auth = BasicAuth(app)

# Global variables
current_store = {
  "pizza_class": [],
  "pizza_size": [],
  "pizza_flavour": [],
  "pizza_quantity": [],
  "pizza_size_and_flavour": [],
  "pizza_size_and_quantity": [],
  "pizza_flavour_and_quantity": [],
  "address": "",
  "phone_number": ""
}

previous_orders = []

expecting_size = False
expecting_flavour = False
expecting_quantity = False
expecting_size_and_flavour = False
expecting_size_and_quantity = False
expecting_flavour_and_quantity = False

is_params_empty = True

@app.route('/')
def index():
    # print(db_conn)
    return 'hello from backend'

@app.route('/dialogflowFulfillment', methods=["GET", "POST"])
@basic_auth.required
def dialogFlowFirebaseFulfillment():
  db_cursor  = db_conn.cursor()
  # This is Webhook Request that is sent to the Replit backend when Dialogflow 
  # identifies an Intent that has Fulfillment enabled.
  webhookRequest: WebhookRequestType = request.get_json()


  # Extract properties from webhook request
  intentName = webhookRequest["queryResult"]["intent"]["displayName"]
  parameters = webhookRequest["queryResult"]["parameters"]
  session = webhookRequest["session"]
  contexts = webhookRequest["queryResult"]["outputContexts"]
  output_context = {
    'name': f'{session}/contexts/pizza-order-specifics',
    'lifespanCount': 10,
    'parameters': current_store
  }

  
  # Know what to do for each intent
  if intentName == "Default Welcome Intent":
    response = {"fulfillmentText": "Hello. Welcome to Pizza Oven. How can I help you?"}
    return jsonify(response)
  elif intentName == "Pizza Order Specifics":

    # TO answer generic questions
    # Check if all lists are empty

    global is_params_empty
    
    for value in parameters.values():
        if isinstance(value, list) and value:
            is_params_empty = False
            break

    for value in parameters.values():
        if isinstance(value, str) and value.strip():
            is_params_empty = False
            break
          
    print(parameters)
    
    
    if is_params_empty:
      response = {"fulfillmentText": f"Sure. Specify your pizza sizes, flavours and quantities. Also specify your address and phone number."}
      return jsonify(response)

    
    pizza_size_and_quantity = parameters["pizza-size-and-quantity"]
    pizza_size_and_flavour = parameters["pizza-size-and-flavour"]
    pizza_flavour_and_quantity = parameters["pizza-flavour-and-quantity"]
    
    global expecting_flavour
    global expecting_size
    global expecting_quantity
    global expecting_size_and_flavour
    global expecting_size_and_quantity
    global expecting_flavour_and_quantity 

    # add the proper values to the current_store even before processing
    pizza_classes = parameters.get('pizza-class', [])

    for pizza_class in pizza_classes:
      current_store["pizza_class"].append(pizza_class)

    # Adding erronous input to global store for context
    # The nooleanis to prevent corrections from being taken in as errors
      # one parameter missing
    if pizza_size_and_quantity and not expecting_size_and_quantity:
      for item in pizza_size_and_quantity:
        current_store["pizza_size_and_quantity"].append(item)


    if pizza_flavour_and_quantity and not expecting_flavour_and_quantity:
      for item in pizza_flavour_and_quantity:
        current_store["pizza_flavour_and_quantity"].append(item)


    if pizza_size_and_flavour and not expecting_size_and_flavour:
      for item in pizza_size_and_flavour:
        current_store["pizza_size_and_flavour"].append(item)

      # two parameters missing
    if parameters["pizza-quantity"] and not expecting_quantity:
      for item in parameters["pizza-quantity"]:
        current_store["pizza_quantity"].append(item)

    if parameters["pizza-size"] and not expecting_size:
      for item in parameters["pizza-size"]:
        current_store["pizza_size"].append(item)

    if parameters["pizza-flavour"] and not expecting_flavour:
      for item in parameters["pizza-flavour"]:
        current_store["pizza_flavour"].append(item)

    print("Before Correction:",expecting_flavour, expecting_size, expecting_quantity, expecting_size_and_flavour, expecting_size_and_quantity, expecting_flavour_and_quantity)
    # Correcting the errors
      # correcting two missing parameters
    if expecting_size_and_flavour:
      current_item = current_store["pizza_quantity"].pop()

      corrected_order = {
        "pizza-class-quantity": current_item,
        "pizza-class-flavour": parameters["pizza-size-and-flavour"][0]["pizza-flavour"],
        "pizza-class-size": parameters["pizza-size-and-flavour"][0]["pizza-size"]
      }

      current_store["pizza_class"].append(corrected_order)

      expecting_size_and_flavour = False


    if expecting_size_and_quantity:
      current_item = current_store["pizza_flavour"].pop()
      
      corrected_order = {
        "pizza-class-quantity": parameters["pizza-size-and-quantity"][0]["pizza-quantity"],
        "pizza-class-flavour": current_item,
        "pizza-class-size": parameters["pizza-size-and-quantity"][0]["pizza-size"]
      }

      current_store["pizza_class"].append(corrected_order)

      expecting_size_and_quantity = False


    if expecting_flavour_and_quantity:
      current_item = current_store["pizza_size"].pop()

      corrected_order = {
        "pizza-class-quantity": parameters["pizza-flavour-and-quantity"][0]["pizza-quantity"],
        "pizza-class-flavour": parameters["pizza-flavour-and-quantity"][0]["pizza-flavour"],
        "pizza-class-size": current_item
      }

      current_store["pizza_class"].append(corrected_order)

      expecting_flavour_and_quantity = False


      # correcting one missing parameter
    if expecting_flavour:
      current_item = current_store["pizza_size_and_quantity"].pop()

      corrected_order = {
        "pizza-class-quantity": current_item["pizza-quantity"],
        "pizza-class-size": current_item["pizza-size"],
        "pizza-class-flavour": parameters["pizza-flavour"][0]
      }

      current_store["pizza_class"].append(corrected_order)

      expecting_flavour = False


    if expecting_size:
      current_item = current_store["pizza_flavour_and_quantity"].pop()

      corrected_order = {
        "pizza-class-quantity": current_item["pizza-quantity"],
        "pizza-class-size": parameters["pizza-size"][0],
        "pizza-class-flavour": current_item["pizza-flavour"]
      }

      current_store["pizza_class"].append(corrected_order)

      expecting_size = False


    if expecting_quantity:
      current_item = current_store["pizza_size_and_flavour"].pop()

      corrected_order = {
        "pizza-class-quantity": parameters["pizza-quantity"][0],
        "pizza-class-size": current_item["pizza-size"],
        "pizza-class-flavour": current_item["pizza-flavour"]
      }

      current_store["pizza_class"].append(corrected_order)

      expecting_quantity = False


    print("After Correction:",expecting_flavour, expecting_size, expecting_quantity, expecting_size_and_flavour, expecting_size_and_quantity, expecting_flavour_and_quantity)


        
    # Sending back corrections to agent using global store as a reference

      # two parameters missing
    if current_store["pizza_quantity"]:
      pizza_quantity = current_store["pizza_quantity"][-1]

      expecting_size_and_flavour = True

      response = {"fulfillmentText": f"May you specify the size and flavour of the {pizza_quantity} pizza(s)?"}
      return jsonify(response)


    if current_store["pizza_flavour"]:
      pizza_flavour = current_store["pizza_flavour"][-1]

      expecting_size_and_quantity = True

      response = {"fulfillmentText": f"May you specify the size and quantity of the {pizza_flavour} pizza(s)?"}
      return jsonify(response)


    if current_store["pizza_size"]:
      pizza_size = current_store["pizza_size"][-1]

      expecting_flavour_and_quantity = True

      response = {"fulfillmentText": f"May you specify the flavour and quantity of the {pizza_size} pizza(s)?"}
      return jsonify(response)
        
      # one parameter missing
    if current_store["pizza_size_and_quantity"]:
      pizza_size_and_quantity = current_store["pizza_size_and_quantity"][-1]

      expecting_flavour = True
      
      response = {"fulfillmentText": f"May you specify the flavour of {pizza_size_and_quantity['pizza-quantity']} {pizza_size_and_quantity['pizza-size']} pizza(s)?"}
      return jsonify(response)


    if current_store["pizza_flavour_and_quantity"]:
      pizza_flavour_and_quantity = current_store["pizza_flavour_and_quantity"][-1]

      expecting_size = True

      response = {"fulfillmentText": f"May you specify the size of {pizza_flavour_and_quantity['pizza-quantity']} {pizza_flavour_and_quantity['pizza-flavour']} pizza(s)?"}
      return jsonify(response)


    if current_store["pizza_size_and_flavour"]:
      pizza_size_and_flavour = current_store["pizza_size_and_flavour"][-1]

      expecting_quantity = True

      response = {"fulfillmentText": f"May you specify the quantity of {pizza_size_and_flavour['pizza-size']} {pizza_size_and_flavour['pizza-flavour']} pizza(s)?"}
      return jsonify(response)



  
    # From this point we should be dealing either pizzas that have complete details
    # take recent parameters and add to global store
    
    phone_number = parameters.get('phone-number')
    address = parameters.get('address')

    if phone_number:
      current_store["phone_number"] = phone_number

    if address:
      current_store["address"] = address

    print(current_store)
    
    # the first process is to take parameters from the pizza
    order_summary = []
    # missing_pizzas_parameters = []
    missing_other_parameters = []
    
    pizza_number = 0

    pizza_price_total = 0  
    
    # Check pizza details
    for pizza_class in current_store["pizza_class"]:
      pizza_number = pizza_number + 1
      # Extract parameters
      flavour = pizza_class.get('pizza-class-flavour')
      size = pizza_class.get('pizza-class-size')
      quantity = pizza_class.get('pizza-class-quantity')

      # Get Pizza Table
      sql = "SELECT * FROM pizzas WHERE PizzaName = %s"
      adr = (flavour,)
      db_cursor.execute(sql, adr)
      pizzas_table = db_cursor.fetchall()

      # Get Pizza Price
      pizza_price = 0
      if size == "small":
        pizza_price = pizzas_table[0][3]
      elif size == "medium":
        pizza_price = pizzas_table[0][4]
      elif size == "large":
        pizza_price = pizzas_table[0][5]
      elif size == "super large":
        pizza_price = pizzas_table[0][6]

      # Calculate Pizza Price
      pizza_price_total = pizza_price_total + (pizza_price * quantity)
      
      # Add to order summary
      if quantity and size and flavour:
        if quantity > 1:
          order_summary.append(f"{quantity} {size} {flavour} pizzas({quantity} * {pizza_price} = {pizza_price * quantity})")
        else:
          order_summary.append(f"{quantity} {size} {flavour} pizza({quantity} * {pizza_price} = {pizza_price * quantity})")
        
    # after pizza processing, check for other parameters...
    # Phone Number
    if not current_store["phone_number"]:
      missing_other_parameters.append("phone number")
    
    # Address
    if not current_store["address"]:
      missing_other_parameters.append("address")

    # if other parameters have an issue, prompt well for 
    if missing_other_parameters:
      if len(missing_other_parameters) > 1:
        missing_str = ", ".join(x for x in missing_other_parameters)
        missing_str = missing_str.rsplit(", ", 1)
        missing_str = " and ".join(missing_str)
        fulfillment_text = f"Please specify your {missing_str}"
        print(f'missing {missing_other_parameters}')
        return textAndContext(fulfillment_text, output_context)
      else:
        fulfillment_text = f"Please specify your {missing_other_parameters[0]}"
        print(f'missing {missing_other_parameters[0]}')
        return textAndContext(fulfillment_text, output_context)

    # when all aparameters are good...
    address = current_store["address"]
    phone_number = current_store["phone_number"]

    pizza_uuid = uuid.uuid4()
    pizza_uuid_in_bytes = pizza_uuid.bytes

    # adding each item ordered to database
    for pizza in current_store["pizza_class"]:
      # Get Pizza ID
      sql = "SELECT * FROM pizzas WHERE PizzaName = %s"
      adr = (pizza["pizza-class-flavour"],)
      db_cursor.execute(sql, adr)
      pizzas_table = db_cursor.fetchall()

      pizza_id = pizzas_table[0][0]

      # add each item
      sql = """
        INSERT INTO `item_order` (`OrderUuid`, `PizzaId`, `PizzaSize`, `PizzaQuantity`)
        VALUES (%s, %s, %s, %s)
      """
      adr = (pizza_uuid_in_bytes, pizza_id, pizza["pizza-class-size"], pizza["pizza-class-quantity"])
      db_cursor.execute(sql, adr)
      db_conn.commit()


    # adding order to database
    sql = """
      INSERT INTO `order` (`OrderUuid`, `Address`, `PhoneNumber`)
      VALUES (%s, %s, %s)
    """
    adr = (pizza_uuid_in_bytes, current_store["address"], current_store["phone_number"])
    db_cursor.execute(sql, adr)
    db_conn.commit()

    
    fulfillment_text = f"You ordered: {'; '.join(order_summary)} for {phone_number} at {address}.\nTotal is {pizza_price_total}.\nYour Order ID is #{pizza_uuid}."

    # add to previous orders
    previous_orders.append({
      "pizza_classes": current_store["pizza_class"],
      "phone_number": current_store["phone_number"],
      "address": current_store["address"],
    })

    # print(previous_orders)
    # reset current store
    print("RESETTING STORE")
    current_store["pizza_class"] = []
    current_store["pizza_size_and_flavour"] = []
    current_store["pizza_size_and_quantity"] = []
    current_store["address"] = ""
    current_store["phone_number"] = ""

    expecting_size = False
    expecting_flavour = False
    expecting_quantity = False
    expecting_size_and_flavour = False
    expecting_size_and_quantity = False
    expecting_flavour_and_quantity = False

    is_params_empty = True
    return textAndContext(fulfillment_text, output_context)
  elif intentName == "Drinks General Question":
    sql = "SELECT * FROM drinks"
    db_cursor.execute(sql)
    drinks_table = db_cursor.fetchall()
    drink_types_set = set()
    
    for drink_row in drinks_table:
      drink_types_set.add(drink_row[1].lower())

    drink_types_list = list(drink_types_set)
    drink_types_str = ", ".join(drink_type for drink_type in drink_types_list)

    drink_types_str = drink_types_str.rsplit(", ", 1)
    drink_types_str = " and ".join(drink_types_str)

    
    response = {"fulfillmentText": f"The types of drinks are {drink_types_str}"}
    return jsonify(response)
  elif intentName == "Drinks Class General Question":
    sql = "SELECT * FROM drinks WHERE DrinkType = %s"
    drink_class = parameters.get('drink-class')
    adr = (drink_class,)
    
    db_cursor.execute(sql, adr)
    drinks_table = db_cursor.fetchall()

    drinks = []
    
    for drink_row in drinks_table:
      drinks.append(drink_row[2])

    
    drinks_str = ", ".join(drink for drink in drinks)

    drinks_str = drinks_str.rsplit(", ", 1)
    drinks_str = " and ".join(drinks_str)
    
    response = {"fulfillmentText": f"The {drink_class.lower()} drinks are {drinks_str}"}
    
    return jsonify(response)
  elif intentName == "Pizza Flavours General Question":
    sql = "SELECT * FROM pizzas"
    
    db_cursor.execute(sql)
    pizzas_table = db_cursor.fetchall()
    
    pizza_names = []
    
    for pizza_row in pizzas_table:
      pizza_names.append(pizza_row[1])
    
    pizza_names_str = ", ".join(pizza_name for pizza_name in pizza_names)
    
    pizza_names_str = pizza_names_str.rsplit(", ", 1)
    pizza_names_str = " and ".join(pizza_names_str)
    
    response = {"fulfillmentText": f"The types of pizzas are {pizza_names_str}"}
    return jsonify(response)
  elif intentName == "Pizzas Description General Question":
    # Get all pizzas
    sql = "SELECT * FROM pizzas WHERE PizzaName = %s"
    pizza_flavour = parameters.get('pizza-flavour')
    adr = (pizza_flavour,)
    db_cursor.execute(sql, adr)
    pizzas_table = db_cursor.fetchall()

    # Return Description
    response = {"fulfillmentText": f"{pizzas_table[0][2]}"}
    return jsonify(response)
  elif intentName == "Pizza Toppings General Question":
    # Get The Pizza ID
    sql = "SELECT * FROM pizzas WHERE PizzaName = %s"
    pizza_flavour = parameters.get('pizza-flavour')
    adr = (pizza_flavour,)
    db_cursor.execute(sql, adr)
    pizzas_table = db_cursor.fetchall()

    pizza_id = pizzas_table[0][0]

    # Get the Topping IDS
    sql = "SELECT * FROM pizzatoppings WHERE PizzaID = %s"
    adr = (pizza_id,)
    db_cursor.execute(sql, adr)
    pizzatoppings_table = db_cursor.fetchall()

    pizza_toppings_ids = []
    for pizzatoppings_row in pizzatoppings_table:
      pizza_toppings_ids.append(pizzatoppings_row[2])

    # Get Topping names
    topping_names = []

    for pizza_toppings_id in pizza_toppings_ids:
      sql = "SELECT * FROM toppings WHERE ToppingID = %s"
      adr = (pizza_toppings_id,)
      db_cursor.execute(sql, adr)
      toppings_table = db_cursor.fetchall()
      topping_names.append(toppings_table[0][1])

    # Return
    topping_names_str = ", ".join(topping_name for topping_name in topping_names)

    topping_names_str = topping_names_str.rsplit(", ", 1)
    topping_names_str = " and ".join(topping_names_str)

    response = {"fulfillmentText": f"The toppings for {pizza_flavour} are {topping_names_str}"}
    
    return jsonify(response)
  elif intentName == "Pizza Prices Per Flavour":
    # Get all pizzas
    sql = "SELECT * FROM pizzas WHERE PizzaName = %s"
    pizza_flavour = parameters.get('pizza-flavour')
    adr = (pizza_flavour,)
    db_cursor.execute(sql, adr)
    pizzas_table = db_cursor.fetchall()

    # Return Description
    response = {"fulfillmentText": f"{pizza_flavour} prices are as follows. Small: {pizzas_table[0][3]}, Medium: {pizzas_table[0][4]}, Large: {pizzas_table[0][5]}, Super Large: {pizzas_table[0][6]}"}
    
    return jsonify(response)
  elif intentName == "Pizza Prices Per Flavour And Size":
    # Get all pizzas
    sql = "SELECT * FROM pizzas WHERE PizzaName = %s"
    pizza_flavour = parameters.get('pizza-flavour')
    adr = (pizza_flavour,)
    db_cursor.execute(sql, adr)
    pizzas_table = db_cursor.fetchall()

    pizza_size = parameters.get('pizza-size')
    pizza_price = 0
    if pizza_size == "small":
      pizza_price = pizzas_table[0][3]
    elif pizza_size == "medium":
      pizza_price = pizzas_table[0][4]
    elif pizza_size == "large":
      pizza_price = pizzas_table[0][5]
    elif pizza_size == "super large":
      pizza_price = pizzas_table[0][6]
    
    # Return Description
    response = {"fulfillmentText": f"A {pizza_size} {pizza_flavour} costs {pizza_price}"}
    
    return jsonify(response)
  elif intentName == "Cancel Order - yes":
    current_store["pizza_class"] = []
    current_store["pizza_size_and_flavour"] = []
    current_store["pizza_size_and_quantity"] = []
    current_store["address"] = ""
    current_store["phone_number"] = ""
    
    response = {"fulfillmentText": "Order is cancelled."}
    return jsonify(response)
  else:
    response = {"fulfillmentText": f"There are no fulfillment responses defined for Intent {intentName}" }
    return jsonify(response)

def textAndContext(text, context):  
  response = {
    "fulfillmentText": text,
    "outputContexts": [context]
  }
  
  return jsonify(response)

app.run(host='0.0.0.0', port=81)
