from app.database import get_db

class Auto:
    # Constructor de la clase Auto
    def __init__(self, autoId=None, nombre=None, marca=None, modelo=None, dominio=None, foto=None):
        self.autoId = autoId # ID del vehículo
        self.nombre = nombre # Nombre del vehículo
        self.marca = marca # Marca del vehículo
        self.modelo = modelo    # Modelo del vehículo
        self.dominio = dominio # Dominio del vehículo
        self.foto = foto    # URL de la imagen del vehículo
        
    
    # Método para guardar o actualizar un vehículo en la base de datos
    def save(self):
        db=get_db()
        cursor=db.cursor()
        if self.autoId is None:
            # Si el ID del vehículo no existe, insertarlo
            sql='INSERT INTO vehiculos (nombre, marca, modelo, dominio, foto) VALUES (%s,%s,%s,%s,%s)'
            values=(self.nombre,self.marca,self.modelo,self.dominio,self.foto)
            cursor.execute(sql,values)
            self.autoId=cursor.lastrowid
        else:
            # Si el ID del vehículo ya existe, actualizarlo
            sql='UPDATE vehiculos SET nombre=%s,marca=%s,modelo=%s,dominio=%s,foto=%s WHERE id=%s'
            values=(self.nombre,self.marca,self.modelo,self.dominio,self.foto,self.autoId)
            cursor.execute(sql,values)
        db.commit()
        cursor.close()

    # Método estatico para obtener todos los vehículo de la base de datos
    @staticmethod
    def get_all():
        db=get_db()
        cursor=db.cursor()
        cursor.execute('SELECT id, nombre, marca, modelo, dominio, foto FROM vehiculos;')
        result=cursor.fetchall()
        autos_dict={}
        for row in result:
            autoId=row[0]
            if autoId not in autos_dict: 
                autos_dict[autoId]=Auto(autoId=row[0],nombre=row[1],marca=row[2],modelo=row[3],dominio=row[4],foto=row[5])
        db.commit()
        cursor.close()
        return list(autos_dict.values())  # Devolver la lista de vehículos
    
    # Método para obtener un producto de la base de datos
    @staticmethod
    def get_by_id(autoId):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT
                v.id, v.nombre, v.marca, v.modelo, v.dominio, v.foto
            FROM
                vehiculos v
            WHERE
                v.id = %s
            """, (autoId,))
        rows = cursor.fetchall()
        cursor.close()
        if rows:
            auto_map = {}
            for row in rows:
                if row[0] not in auto_map:
                    auto_map[row[0]] = Auto(autoId=row[0], nombre=row[1], marca=row[2], modelo=row[3], dominio=row[4], foto=row[5])
            if autoId in auto_map:
                return auto_map[autoId]
            else:
                return None  # Si no se encuentra el vehículo con ese ID
        return None  # Si no se encontró ningún vehículo

    # Método para eliminar un vehículo de la base de datos
    def delete(self):
        db=get_db()
        cursor=db.cursor()
        sql='DELETE FROM vehiculos WHERE id=%s'
        values=(self.autoId,)
        cursor.execute(sql,values)
        db.commit()

    # Método para serializar un objeto Auto a un diccionario
    def serialize(self):
        return {
            'id': self.autoId,
            'nombre': self.nombre,
            'marca': self.marca,
            'modelo': self.modelo,
            'dominio': self.dominio,
            'foto': self.foto,
        }
    
    def __str__(self):
        return f'ID: {self.autoId}, Nombre: {self.nombre}, Marca: {self.marca}, Modelo: {self.modelo}, Dominio: {self.dominio}'
