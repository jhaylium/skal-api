from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from deps import serverConnections
from deps import storedProcedures
from deps.urlArgument import urlArguments
import datetime as dt
# from deps import BeerPriceStaging
# from deps import geocoding

app = Flask(__name__)
api = Api(app)

#set up variables to be passed from url
#parser = reqparse.RequestParser()
#beer id to be used with beer details
#parser.add_argument('beer_id', type=int, required=True)

apiVersion = '/api/v1'
#set up Resources and code for API
class Home(Resource):
    def get(self):
        return 'Welcome to the Skal API'

class BeerDetails(Resource):
    def get(self):
        beer_id = urlArguments.urlBeerDetails(self)
        if beer_id == '':
            return 'No Beer ID Specified'
        else:
            return jsonify(serverConnections.beerDetails(storedProcedures.beerDetails,beer_id,serverConnections.connectToServer()))

class UserInfo(Resource):
    def post(self):
        userInfo = urlArguments.urlAddUser(self)
        payloadUserData = []
        for u in userInfo.values():
            payloadUserData.append(u)
        arg = payloadUserData
        serverConnections.createUser(arg,serverConnections.connectToServer())


        return {'create user': 'new user created'}


class BeerPrice(Resource):
    def get(self):
        beerList = urlArguments.urlFindBeer(self)
        beer_data = []
        for b in beerList.values():
            beer_data.append(b)
        data = serverConnections.getBeerPrices(beer_data, serverConnections.connectToServer())


        return data

    def post(self):
        file = open("postBeerCall.txt", "a")
        file.write("Post Beer Called at " + dt.datetime.now().strftime('%m.%d.%YT%H.%M.%S') + "\n")
        priceList = urlArguments.urlBeerPrice(self)
        price = priceList
        #use to test output from url
        #return price
        price_data = []
        for p in price.values():
            price_data.append(p)
        arg = (price_data)
        # return price_data
        serverConnections.postBeerPrice(arg, serverConnections.connectToServer())
        file.write("Post Beer finished at " + dt.datetime.now().strftime('%m.%d.%YT%H.%M.%S') + "\n")
        # return 'Successfully Added'

class Login(Resource):
    def get(self):
        userLoginInfo = urlArguments.urlLogin(self)
        userName = userLoginInfo['userName']
        password = userLoginInfo['password']
        loginStatus = serverConnections.getLogin(storedProcedures.login,userName, password,serverConnections.connectToServer())
        return loginStatus


class AutoComplete(Resource):
    def get(self):
        beerList = serverConnections.getAutoList(storedProcedures.getBeerList, serverConnections.connectToServer())
        breweryList = serverConnections.getAutoList(storedProcedures.getBreweryList, serverConnections.connectToServer())
        beerTypeList = serverConnections.getAutoList(storedProcedures.getBeerTypeList, serverConnections.connectToServer())
        autoComplete = {'results':{'beer':beerList, 'brewery':breweryList, 'type':beerTypeList}}
        return autoComplete



#Map API Endpoints
api.add_resource(Home, '/')
api.add_resource(BeerDetails, apiVersion + '/beerdetails')
api.add_resource(UserInfo, apiVersion + '/userinfo')
api.add_resource(BeerPrice, apiVersion + '/beerprice')
api.add_resource(Login, apiVersion + '/login')
api.add_resource(AutoComplete, apiVersion + '/autolist')
#api.add_resource(UpdateDatabase, apiVersion + '/updatedata')


#if __name__ == '__main__':
#    app.run(debug=True)

