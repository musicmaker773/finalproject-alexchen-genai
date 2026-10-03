
import streamlit as st
from openai import OpenAI
import json

client = OpenAI(
    api_key = st.secrets["OPENAI_API_KEY"]
)

system_prompt = """
You are going to get some information about the game Plants Vs. Zombies. The user will enter in some information if it is a plant or a zombie followed by the name of the plant or zombie. You must get your information from Wikis of Plants vs. Zombies. For the Plants, you will get the story, Sun Cost, Health, and Damage. For the zombies, you will get the Overview or About, the toughness, health, the sun cost, the brain cost, and weakness of the zombie. 

Respond with a JSON in the following format if it is a plant:

{
    "Story": "STORY",
    "Sun Cost": #,
    "Health": #,
    "Damage": #

}

Respond with a JSON in the following format if it is a zombie:

{
    "Overview": "OVERVIEW",
    "Toughness": "TOUGHNESS",
    "Health": #,
    "Sun Cost": #,
    "Brain Cost": #,
    "Weakness", "WEAKNESS"

}

If information is not listed in the wikis, then label it as "None" if it is a string, or put 0 if it's a number.
"""

st.title("Plants VS Zombies")
st.write("This is a information searcher for the Plants and Zombies from Plants VS Zombies")

choice1 = st.selectbox("Plant or Zombie?", ["Plant", "Zombie"])

temp_str = st.text_input("Enter in the name of the Plant or Zombie you want to search infomration about: ")

user_prompt = choice1 + ": " + temp_str

btn = st.button("Submit")

if btn:
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    
    st.session_state["temp"] = json.loads(response.choices[0].message.content)

    if choice1 == "Plant":

        st.write(temp_str)
        st.write("Story: " + st.session_state["temp"]["Story"])
        st.write("Sun Cost: " + str(st.session_state["temp"]["Sun Cost"]))
        st.write("Health: " + str(st.session_state["temp"]["Health"]))
        st.write("Damage: " + str(st.session_state["temp"]["Damage"]))

    elif choice1 == "Zombie":
        st.write(temp_str)
        st.write("Overview: " + st.session_state["temp"]["Overview"])
        st.write("Toughness: " + st.session_state["temp"]["Toughness"])
        st.write("Health: " + str(st.session_state["temp"]["Health"]))
        st.write("Sun Cost: " + str(st.session_state["temp"]["Sun Cost"]))
        st.write("Brain Cost: " + str(st.session_state["temp"]["Brain Cost"]))
        st.write("Weakness: " + str(st.session_state["temp"]["Weakness"]))
