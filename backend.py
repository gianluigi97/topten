from flask import Flask, render_template, request
from funcs.integrationIA import ListTen
from funcs.database import Database

app = Flask(__name__)


@app.route("/")
def index():

    categoria = request.args.get("categoria", "").strip()
    refresh = request.args.get("refresh") == "True"

    if not categoria:
        return render_template("index.html", classifica=[], categoria="",fonte="")

    service = ListTen()
    db = Database(database="Topten")

    existing_list = db.select(table_name="records", c_input=categoria)

    if existing_list and not refresh:
        classifica = existing_list
        fonte = "database"

    else: 
        raw_ranking = service.get_rank(richiesta=categoria)

        if not existing_list:
            db.insert(
                table_name="records", 
                lista_ranking=service.format_ia_response(raw_ranking, categoria=categoria.lower(), 
                db=True)
                )
            
        classifica = service.format_ia_response(raw_ranking)
        fonte = "ChatGPT"
        
    return render_template(
        "index.html", 
        classifica=classifica, 
        categoria=categoria,
        fonte=fonte
        )



if __name__ == "__main__":
    app.run(debug=True)


