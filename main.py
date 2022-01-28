from flask import Flask, render_template, request, redirect, url_for
import sqlalchemy
import db
from models import Tarea

app = Flask(__name__)

# La barra (el slash) se conoce como la página de inicio (página home).
# Vamos a definir para esta ruta, el comportamiento a seguir.


@app.route('/')
def home():
    todas_las_tareas = db.session.query(Tarea).all() #Consultamos y almacenamos todas las tareas de la base de datos
    try:
        progreso_query = db.session.query(Tarea).filter_by(hecha=True).count()*100/len(todas_las_tareas)
    except:
        progreso_query = 0 #En caso de ZeroDivision Exception, asignar variable progreso_query a 0
    return render_template("index.html",lista_de_tareas=todas_las_tareas,count=len(todas_las_tareas),progreso=round(progreso_query)) #cargamos template index.html


@app.route('/crear-tarea', methods=['POST'])
def crear():
    #tarea es un objeto de la clase tarea
    tarea = Tarea(contenido=request.form['contenido_tarea'], hecha=False) #parametro contenido usa el método form de la clase request de la libreria flask pasando como parametro el input de la pagina
    db.session.add(tarea) #añadir objeto tarea a la base de datos
    db.session.commit() #Ejecutar commit en la base de datos
    return redirect(url_for('home')) #Crear tarea y redireccionar a home


@app.route('/tarea-hecha/<id>')
def hecha(id):
    tarea = db.session.query(Tarea).filter_by(id=int(id)).first() #Se obtiene la tarea que se busca
    tarea.hecha=not(tarea.hecha) #guardamos en el atributo hecha del onjeto tarea la variable booleana su contrario.
    db.session.commit()
    return redirect(url_for('home')) #Volver a home luego de cambiar el estado de la tarea


@app.route('/eliminar-tarea/<id>')
def eliminar(id):
    tarea = db.session.query(Tarea).filter_by(id=int(id)).delete()#Buscar dentro de la base de datos el registro que coincida con el id, cuando se encuantra lo elimina
    db.session.commit()
    return redirect(url_for('home')) #Volver a home con la tarea eliminada


if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine) #Se crea el modelo de datos
    app.run(debug=True)


