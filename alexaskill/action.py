import urllib, json

url = "https://0s2cp85xw1.execute-api.us-east-1.amazonaws.com/prod/RecipeUpdate?TableName=Recipes"
response = urllib.urlopen(url)
data = json.load(response)

TITLE = "Recipe Assistant"

def lambda_handler(event, context):
    # print("event.session.application.applicationId=" +
    #       event['session']['application']['applicationId'])

    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.ask.skill.144f905f-e3bb-4f7d-8afa-e4b9879d3dd8"):
    #     raise ValueError("Invalid Application ID") 

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

def on_session_started(session_started_request, session):
    """Called when the session starts"""

    print("on_session_started requestId=" +
          session_started_request['requestId'] + ", sessionId=" +
          session['sessionId'])

    return get_welcome_response()

def on_launch(launch_request, session):
    """
    Called when the user launches the skill without specifying what they
    want.
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    return get_welcome_response()

def get_welcome_response():
    speech_output = ("Recipe assistant here. What recipe would you like to make?")
    should_end_session = False
    attributes = {'mode': "Main"}
    return build_response(attributes, build_speechlet_response(TITLE, speech_output, should_end_session))

def on_session_ended(session_ended_request, session):
    """
    Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])

def on_intent(intent_request, session):
    """Called when the user specifies an intent for this skill"""

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    
    if intent_name == "ItemIntent":
        return handle_item_request(intent, session)
    elif intent_name == "HelpIntent":
        return handle_help_request(intent, session)
    elif intent_name == "QuitIntent":
        return handle_quit_request(intent, session)
    elif intent_name == "IngredientIntent":
        return handle_ingredient_request(intent, session)
    elif intent_name == "NextIngredientIntent":
        return handle_next_ingredient_request(intent, session)
    elif intent_name == "LastIngredientIntent":
        return handle_last_ingredient_request(intent, session)
    elif intent_name == "RestartIntent":
        return handle_restart_request(intent, session)
    elif intent_name == "NextStepIntent":
        return handle_next_step_request(intent, session)
    elif intent_name == "LastStepIntent":
        return handle_last_step_request(intent, session)
    elif intent_name == "RecipeIntent":
        return handle_recipe_request(intent, session)
    else:
        raise ValueError("Invalid intent")

def handle_item_request(intent, session):
    #Should enter recipe dialogue and get requested recipe from the database
    title = intent['name']
    request = intent['slots']['Recipe']['value'].lower()
    should_end_session = False
    
    #Get list of ingredients and list of steps for requested recipe from database
    #(Right now, I am just searching items, the dictionary I made at the top)
    found = False
    for item in data["Items"]:
        if item["RecipeName"] == request:
            ingredients = item["Ingredients"].split('\n')
            steps = item["Directions"].split('\n')
            found = True

    if not found:
        speech_output = "Sorry, the requested item was not found in our database"
        attributes = {'mode': "Main"}
    
    else:
        speech_output = "Recipe found"
        attributes = {'mode': "Ingredients",
                      'ingredients': ingredients,
                      'steps': steps,
                      'ingredientNum': 0,
                      'stepsNum': 0
                      }
  
    return build_response(attributes, build_speechlet_response(title, speech_output, should_end_session))
  
def handle_help_request(intent, session):
    #Should handle what can I say
    title = intent['name']
    should_end_session = False
    speech_output = ""  # List all possible utterances
    attributes = session['attributes']
    
    if attributes['mode'] == "Main":
        speech_output = "You can say 'find' a certain item, 'I'd like to make' a certain item, or 'quit'"

    elif attributes['mode'] == "Ingredients":
        speech_output = "You can say 'what are the ingredients', 'next ingredient', 'last ingredient'," \
                        "'start again', 'main menu', 'conclude', or 'leave'"

    else:
        speech_output = "You can say 'read recipe', 'start', 'next step', 'last step'," \
                        "'start again', 'main menu', 'conclude', or 'leave'"
                        
    return build_response(attributes, build_speechlet_response(title, speech_output, should_end_session))
  
