from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuration de la base de données MySQL.
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'db_user'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'blog_activite_creche'

mysql = MySQL(app)

@app.route("/")
def acceuil():
    # Effectuer une requête SELECT pour récupérer les trois derniers articles
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("SELECT id, titre, description FROM articles;")
    except Exception as e:
        print("Erreur SQL : ", str(e))

    articles = cursor.fetchall()
    print(articles[0])
    cursor.close()
    return render_template('acceuil.html', articles=articles)


# Définissez une route avec un paramètre dans l'URL.
# Le paramètre 'id' est une variable qui capturera la valeur entière de l'URL.
# Par exemple, si vous accédez à '/article/123', 'id' sera égal à 123.
@app.route('/article/<int:id>')
def afficher_article(id):
    # Cette fonction est associée à la route '/article/<int:id>'.
    # 'id' est un paramètre que vous pouvez utiliser dans la fonction.
    cur = mysql.connection.cursor()
    cur.execute("SELECT titre, contenu_article FROM articles where id = %s", (id,))
    article = cur.fetchone()
    cur.close()


    return render_template('article.html', article=article)

# Cette condition permet de s'assurer que l'application n'est exécutée que si le fichier app.py est directement exécuté (et non importé en tant que module).
if __name__ == "__main__":
    app.run(debug=True)