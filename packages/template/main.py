import json

CONFIG = json.load(open('./packages/weather/package_config.json'))
ANSWERS = json.load(open(CONFIG['python_datas']['answers']))['weather']

# Define here every function which is corresponding with an action
# Ex : I have an action called hello, so i must define a function hello
# Caution : the case bust be the same
# Ex : the "hello" action will never ba assiciated with "Hello" function

# Every function will have in parameter the entities from a sentence of the same type
# that the parameters defined in ./datas/expressions.json
# It will be a dict like {
#    "value": "the value of the parameter",
#    "type": "the type of the parameter",
#    "name": "the name of the parameter"
# }

# The function will return the chatbot response to the user, in str
def hello(entities):
    return 'hello'