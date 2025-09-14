from pydantic import BaseModel
import psycopg2
import os

DATA_FILE="/data/notas.txt"


DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT","5432")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

class Nota(BaseModel):
    titulo: str
    contenido: str

    def guardar(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO notas (titulo, contenido) VALUES (%s, %s) RETURNING id",
            (self.titulo, self.contenido)
        )
        nota_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        with open(DATA_FILE, "a", encoding="utf-8") as f:
            print(f.name)
            f.write(f"{nota_id},{self.titulo},{self.contenido}\n")

        return {"message": "Nota guardada correctamente", "id": nota_id}
    
    @staticmethod
    def todas():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, titulo, contenido FROM notas")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        notas = [{"id": row[0], "titulo": row[1], "contenido": row[2]} for row in rows]
        return {"notas": notas}