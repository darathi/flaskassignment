
import logging

from flask import Flask, Blueprint, jsonify,render_template,url_for,redirect
from flask_pymongo import pymongo
from flask import jsonify, request
import pandas as pd

    
con_string = "mongodb+srv://darathi:darathi@cluster0.tcprpse.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_string)

db =client.get_database('book')

user_collection = pymongo.collection.Collection(db, 'bookdatabase') #(<database_name>,"<collection_name>")
print("MongoDB connected Successfully")

def project_api_routes(endpoints):

    @endpoints.route('/welcome', methods=['GET'])
    def hello():
        res = 'Welcome to the Book Catalog'
        print("Hello world")
        return res

    @endpoints.route('/add-books', methods=['POST'])
    def addbook():
        resp = {}
        try:
            req_body = request.json
            user_collection.insert_one(req_body)            
            print("Book Data entered Successfully!")
            status = {
                "statusCode":"200",
                "statusMessage":"Book Data entered Successfully!"
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp


    @endpoints.route('/add-many-books', methods=['POST'])
    def add_many_books():
        resp = {}
        try:
            req_body = request.json
            user_collection.insert_many(req_body)            
            print("Book Data entered Successfully!")
            status = {
                "statusCode":"200",
                "statusMessage":"Book Data entered Successfully!"
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp


   

    @endpoints.route('/read-books',methods=['GET'])
    def read_books():
        resp = {}
        try:
            bookdata = user_collection.find({})
            print(bookdata)
            bkdatalist =list(bookdata)
            status = {
                "statusCode":"200",
                "statusMessage":"Book Data Retrieved Successfully from the Database."
            }
            output = [{'title' : bookpiece['title'], 
            'isbn' : bookpiece['isbn'],
            'pageCount' : bookpiece['pageCount'],
            'publishedDate' : bookpiece['publishedDate'],
            'thumbnailUrl' : bookpiece['thumbnailUrl'],
            'longDescription' : bookpiece['longDescription'],
            'status' : bookpiece['status'],
            'authors' : bookpiece['authors'],
             'categories' : bookpiece['categories']
            } for bookpiece in bkdatalist]  #list comprehension
            resp['data'] = output
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp


    @endpoints.route('/update-books',methods=['PUT'])
    def update_book_data():
        resp = {}
        try:
            req_body = request.json
            # req_body = req_body.to_dict()
            user_collection.update_one({"isbn":req_body['isbn']}, {"$set": req_body['update_book_data']})
            print("Book Updated Successfully in the Database.")
            status = {
                "statusCode":"200",
                "statusMessage":"Book Data Updated Successfully in the Database."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp    

    @endpoints.route('/template',methods=['GET','POST'])
    def getdoc():
        resp = {}
        try:
            
            return render_template('sample.html')
        
        except Exception as e:
            print(e)
            status={
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp    


    @endpoints.route('/delete',methods=['DELETE'])
    def delete():
        resp = {}
        try:
            delete_isbn= request.args.get('isbn')
            user_collection.delete_one({"isbn":delete_isbn})
            status = {
                "statusCode":"200",
                "statusMessage":"Book Data Deleted Successfully in the Database."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp
    
    @endpoints.route('/file_upload',methods=['POST'])
    def file_upload():
        resp = {}
        try:
            req = request.form
            file = request.files.get('file')
            df = pd.read_csv(file)
            print(df)
            print(df.head)
            print(df.columns())
            status = {
                "statusCode":"200",
                "statusMessage":"File uploaded Successfully."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp

# def get_database():
   

#     # Provide the mongodb atlas url to connect python to mongodb using pymongo
#     CONNECTION_STRING = "mongodb+srv://<username>:<password>@<cluster-name>.mongodb.net/myFirstDatabase"

#     # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
#     from pymongo import MongoClient
#     client = MongoClient(CONNECTION_STRING)

#     # Create the database for our example
    return endpoints
# @endpoints.route('/index',methods=['GET','POST'])
    # def index():
    #     if 'username' in session:
    #         return "You are logged in as"+session['username']
    #     return render_template('login.html')
    #     # print('index')
    #     # return render_template('sample.html')
    # @endpoints.route('/login',methods=['GET','POST'])
    # def login():
    #     users="collection name of users"
    #     login_user=users.find_one({'username':request.form['username']})
    #     if login_user :
    #         if()