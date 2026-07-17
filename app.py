from flask import Flask,render_template,request,jsonify
import sqlite3,random
app=Flask(__name__)
DB="products.db"

def conn():
    return sqlite3.connect(DB)

def init():
    c=conn()
    c.execute("CREATE TABLE IF NOT EXISTS Products(Product_Name TEXT UNIQUE,Stock_On_Hand INTEGER)")
    c.commit();c.close()
init()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate",methods=["POST"])
def generate():
    c=conn();cur=c.cursor()
    cur.execute("DELETE FROM Products")
    for i in range(1,51):
        cur.execute("INSERT INTO Products VALUES(?,?)",(f"Item {i}",random.randint(20,50)))
    c.commit();c.close()
    return jsonify(success=True)

@app.route("/products")
def products():
    page=int(request.args.get("page",1))
    per=20
    off=(page-1)*per
    c=conn();cur=c.cursor()
    rows=cur.execute("SELECT Product_Name,Stock_On_Hand FROM Products LIMIT ? OFFSET ?",(per,off)).fetchall()
    total=cur.execute("SELECT COUNT(*) FROM Products").fetchone()[0]
    c.close()
    return jsonify(data=[{"name":r[0],"stock":r[1]} for r in rows],pages=(total+per-1)//per)

@app.route("/sort-name",methods=["POST"])
def sort_name():
    c=conn();cur=c.cursor()
    rows=cur.execute("SELECT Product_Name,Stock_On_Hand FROM Products").fetchall()
    rows.sort(key=lambda x:int(x[0].split()[1]))
    cur.execute("DELETE FROM Products")
    cur.executemany("INSERT INTO Products VALUES(?,?)",rows)
    c.commit();c.close()
    return jsonify(success=True)

@app.route("/sort-stock",methods=["POST"])
def sort_stock():
    c=conn();cur=c.cursor()
    rows=cur.execute("SELECT Product_Name,Stock_On_Hand FROM Products").fetchall()
    rows.sort(key=lambda x:x[1],reverse=True)
    cur.execute("DELETE FROM Products")
    cur.executemany("INSERT INTO Products VALUES(?,?)",rows)
    c.commit();c.close()
    return jsonify(success=True)

@app.route("/reduce",methods=["POST"])
def reduce():
    c=conn();c.execute("UPDATE Products SET Stock_On_Hand=MAX(Stock_On_Hand-2,0)")
    c.commit();c.close()
    return jsonify(success=True)

@app.route("/increase",methods=["POST"])
def increase():
    c=conn();cur=c.cursor()
    rows=cur.execute("SELECT Product_Name,Stock_On_Hand FROM Products").fetchall()
    for n,s in rows:
        if int(n.split()[1])%2==0:
            cur.execute("UPDATE Products SET Stock_On_Hand=? WHERE Product_Name=?",(s+2,n))
    c.commit();c.close()
    return jsonify(success=True)

if __name__=="__main__":
    app.run(debug=True)
