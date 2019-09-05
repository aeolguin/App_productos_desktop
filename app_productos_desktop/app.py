from tkinter import ttk
from tkinter import *

import mysql.connector
#Conexion a la base de datos
mydb = mysql.connector.connect(
        host="localhost",
        user="ariel1",
        passwd="martina2712",
        database="database"
        )
mydbcursor = mydb.cursor()


class Productos:

    def __init__ (self, window):
        self.wind = window
        self.wind.title("Aplicacion de Productos")

        #Creamos un contenedor frame
        frame = LabelFrame(self.wind, text = 'Registre un Nuevo Producto')
        frame.grid(row = 1, column = 0, columnspan = 3, pady = 20)

        #Creamos un imput con el nombre del producto
        Label(frame, text = 'Nombre: ').grid(row = 2, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 2, column = 1)

        #Creamos un imput con el precio del producto
        Label(frame, text = 'Precio: ').grid(row = 3, column = 0)
        self.price = Entry(frame)
        self.price.grid(row = 3, column = 1)

        #Creamos el boton de Salvar
        ttk.Button(frame, text = 'Salvar Producto', command = self.add_product).grid(
            row = 4, columnspan = 2, sticky = W + E)

        #Mensaje de salida
        self.mensaje = Label(text = '', fg = 'blue')
        self.mensaje.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

        #Creamos una vista de tabla
        self.tree = ttk.Treeview(height = 10, column = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Nombre', anchor = CENTER)
        self.tree.heading('#1', text = 'Precio', anchor = CENTER)
        
        #Llenando las filas de la tabla
        self.get_pructs()

        #Botones de actualizar y eliminar
        ttk.Button(text = 'Eliminar Producto', command = self.del_product).grid(row = 5, column = 0, sticky = W + E)
        ttk.Button(text = 'Editar Producto', command = self.edit_product).grid(row = 5, column = 1, sticky = W + E)

    #Funcion de Consulta a la Base de datos
    def run_query(self, query, parameters = ()):
        mydbcursor.execute(query, parameters)
        result = mydbcursor.fetchall()
        return result
    
    #funcion de Insert de datos en la Base de datos
    def run_add(self, query, parameters = ()):
         mydbcursor.execute(query, parameters)
         mydb.commit()
   
    def get_pructs(self):
        #borramos todos los datos de la tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        
        #consulta de datos
        query = 'SELECT * from producto ORDER BY nombre DESC'
        db_rows = self.run_query(query)
        
        #Mostrando los datos en la tabla
        for row in db_rows:
            self.tree.insert('', 0, text = row[1], value = row[2])
        
    #funcion de validacion de datos
    def validation(self):
        return len(self.name.get()) != 0 and len(self.name.get()) != 0

    #funcion de agragar producto
    def add_product(self):
        if self.validation():
            val1 = self.name.get()
            val2 = self.price.get()
            query = 'INSERT INTO producto(nombre,precio) VALUES(%s, %s)'
            parameters = (f'{val1}', f'{val2}')
            self.run_add(query, parameters)
            self.mensaje['text'] = 'El producto {} fue agregado correctamente'.format(
                self.name.get()
            )
            self.name.delete(0, END)
            self.price.delete(0, END)
        else:
            self.mensaje['text'] = 'El nombre y el precio es requerido'
        self.get_pructs()

    #Funcion de Eliminar un producto
    def del_product(self):
        self.mensaje['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor selecciona un ítem de la lista'
            return
        self.mensaje['text'] = ''
        parameters = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM producto WHERE producto.nombre = %s'
        self.run_add(query, (parameters, ))
        self.mensaje['text'] = 'El producto {} fue eliminado correctamente'.format(parameters)
        self.get_pructs()

    #Funcion de editar producto
    def edit_product(self):
        self.mensaje['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor selecciona un ítem de la lista'
            return
        




if __name__ == '__main__':
    window = Tk()
    application = Productos(window)
    window.mainloop()

