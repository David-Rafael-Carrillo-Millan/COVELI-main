from .entities.Autor import Autor
from .entities.Libro import Libro

from werkzeug.utils import secure_filename


import os

import random
class ModeloLibro():

    # @classmethod
    # def listar_libros(self, db):
    #     try:
    #         cursor = db.connection.cursor()
    #         sql = """SELECT LIB.isbn, LIB.titulo, LIB.anoedicion, LIB.precio,LIB.imagen_portada,
    #                 AUT.apellidos, AUT.nombres
    #                 FROM libros LIB JOIN autor AUT ON LIB.autor_id = AUT.id
    #                 ORDER BY LIB.titulo ASC"""
    #         cursor.execute(sql)
    #         data = cursor.fetchall()
    #         libros = []
    #         for row in data:
    #             aut = Autor(0, row[5], row[6])
    #             lib = Libro(row[0], row[1],aut, row[2], row[3], row[4])
    #             libros.append(lib)
    #             # print(lib.img_portada)
    #         return libros
    #     except Exception as ex:
    #         raise Exception(ex)

    @classmethod
    def listar_libros(self, db):
        try:
            cursor = db.connection.cursor()
            # Llamada al procedimiento almacenado
            cursor.callproc('listar_libros')
            data = cursor.fetchall()

            libros = []
            libros_vendidos = []
            for row in data:
                aut = Autor(0, row[5], row[6])
                lib = Libro(row[0], row[1], aut, row[2], row[3], row[4])
                print(lib.img_portada)

                libro_v = self.verificar_libro_en_compra(db, lib.isbn)
                if libro_v:
                    libros_vendidos.append(lib.isbn)

                libros.append(lib)
            # libros.append(libros_vendidos)
            return libros, libros_vendidos
        except Exception as ex:
            raise Exception(ex)

    # @classmethod
    # def registrar_libro(self, db, libro, autor):
    #     try:
    #         titulo = libro.titulo
    #         anoedicion = libro.anoedicion
    #         precio = libro.precio
    #         apellidos = autor.apellidos
    #         nombres = autor.nombres
    #         imagen = libro.img_portada
    #         fecha = '1990-03-16'
    #
    #         #Insertar valores del autor
    #         cursor = db.connection.cursor()
    #         sql = """INSERT INTO autor (apellidos, nombres, fechanacimiento
    #                 )VALUES ('{0}', '{1}' ,'{2}')""".format(apellidos, nombres, fecha)
    #         cursor.execute(sql)
    #         db.connection.commit()
    #         autor_id = cursor.lastrowid
    #         print(autor_id)
    #         print(precio)
    #
    #         cursor = db.connection.cursor()
    #         sql = """INSERT INTO libros (isbn, titulo, autor_id, anoedicion, precio, imagen_portada
    #                 )VALUES ('{0}', '{1}' ,{2}, '{3}', '{4}', '{5}')""".format(libro.isbn, titulo, autor_id, anoedicion,
    #                 precio, imagen)
    #         cursor.execute(sql)
    #         db.connection.commit()
    #
    #         return True
    #     except Exception as ex:
    #         raise Exception(ex)

    @classmethod
    def registrar_libro(self, db, libro, autor):
        try:
            # Llamar al procedimiento almacenado
            cursor = db.connection.cursor()
            sql = "CALL registrar_libro_y_autor(%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (
                libro.isbn,
                libro.titulo,
                autor.apellidos,
                autor.nombres,
                '1990-03-16',
                libro.anoedicion,
                libro.precio,
                libro.img_portada
            ))
            db.connection.commit()
            return True
        except Exception as ex:
            db.connection.rollback()
            raise Exception(f"Error al registrar libro y autor: {ex}")

    @classmethod
    def obtener_datos_libro(self, db, isbn):

        try:
            cursor = db.connection.cursor()
            sql = "CALL obtener_libro_por_isbn(%s)"
            cursor.execute(sql, (isbn,))
            data = cursor.fetchone()  # Obtiene solo el primer registro

            libro_con_autor = {
                "isbn": data[0],
                "titulo": data[1],
                "anoedicion": data[2],
                "precio": data[3],
                "imagen_portada": data[4],
                "autor": {
                    "apellidos": data[5],
                    "nombres": data[6],
                    "id": data[7]
                }
            }

            return libro_con_autor
        except Exception as ex:
            raise Exception(ex)

        pass

    @classmethod
    def actualizar_book(self, db, libro, autor):
        try:
            titulo = libro.titulo
            anoedicion = libro.anoedicion
            precio = libro.precio
            apellidos = autor.apellidos
            nombres = autor.nombres
            imagen = libro.img_portada
            fecha = '1990-03-16'

            cursor = db.connection.cursor()
            sql = """UPDATE autor 
                     SET apellidos = '{0}', 
                         nombres = '{1}' 
                     WHERE id = {2}""".format(apellidos, nombres, autor.id)

            cursor.execute(sql)
            db.connection.commit()

            if imagen:
                cursor = db.connection.cursor()
                sql = """UPDATE libros 
                         SET titulo = '{0}', 
                             anoedicion = '{1}', 
                             precio = {2}, 
                             imagen_portada = '{3}' 
                         WHERE isbn = '{4}'""".format(titulo, anoedicion, precio, imagen, libro.isbn)
                cursor.execute(sql)
                db.connection.commit()
                return True
            else:
                cursor = db.connection.cursor()
                sql = """UPDATE libros 
                         SET titulo = '{0}', 
                             anoedicion = '{1}', 
                             precio = {2} 
                        WHERE isbn = '{3}'""".format(titulo, anoedicion, precio, libro.isbn)
                cursor.execute(sql)
                db.connection.commit()
                return True

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def borrar_book(self, db, isbn):
        try:
            cursor = db.connection.cursor()
            sql = """CALL borrar_libro(%s)"""
            cursor.execute(sql, (isbn,))
            db.connection.commit()
            return True
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def verificar_libro_en_compra(self, db, isbn):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT COUNT(*) AS total FROM compra WHERE libro_isbn = %s"
            cursor.execute(sql, (isbn,))
            resultado = cursor.fetchone()
            return resultado[0] > 0  # Devuelve True si el libro existe, False si no
        except Exception as ex:
            print(f"Error al verificar el libro: {ex}")
            return False

    @classmethod
    def leer_libro(self, db, isbn):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT isbn, titulo, anoedicion, precio 
                    FROM libros WHERE isbn = {0}""".format(isbn)
            cursor.execute(sql)
            data = cursor.fetchone()
            libro = Libro(data[0], data[1], None, data[2], data[3],None)
            return libro
        except Exception as ex:
            raise Exception(ex)

    # @classmethod
    # def borrar_book(self, db, isbn):
    #     try:
    #         cursor = db.connection.cursor()
    #         sql = """DELETE FROM libros WHERE isbn = {0}""".format(isbn)
    #         cursor.execute(sql)
    #         db.connection.commit()
    #         return True
    #     except Exception as ex:
    #         raise Exception(ex)


    @classmethod
    def listar_libros_vendidos(self, db):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT COM.libro_isbn, LIB.titulo, LIB.precio,
                    COUNT(COM.libro_isbn) AS Unidades_Vendidas
                    FROM compra COM JOIN libros LIB on COM.libro_isbn = LIB.isbn
                    GROUP BY COM.libro_isbn ORDER BY 4 DESC, 2 ASC"""
            cursor.execute(sql)
            data = cursor.fetchall()
            libros = []
            for row in data:
                lib = Libro(row[0], row[1],None, None, row[2],None)
                lib.unidades_vendidas = int(row[3])
                libros.append(lib)
            return libros
        except Exception as ex:
            raise Exception(ex)


    @classmethod
    def generar_isbn(self):
        # Prefijo de ISBN-13, comúnmente "978" o "979"
        prefijo = "978"
        # Grupo registral: Número que indica el idioma o región (generalmente 0 o 1 para países angloparlantes)
        grupo = str(random.randint(0, 1))
        # Identificador de editor: Número de longitud variable, aquí se usa un ejemplo de 5 dígitos
        editor = str(random.randint(10000, 99999))
        # Elemento de título: Número de longitud variable, aquí se usa un ejemplo de 3 dígitos
        titulo = str(random.randint(100, 999))
        # Combinar todas las partes para formar un ISBN de 12 dígitos
        isbn_12 = prefijo + grupo + editor + titulo
        return isbn_12


    @classmethod
    def allowed_file(self, filename):
        allowed_extensions_files = {'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions_files

    @classmethod
    def verificar_imagen(self, imagen, app):
        if imagen and self.allowed_file(imagen.filename):
            filename = secure_filename(imagen.filename)
            imagen_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            imagen.save(imagen_path)
            return  filename
        else:
            return None
