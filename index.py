from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

cliente = MongoClient("mongodb+srv://gerenciadorcred:whBDSGd6FwuNnXOG@forworks.psgpztk.mongodb.net/")
db = cliente["kaizenApp"]
col_credentials = db["credenciais"]
col_empresa = db["empresa"]
col_imagens = db["image_empresa"]

app = Flask(__name__)


@app.route("/criar_empresa", methods=["POST"])
def criar_empresa():
    _id = str(ObjectId())

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


@app.route("/listar_empresa", methods=["POST"])
def listar_empresa():
    return [x for x in col_empresa.find()]


@app.route("/<_id>/pegar_logo", methods=["POST"])
def pegar_loogo(_id):
    return jsonify({"msg": col_imagens.find_one({"_id": _id})["logoEmpresa"]})


@app.route("/<qtd>/criar_credencial", methods=["POST"])
def criar_credencial(qtd):
    payload = request.json

    nova_qtd = int(qtd)
    qtd_antiga = int(col_empresa.find_one({'_id': payload["_id"]})["qtdCredenciais"])

    qtd_atualizada = qtd_antiga + nova_qtd

    for x in range(int(qtd)):
        col_credentials.insert_one({
            "_id": str(ObjectId()),
            "ativa": False,
            "empresa_id": payload["_id"]
        })

    col_empresa.update_one(
        {"_id": payload["_id"]},
        {"$set": {"qtdCredenciais":  qtd_atualizada}}
    )

    return jsonify({"msg": "Credenciais criada com sucesso!"})


@app.route("/<_id>/listar_credencial", methods=["POST"])
def listar_credencial(_id):
    return [x for x in col_credentials.find({"empresa_id": _id})]


if __name__ == "__main__":
    app.run()