def handle_quit_request(intent, session):
    #Should handle exit or quit in any of the modes (main, recipe, directions)
    title = intent['name']
    attributes = session['attributes']
    should_end_session = False
    
    #If there are no attributes, you are in the main mode
    if attributes['mode'] == "Main":
        #Quit the app
        speech_output = "Quitting app"
                          
    elif attributes['mode'] == "Ingredients" or attributes['mode'] == "Steps":
        speech_output = "Quitting " + attributes['mode'] + " mode"
        attributes = {'mode': "Main"}              
                      
    return build_response(attributes, build_speechlet_response(title, speech_output, should_end_session))
                          
def handle_ingredient_request(intent, session):
    #Return the first ingredient in the recipe
    title = intent['name']
    attributes = session['attributes']
    should_end_session = False
    
    if attributes['mode'] == "Main":
        speech_output = "Please specify an item you would like to make"

    else:
        if len(attributes['ingredients']) >= 1:
            speech_output = attributes['ingredients'][0]
            attributes['ingredientNum'] = 1 
        else:
            speech_output = "There are no ingredients"
                          
    return build_response(attributes, build_speechlet_response(title, speech_output, should_end_session))
                          
def handle_next_ingredient_request(intent, session):  
    #Return the next ingredient in the recipe
    title = intent['name']
    attributes = session['attributes']
    should_end_session = False
    
    speech_output = attributes['ingredients'][attributes['ingredientNum']]
    attributes['ingredientNum'] += 1

    if attributes['ingredientNum'] == len(attributes['ingredients']):
        attributes['mode'] = "Steps"
        attributes['ingredientNum'] = 0
        speech_output += "<break time=\"1s\" /> You are now in the recipe directions dialogue"
                          
    return build_response(attributes, build_speechlet_response(title, speech_output, should_end_session))
                          
def handle_last_ingredient_request(intent, session):
    #Return last ingredient in the recipe
    title = intent['name']
    attributes = session['attributes']
    should_end_session = False
                          
    ingredients = attributes['ingredients']                
    speech_output = ingredients[len(ingredients) - 1] + "<break time=\"1s\" /> You are now in the recipe directions dialogue"
    attributes['mode'] = "Steps"
    attributes['ingredientNum'] = 0
               
    return build_response(attributes, build_speechlet_response(title, speech_output, should_end_session))
                  
def handle_restart_request(intent, session):
    #Handles restarting the inside 2 modes (recipe, directions)
    title = intent['name']
    attributes = session['attributes']
                          
    if attributes['mode'] == "Ingredients":
        return handle_ingredient_request(intent, session)

    elif attributes['mode'] == "Steps":
        return handle_recipe_request(intent, session)
                          
def handle_next_step_request(intent, session):
    #Return following instructions for the recipe one by one
    title = intent['name']
    attributes = session['attributes']
    should_end_session = False
    
    speech_output = attributes['steps'][attributes['stepsNum']]
    attributes['stepsNum'] += 1     

    if attributes['stepsNum'] == len(attributes['steps']):
        attributes['stepsNum'] = 0
        speech_output += "<break time=\"1s\" /> You have reached the last step. Say 'main menu' to go to main mode"
                  
    return build_response(attributes, build_speechlet_response(title, speech_output, should_end_session))
                          
def handle_last_step_request(intent, session):
    #Return last step in the recipe
    title = intent['name']
    attributes = session['attributes']
    should_end_session = False
                          
    steps = attributes['steps']                
    speech_output = steps[len(steps) - 1] + "<break time=\"1s\" /> You have reached the last step. Say 'main menu' to go to main mode"
    attributes['stepsNum'] = len(steps) - 1
                  
    return build_response(attributes, build_speechlet_response(title, speech_output, should_end_session))
                          
def handle_recipe_request(intent, session):
    #Returns the first step of the recipe
    title = intent['name']
    attributes = session['attributes']
    should_end_session = False
    
    if attributes['mode'] == "Main":
        speech_output = "Please specify an item you would like to make"

    else:
        if len(attributes['steps']) >= 1:            
            speech_output = attributes['steps'][0]
            attributes['stepsNum'] = 1  
        else:
            speech_output = "There are no steps"
    
    return build_response(attributes, build_speechlet_response(title, speech_output, should_end_session))
                          
def build_speechlet_response(title, output, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'shouldEndSession': should_end_session
    }
    
def build_response(attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': attributes,
        'response': speechlet_response
    }