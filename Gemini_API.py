import google.generativeai as genai
import PIL.Image

chat = None
query_chat = None
def Start_a_ChatSecondApiChat(second_api_key):
    genai.configure(api_key=second_api_key)
    global  query_chat
    model = genai.GenerativeModel('gemini-1.5-flash')
    query_chat = model.start_chat(history=[])
def Start_a_Chat(api_key):
    genai.configure(api_key=api_key)
    global  chat
    model = genai.GenerativeModel('gemini-1.5-flash')
    chat = model.start_chat(history=[])
    # json_data = Data_Recommendation.data[:300].to_json(orient='records')

    # initial_prompt = f"Here's some data:\n  {json_data} \n Please remember the data as u are the centeral management of entire store ."
    # chat.send_message(initial_prompt)



def images(path):
    img = PIL.Image.open(path)
    prompt2 = "Identify the clothing items in the image and provide a good user written prompt who is looking for the cloth shown in the image. Be professional as you are an expert in clothing."
    response = chat.send_message([prompt2,img])
    print("Model Response Image : "+response.text)
    return response.text
def getClothPrompt(prompt,new_question):
    prompt2 = f"New question. I want to  feed this {prompt} to my encoder for vector db search merge it with any previous context and make a line that reserve the context your output must be just a sentence" if new_question==True else f"\"{prompt}\" <- This is the user's query. If you have previous context related to current query only then use it with current query, but do not include all the previous context, just use context related to current query and generate a nice user created prompt. If you do have any previous context about the given prompt, then just return a prompt as it is by checking if there's any spelling mistakes. Your output should be only the user created prompt, nothing else."
    response = query_chat.send_message(prompt2)
    print("prompt 2", response.text)
    return response.text

def give_indices(user_prompt):
    prompt1 = user_prompt
    print(user_prompt)
    prompt2 = "Given these above requirements provide me with product id that matches the user need "
    prompt3="The Output format should list of product id For ex [1,2,3,4,5,8], If there is no product then give most matching product ids based on name or description list The output should be just a list nothing else"
    prompt=(f"User For men :{prompt1} , "
            f"{prompt2} ,{prompt3}")
    response = chat.send_message(prompt)
    print("Model Response : "+response.text)
    li = response.text.split(',')[1:-1]
    return li

def getLLMResponse(user_prompt,data,score):
    prompt = f"New Question. You are an expert in clothing. Recommend the best products based on this search query: {user_prompt}. Here are the top products: {data}. Be professional and Do not return product data in response but just give a gist of product type. Do not make user feel uncomfortable with your response. If {score} is less than 0.3, only then ask user in a nice way to ask query related to clothing more specifically for personalized recommendations. Your current query is not directly related to clothing. If user query is friendly like \"Hi or Hello , How are you?\" then respond it in a nice way asking \"How can I assist you today?\". Do not help user with query which is not related to clothing."
    response = chat.send_message(prompt)
    print(response.text)
    return response.text