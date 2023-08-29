from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

cliente = MongoClient("mongodb+srv://gerenciadorDeCredenciais:3trjdQSmrrjaXHMv@forworks.psgpztk.mongodb.net/")
db = cliente["kaizenApp"]
col_credentials = db["credenciais"]
col_empresa = db["empresa"]
col_imagens = db["image_empresa"]

app = Flask(__name__)


@app.route("/criar_empresa", methods=["POST"])
def criar_empresa():
    _id = str(ObjectId)

    payload = request.json

    col_empresa.insert_one(
        {
            "_id": _id,
            "nomeEmpresa": payload["nomeEmpresa"],
            "qtdCredenciais": payload["qtdCredenciais"]
        }
    )

    col_imagens.insert_one(
        {
            "_id": _id,
            "logoEmpresa": payload["logoEmpresa"]
        }
    )

    return jsonify({"msg": "Empresa registrada com sucesso!"})



if __name__ == "__mai__":
    app.run()
