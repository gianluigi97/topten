from flask import Flask, render_template, request
from funcs.get_lists import ListTen
from funcs.database import Database

app = Flask(__name__)


@app.route("/")
def index():
    categoria = request.args.get("categoria", "").strip()
    service = ListTen()
    db = Database(database="Topten")

    if not categoria:
        return render_template(
            "index.html",
            classifica=[],
            categoria=""
        )

    raw_ranking = service.get_rank(richiesta=categoria)
    db.insert(table_name="records", lista_ranking=service.format_ia_response(raw_ranking, categoria=categoria, db=True))
    classifica = service.format_ia_response(raw_ranking) if categoria else []

    return render_template(
        "index.html", 
        classifica=classifica, 
        categoria=categoria
        )



if __name__ == "__main__":
    app.run(debug=True)