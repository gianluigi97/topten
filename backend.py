from flask import Flask, render_template, request
from funcs.get_lists import ListTen

app = Flask(__name__)

@app.route("/")
def index():
    categoria = request.args.get("categoria", "").strip()
    service = ListTen()
    raw_ranking = service.get_rank(richiesta=categoria)
    classifica = service.format_ia_response(raw_ranking) if categoria else []
    return render_template("index.html", classifica=classifica, categoria=categoria)





if __name__ == "__main__":
    app.run(debug=True)