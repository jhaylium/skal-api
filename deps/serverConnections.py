#Connect to SQL Server
import datetime
import pyodbc
from configparser import ConfigParser
from deps import storedProcedures
from deps import geocoding

def connectToServer():
    cfg = ConfigParser()
    cfg.read(r'C:\Users\Jeffery\Documents\PythonFiles\SkalApi\firstTest\skalcred.ini')
    #set up credentials for API
    serverName = cfg.get('skalServer', 'server')
    username = cfg.get('skalServer', 'userName')
    password = cfg.get('skalServer', 'passWord')
    database = cfg.get('skalServer', 'dataBase')
    #Connect to Database
    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};SERVER=' + serverName + ';DATABASE='+ database +
                          ';UID=' + username + ';PWD=' + password, autocommit=True)
    cursor = conn.cursor()
    return  cursor

def createUser(args, connect):
    sql = storedProcedures.createUser
    params = args
    connect.execute(sql,params)
    data = connect.fetchall()
    if len(data != 0):
        createdStatus = 'User Created'
    else:
        createdStatus = 'Something went wrong'
    return createdStatus;

def beerDetails(storedProcedure,beer_id,connect):
    sql = storedProcedure
    params = (beer_id)
    connect.execute(sql, params)
    data = connect.fetchall()[0]
    columns = [column[0] for column in connect.description]
    beerDict = {}
    for x,y in zip(columns,data):
        beerDict.update({x:y})
    return beerDict

def postBeerPrice(args,connect):
    # print("Start Beer Price Process")
    checkAddress = storedProcedures.checkAddress
    userInput = (args)
    lat = userInput[3]
    lng =  userInput[4]
    file = open("postBeerFile.txt", "a")
    file.write('Started Post Beer Request at ' + datetime.datetime.now().strftime('%m.%d.%YT%H.%M.%S') + "\n")
    file.close()
    # """Check if beer is already in the database"""
    # connect.execute()
    # data = connect.fetchall()
    # beerOnDatabase = list(data[0])
    """Check Address in Database"""
    # print('Run Address Check')
    connect.execute(checkAddress, [lat,lng])
    data = connect.fetchall()
    if len(data) > 0:
        locationList = list(data[0])
        """Check to see if location exists in database, if it doesn't use 
        Google to find address """
    else:
        # print('Location Not in Database')
        geocode = geocoding.Location()
        # print('Geocode Complete')
        locationList = geocode.getLocation(lat, lng)
    params = args + locationList
    # print(params)
    connect.execute(storedProcedures.postPrice, params)

    # print('beer placed')


def getLogin(storedProcedure, userName, password,connect):
    sql = storedProcedure
    params = userName
    connect.execute(sql,params)
    data = connect.fetchall()
    if len(data) != 0:
        if data[0][0] == password:
            loginStatus =  'Login Successful'
        else:
            loginStatus = 'Incorrect Password. Please try again or contact support.'
    else: loginStatus = 'UserName does not exist. Please create an account or contact support.'

    return loginStatus

def getAutoList(storedProcedure, connect):
    sql = storedProcedure
    connect.execute(sql)
    data = connect.fetchall()
    dict = {}
    for item in data:
        id = item[0]
        beer=item[1]
        dict.update({id:beer})
    return(dict)



def getBeerPrices(args, connect):
    sql = storedProcedures.getBeerPrices
    params = args
    jsonResult = {'results': {}}
    connect.execute(sql,params)
    data = connect.fetchall()
    if len(data) == 0:
        jsonResult = jsonResult['results'].update({'item0': 'No Data Found'})
        return jsonResult
    else:
        headers = ['beer_name', 'beer_price', 'units', 'store_address',
                   'store_name', 'brewery_logo', 'time_entered',
                   'user_name', 'beer_type', 'distance', 'brewery_name']

        itemNum = 0
        for item in data:
            n = 0
            dictionary = {}
            for value in item:
                if headers[n] == 'time_entered':
                    value = datetime.datetime.strftime(value, "%m/%d/%Y %H:%M:%S")
                dictionary.update({headers[n]: value})
                n = n + 1
            jsonResult['results'].update({'item' + str(itemNum): dictionary})
            itemNum = itemNum + 1
        return jsonResult




