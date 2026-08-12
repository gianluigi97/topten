from sqlalchemy import create_engine, text, insert, MetaData, Table, select
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
from funcs.stringMatch import similarity

# load_dotenv(r"C:\GianC\topten\key.env") # Windows
# load_dotenv(r"/Users/gianluigimosti/WorkPlace/topten/key.env") # Mac
load_dotenv()

class Database:

    def __init__(self, database):

        self.username = os.getenv("DB_USERNAME")
        self.password = os.getenv("DB_PASSWORD") 
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.db = database

        self._engine = None
        self._metadata = MetaData()
        self._tables = {}

    def _get_engine(self):

        if self._engine: 
            return self._engine

        self._engine = create_engine(
            f"mysql+pymysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.db}",
            connect_args={'connect_timeout':5}
        )

        return self._engine

    def _get_table(self, table_name):

        if table_name in self._tables:
            return self._tables[table_name]

        table = Table(
            table_name,
            self._metadata,
            autoload_with=self._get_engine()
        )

        self._tables[table_name] = table
        return table

    def similarString(self, customer_input, accurancy=0.8):

        table = self._get_table("famiglie_categorie")
        stmt = select(table)

        with self._get_engine().begin() as conn:
            res = conn.execute(stmt).fetchall()

        famiglie = [r[0] for r in res]

        result_string = None
        actual_ratio = 0

        for existing_fam in famiglie: 
            ratio = similarity(existing_fam, customer_input)
            if ratio > actual_ratio and ratio >= accurancy:
                actual_ratio = ratio
                result_string = existing_fam
            else: 
                continue

        return result_string


    def select(self, table_name, c_input):

        table = self._get_table(table_name)
        famiglia = self.similarString(c_input)
        if famiglia: 
            stmt = select(table.c.posizione, table.c.nome).where(table.c.famiglia==famiglia.lower())

            with self._get_engine().begin() as conn:
                res = conn.execute(stmt).fetchall()

                return [
                        {
                            'posizione' : r[0],
                            'nome' : r[1],
                            'famiglia' : famiglia
                        }
                        for r in res
                    ]
        else:
            return None


    def insert(self, table_name, lista_ranking: dict):

        if not lista_ranking: 
            return 

        for el in lista_ranking: 
            el.pop('descrizione', None)

        table = self._get_table(table_name)
        stmt = insert(table)

        with self._get_engine().begin() as conn:
            conn.execute(stmt, lista_ranking)


if __name__ == "__main__":

    db = Database(database="Topten")
    result = db.select(table_name="records", c_input="invenzioni piu importanti della storia dell'uomo")

    print(result)
