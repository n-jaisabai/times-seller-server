from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
import pyrebase

config = {
    "apiKey": "AIzaSyCCxaqjq7ELPCdZTeAnyXKKN84beNIhRuU",
    "authDomain": "times-seller.firebaseapp.com",
    "databaseURL": "https://times-seller.firebaseio.com",
    "storageBucket": "times-seller.appspot.com",
    "messagingSenderId": "106379103348",
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

app = Flask(__name__)
api = Api(app)
cors = CORS(app)


class ProductsApi(Resource):
    def get(self):
        try:
            products = []
            res = db.child('products').get().val()
            for key, value in res.items():
                data = {key: value}
                products.append(data)
            return products
        except Exception as err:
            return str(err)

    def post(self):
        try:
            data = request.get_json()
            db.child("products").push(data)
            return jsonify({'result': 'Success!'})
        except Exception as err:
            return jsonify({'error': str(err)})


class ProductApi(Resource):
    def get(self, todo_id):
        try:
            products = db.child('products').child(todo_id).get()
            return products.val()
        except Exception as err:
            return str(err)

    def put(self, todo_id):
        try:
            data = request.get_json()
            db.child("products").child(todo_id).update(data)
            return jsonify({'result': 'Success!'})
        except Exception as err:
            return jsonify({'error': str(err)})

    def delete(self, todo_id):
        try:
            db.child("products").child(todo_id).remove()
            return jsonify({'result': 'Success!'})
        except Exception as err:
            return jsonify({'error': str(err)})


api.add_resource(ProductsApi, '/api/1.0/products')
api.add_resource(ProductApi, '/api/1.0/product/<todo_id>')


if __name__ == '__main__':
    app.run()
