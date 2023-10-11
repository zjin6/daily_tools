## install NeMo
# !pip install nemo_toolkit[nlp]
from nemo.collections.nlp.models import PunctuationCapitalizationModel
## pip install spacy
import spacy
## python -m spacy info
# This will display the information about the Spacy installation, including the version number and language models installed.

## pip install en_core_web_sm
nlp = spacy.load('en_core_web_sm')

# to get the list of pre-trained models
PunctuationCapitalizationModel.list_available_models()
# Download and load the pre-trained BERT-based model
model = PunctuationCapitalizationModel.from_pretrained("punctuation_en_bert")



text1 = '''
[Music] hello there how can i help you today hello i need to get to new york city by 5 p.m tonight is there a train that can get me there yes we have a train leaving in 30 minutes that will get you there at 2 45 pm or if you prefer to leave later we have an express train that leaves at 3 pm and arrives at 4 55 pm i think i'll take the earlier option i'd rather leave early and be relaxed then leave later and be worried that i might be late i have an important meeting at five and i cannot miss it i completely understand i'm the same way would you like to book that ticket now sure would you like a one-way ticket or a round-trip ticket just a one-way ticket for now i'm not sure when i'll be heading back home first class or second class how much does each ticket cost first class costs 100 but it includes a meal and a drink second class costs 50 i'll take a second class ticket i'll just grab a sandwich and a soda before i board the train like a good plan would you prefer a window seat or an aisle seat an aisle please perfect here is your ticket you'll leave from platform six make sure you're there 15 minutes before departure where is platform 6 go past the bookstore and turn right [Music] you'll see a kiosk selling magazines go past the kiosk and you'll see a sign for platforms six to ten follow that sign and you'll arrive at your platform thank you have a great trip and good luck with your meeting thanks [Music] hi there i was wondering if you could help me sure how can i help i'm not from the city and i'm trying to use the bus system for the first time well welcome to the great city of chicago and i can definitely help you navigate the bus routes where are you heading my plan for today is to visit the modern art museum stop at the zoo and then eat dinner downtown that sounds like a fun day you should probably get a 24 hour bus pass for unlimited bus rides that way you can stop and explore as much as you want in each neighborhood for the entire day that sounds great a lot of tourists prefer this option it's a good deal too instead of paying two dollars per bus ride you can pay eight dollars and ride all day perfect that's what i'll do then here is eight dollars and here is your 24 hour bus pass just show it to the driver each time you board the bus and where should i catch the bus to start there is a number five bus that stops in front of this station how often does it stop it stops here pretty often usually about every 10 minutes and will it take me to the museum yes let me get you a map yes thank you a map would be wonderful so you can see that our station is here you're heading to the museum which is here on the east end of the city you will board the number 5 bus and it will take you to a stop in front of the museum the name of the stop is modern art and when i leave the museum is there a bus to the zoo yes you'll go back to the modern art stop and look for the number 33 bus to stop get on this bus go four stops and you'll be at the zoo wonderful and to get from the zoo to downtown for dinner you'll want to catch the number eight bus and get off at the stop called restaurant row this will give you all kinds of dining options for dinner 
'''
text2 = '''
[Music] thank you so much i appreciate all of your help my pleasure good luck navigating and if you have any questions feel free to ask your driver as you board the bus they are very helpful i will thank you [Music] hi i need to get to the airport do you have a direct line to the airport we don't but you can easily get there by making just one transfer you take line 10 to south street then you change to line 8 and ride it all the way to dayton international airport how long does the ride take it takes about 10 minutes to get to south street and the line 8 ride takes about 35 minutes how much is the ticket it is 8.75 can i pay with credit card of course here you go thank you i just need your signature there you go perfect here is your ticket thanks where do i catch line 10 there's a yellow sign over there can you see it yes i can the yellow sign will lead you to line 10. great thanks for your help no problem happy to help where you heading today to the hilton hotel the one on 21st street or the one on main street the one on 21st street are you in town for business or is this a vacation a little bit of both i have a meeting for work but i also have time to relax and enjoy the city for a few days that's nice have you been here before i visited here with my family when i was 10 years old but that was a long time ago yep a lot has changed since then any recommendations for restaurants i should try i always like to eat at the local favorites when i'm in a new town my favorite is nathan's diner on elm street they have the best cheeseburgers sounds delicious i'll give it a try here we are the hilton hotel this is the newest hotel in the city i've heard it's a great place to stay it looks very nice thanks for the ride what do i owe you that'll be forty dollars here's fifty dollars keep the change thank you i appreciate it thanks for watching and be sure to subscribe to our youtube channel for more videos like this
'''

messytext_list = [text1, text2, 'text3']
# try the model on a few examples
neattext_list = model.add_punctuation_capitalization(messytext_list)

doc = nlp(neattext_list[0])

for sent in doc.sents:
    print()
    print(sent)
    
    