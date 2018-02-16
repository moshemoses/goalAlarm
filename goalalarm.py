import json, requests, datetime, time

def grab_data():
    res = requests.get('http://live.nhle.com/GameData/RegularSeasonScoreboardv3.jsonp')
    # We get back json data with some JS around it, gotta remove the JS
    json_data = res.text
    # Remove the leading JS
    json_data = json_data.replace('loadScoreboard(', '')
    json_data = json_data[:-1]
    data = json.loads(json_data)
    rawjson = data.get("games")
    return rawjson


def ifgametoday(team):
    
    """
    res = requests.get('http://live.nhle.com/GameData/RegularSeasonScoreboardv3.jsonp')
    # We get back json data with some JS around it, gotta remove the JS
    json_data = res.text
    # Remove the leading JS
    json_data = json_data.replace('loadScoreboard(', '')
    json_data = json_data[:-1]
    data = json.loads(json_data)
    drek = data.get("games")
    """    
	
    #establish current date
    Today = datetime.datetime.now()
    Today_formatted_day = Today.strftime('%A')
    Day_of_week = Today_formatted_day.upper()
    Month = Today.strftime('%m')
    Day = Today.strftime('%d')
    Month = Month.lstrip('0')
    Day = Day.lstrip('0')
    Date_var = str(Day_of_week+" "+Month+"/"+Day)
    
    #get data 
    rawdata = grab_data()  
    
    #Team name
    team_name = team
    
    #takes the weeks games for team and makes a list
    Weeks_games = []
    for i in range(0, len(rawdata)):
        if team_name in rawdata[i].values():
            Weeks_games.append(rawdata[i])
    
	#find out if game today and create time and id
    for i in range(0, len(Weeks_games)):
        if "TODAY" in Weeks_games[i].values():
            the_game = Weeks_games[i]
            game_time = the_game.get("bs")#grabs the game time
            now = datetime.datetime.now()
            now = now.strftime('%Y-%m-%d')
            new = now + " " +game_time
            print(new)
            game_time = datetime.datetime.strptime(new, '%Y-%m-%d %I:%M %p')
            game_time = game_time + datetime.timedelta(hours=3)
            print(game_time)
            game_id = the_game.get("id") # game id
            while datetime.datetime.now() < game_time:
                print("game today, waiting until gametime")
                time.sleep(60)
            watch_game(game_id, team_name)
        elif "LIVE" in Weeks_games[i].values():
            the_game = Weeks_games[i]
            game_id = the_game.get("id") # game id
            print("LIVE")
            watch_game(game_id, team_name)

        elif "progress" in Weeks_games[i].values():
            the_game = Weeks_games[i]
            game_id = the_game.get("id") # game id
            print("progress")
            watch_game()
        elif "final" in Weeks_games[i].values():
            the_game = Weeks_games[i]
            print("game over")
            

def home_away(game, team):
    for k, v in game[0].items():
        if v == team:
            home_away = k
          
    if home_away[0] == "h":
        score_key = "hts"
        return(score_key)
    elif home_away[0] == "a":
        score_key = "ats"
        return(score_key)
    else:
        return("home_away test not working")

def goals(game_info, score_key):
    team_initial_score = game_info[0].get(score_key)
    return(team_initial_score)
    
def status_check(current_game):
    for i in range(0, len(current_game)):
        if "LIVE" in current_game[i].values():
           return True
        elif "progress" in current_game[i].values():
            return True
        elif "final" in current_game[i].values():
            return False
        else:
            return False
            

def watch_game(g_id, team):
    gamestatus = True
    initialscore=10

    while gamestatus == True:
        print("waiting 5 sec")
        time.sleep(5)
        gamedata = grab_data()
        current_game = []
        for i in range(0, len(gamedata)):
            if g_id in gamedata[i].values():
                current_game.append(gamedata[i])
       
        herethere = home_away(current_game, team)
        goals_scored = goals(current_game, herethere)
        status = status_check(current_game)
        if status == True:
            if int(goals_scored) > int(initialscore):
                print("goal goal goal")
                print("initial score was")
                print(initialscore)
                print("now score is")
                print(goals_scored)
                initialscore = goals_scored
            else: 
                print("same score")
                print("initial score was")
                print(initialscore)
                print("now score still is")
                print(goals_scored)

        elif status==False:
            print("game is over")
            if goals_scored > initialscore:
                print("goal goal goal")
                print("initial score was")
                print(initialscore)
                print("now score is")
                print(goals_scored)
                initialscore = goals_scored
            else: 
                print("same score")
                print("initial score was")
                print(initialscore)
                print("now score still is")
                print(goals_scored)
            gamestatus=False
        else:
            print("error")
            gamestatus=False




    

letswatch = raw_input("Which team shall we monitor?")
ifgametoday(letswatch)