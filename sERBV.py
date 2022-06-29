from BOTTEL import telegram_chatbot
from nested_lookup import nested_lookup
import json
from urllib.request import urlopen
import schedule
import ast
# loads subscriber data
with open("SubData.txt", "r+") as withRp:
    cont = withRp.read()
if cont != "":
    ub = ast.literal_eval(cont)
else:
    ub = {}
# updates the delta data
def DelUd():
    with open("Delta.json", "r+") as ld:
        nl = ld.read()
        return json.loads(nl)
DeltaDict = {}
bot = telegram_chatbot("config.cfg")
# this adds subscriber
def SubTimer(msg, id):
    if informer(msg) != "Please enter correct district. You may check spelling on Google :)":
        ub[id] = msg
        with open("SubData.txt", "r+") as withRp:
            withRp.truncate()
            withRp.write(str(ub))
        return "You Are Now Subscribed.You will recieve daily Corona Updates at 8:30 am everyday." + "\n\n" + informer(
            msg)
    else:
        return "Press /daily again and re-Enter Correct District spelling"
# this is schedule message sender
def sender():
    print("Schedule Message Sent")
    for ids, dists in ub.items():
        bot.send_message(informer(dists), ids)


# this is main function which uses json data from covid 19 api and searches it "
def informer(dist):
    jurl = urlopen("https://api.covid19india.org/state_district_wise.json")
    obj = json.loads(jurl.read())
    val = nested_lookup(dist, obj)
    DeltaDict = DelUd()
    try:
        if DeltaDict[dist] >= 0:
            return "Active cases in your district are: " + str(
                val[0]['active']) + "\n\n" + "The total cases till date are: " + str(
                val[0]["confirmed"]) + "\nTotal deaths till now: " + str(
                val[0]['deceased']) + "\nPatients Recovered: " + str(val[0]["recovered"])
        else:
            return "New Cases in your District are: " + str(
                -DeltaDict[dist]) + "\n\n" + "Active cases in your district are: " + str(
                val[0]['active']) + "\n" + "The total cases till date are: " + str(
                val[0]["confirmed"]) + "\nTotal deaths till now: " + str(
                val[0]['deceased']) + "\nPatients Recovered: " + str(val[0]["recovered"])
    except:
        return "Please enter correct district. You may check spelling on Google :)"

schedule.every().day.at("03:30").do(sender)

print("Bot server is ON")
# this processes the input
def make_reply(msg):
    reply = None
    if msg is not None:
        reply = informer(msg)
        print(msg)
        return reply
# id for knowing if subbscribe request
stid = False
update_id = None
# this lop fetch updates and passes it
while True:
    schedule.run_pending()
    updates = bot.get_updates(offset=update_id)
    updates = updates["result"]  # this stors all user id text etc

    # below lines checks if updates have came or timeout is done(came is +1 update id)
    # if came it fetch message text and user id . it sends meesage INPUT to the make reply function ,the OUTPUT
    # from this make reply is returned to send message function with user id that this fetched from updates
    # takes input and SUBSCRIBER ID and sends ,this message reciever
    if updates:
        for item in updates:
            update_id = item["update_id"]
            try:
                message = str(item["message"]["text"])
            except:
                message = None
            from_ = item["message"]["from"]["id"]  # id
            try:
                print(item["message"]["from"]["username"])
            except:
                print("No Username")
            if message == "/daily":
                bot.send_message("Enter District for which you would like daily updates", from_)
                stid = True
            elif stid is True:
                stid = False
                reply = SubTimer(message, from_)  # sent to process input
                bot.send_message(reply, from_)  # returns output with  id
            else:
                reply = make_reply(message)
                bot.send_message(reply, from_)
