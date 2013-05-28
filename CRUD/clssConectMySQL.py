# coding: UTF-8 
# Python Version: 2.7.3
# Fichero: clssConectMySQL_FJBecerra.py
# Versión: 2.0
# Ejercicio: Ejercicio 1 - Programación Avanzada - Víctimas de... 
# Curso: Programación avanzada en Python
# Centro: CEVUG
# Autor: Fco. J. Becerra
# email: fjbecerr@gmail.com
# Fecha: 23/05/2013
# Operativa: Crea una clase para conectar a una base de datos MySQL

import MySQLdb #Importar libreria

# Clase: clssConectMySQL
# Uso: Clase para operación de conexión a MySQL
class clssConectMySQL:
    
    # Constructor
    # since :    1.0
    # Estado [D]esarrollo/[O]perativa: D    
    # author :
    # uso :     Asigna los parámetros para una conexión y una query
    # param :   
    #   ConectData=[] -> Parámentros de la conexión
    # return :  False / True (Error Conexión / Correcta)        
    def __init__(self,ConectData=[]):
        """Realiza la conexión a una BBDD MySQL. Toma como parametros
        los datos de conexión con lista [Host,DB,User,Password,Tabla]."""
        self.__version__ = "2.0" # Versión Activa
        # Comprobar el número de elementos
        # Estableciendo parametros de conexion
        self.Myhost = ConectData[0]
        self.Mydb = ConectData[1]
        self.Myuser = ConectData[2]
        self.Mypassw = ConectData[3]
        self.MyTabla = ConectData[4]
        self.MyQuery = " "
        self.MyID = 0 # Valor inicial
        self.MyNewR = False # Controla si estamos insertando un registro
        # Descripcion: Establece una conexión MySQL
        self.MyConexion = MySQLdb.connect(host=self.Myhost, user=self.Myuser, passwd=self.Mypassw, db=self.Mydb)       
         

    # Función:  func_Desconectar
    # author :
    # Estado [D]esarrollo/[O]perativa: O    
    # since :   1.0
    # uso   :   Desconectar la conexión
    def func_Desconectar(self):
        self.MyConexion.close()

    
    # Función:  func_DesconectarCursor
    # author :
    # Estado [D]esarrollo/[O]perativa: O    
    # since :   1.0             
    # uso   :   Desconecta un cursor
    def func_DesconectarCursor(self):
        self.MyCursor.close();  

    
    # Función:  func_EstablecerCursor
    # author :
    # Estado [D]esarrollo/[O]perativa: O    
    # since :   1.0             
    # uso   :   Activa un cursor para nuestra conexión
    # param :   iTipoCursor -> Entero permite especificar el tipo   
    def func_EstablecerCursor(self, iTipoCursor):
        if iTipoCursor == 1: # Cursor con DictCursor            
            self.MyCursor = self.MyConexion.cursor(MySQLdb.cursors.DictCursor)                    
        else: # Cursor standard            
            self.MyCursor = self.MyConexion.cursor()        

    
    # Función:  func_Insertar
    # author :
    # Estado [D]esarrollo/[O]perativa: O    
    # since :   1.0         
    # uso   :   Genera una consulta INSERT
    # param :
    #       SQLTabla - Tabla sobre la que insertaremos
    #       SQLCampos - Lista de campos de la operación
    #       SQLDatos - Datos asignados a los campos 
    # return :  handlers
    def func_Insertar(self, SQLTabla, SQLCampos = [], SQLDatos = []):
        """Genera una query INSERT... Se le pasan: el nombre de la tabla, 
        los nombres de campos como una lista y los datos como otra lista."""
        self.MyNewR = True # Nuevo registro en inserción
        self.MyQuery = "INSERT INTO " + SQLTabla + "("        
        # Ajustar el formato a un query añadiendo comillas "" y comas "," a los campos
        CamposMyQuery = self.func_ComponerSQL(SQLCampos,0)
        ValoresMyQuery = self.func_ComponerSQL(SQLDatos,1)

        # Componer los campos de la consulta
        for campo in CamposMyQuery:
            self.MyQuery += campo
        self.MyQuery += ")"
        
        # Componer los valores de los campos de la consulta
        self.MyQuery += " VALUES ("
        for campo in ValoresMyQuery:
            self.MyQuery += campo
        self.MyQuery += ");"


    # Función:  func_Insertar_Basic
    # author :
    # Estado [D]esarrollo/[O]perativa: O    
    # since :   2.0         
    # uso   :   Genera una consulta INSERT
    # param :
    #       SQLDatos - Datos asignados a los campos 
    def func_Insertar_Basic(self, SQLDatos = []):
        """Genera una query INSERT... Se le pasan: los datos como lista. Inserta en la BBDD de prueba"""
        self.MyNewR = True # Nuevo registro en inserción
        self.MyQuery = "INSERT INTO " + self.MyTabla + "("        
        # Ajustar el formato a un query añadiendo comillas "" y comas "," a los campos
        CamposMyQuery = ["id","Tematica","Titulo","Formato","Paginas","Puntuacion"]
        CamposMyQuery = self.func_ComponerSQL(CamposMyQuery,0)
        ValoresMyQuery = self.func_ComponerSQL(SQLDatos,1)

        # Componer los campos de la consulta
        for campo in CamposMyQuery:
            self.MyQuery += campo
        self.MyQuery += ")"
        
        # Componer los valores de los campos de la consulta
        self.MyQuery += " VALUES ("
        for campo in ValoresMyQuery:
            self.MyQuery += campo
        self.MyQuery += ");"

        
    # Función:  func_ComponerSQL
    # author :
    # Estado [D]esarrollo/[O]perativa: O    
    # since :   1.0             
    # uso   :   Añade las "" y "," necesarias a los elementos de una consulta
    # param :
    #   Campos - Campos o Valores que queremos formatear
    #   Campo_o_Valor - Vale 0 cuando para formatear campos (sólo añade "," como separador)
    #                   Vale 1 cuando para formatear valores (añade "" y ",")   
    # return :  La lista con los campos adaptados a SQL
    def func_ComponerSQL(self, Campos = [], Campo_o_Valor = 0):
        """Realiza el formateo de una lista para ajustarla a la sintaxis SQL."""
        camposTemp = [] # Temporal para la composición
        campoTemp = ""  # Temporal para la composición
        ultimoCampo = False # Detecta si alcanzamos el último campo
        longitud = 0 # Controlar el nº de campos en operación
        # Añadir las comillas
        for campo in Campos:
            if str(type(campo)) == "<type \'str\'>" and Campo_o_Valor == 1:
                campoTemp = "\"" + campo + "\""
            else:
                campoTemp = str(campo) # No añadimos ajuste, campos no str (numérico)
            
            # Existen varios campos y no estamos en el último
            if len(Campos)>0 and ultimoCampo == False: 
                campoTemp += ","
                longitud = longitud + 1 # Sumar el campo al control
                if longitud == len(Campos) - 1: # Ultimo campo? no añade la ","
                    ultimoCampo = True # Pasar del campo inicial
         
            camposTemp.append(campoTemp) # Añadimos al temporal
                
        return camposTemp       

    
    # Función:  func_Seleccionar
    # author :
    # Estado [D]esarrollo/[O]perativa: O    
    # since :   1.0             
    # uso   :   Formatea una consulta de selección
    # param :           
    # Parámetros: 
    #       SQLTabla - Tabla para la consulta
    #       SQLCampos - Lista de campos de la operación
    #       SQLWhere - Condición
    def func_Seleccionar(self, SQLTabla, SQLCampos, SQLWhere):
        """Compone una query SELECT... Se la pasan: el nombre de la tabla, 
        los campos y la condición de WHERE."""
        self.MyNewR = False # Registro en selección
        self.MyQuery = "SELECT " + SQLCampos
        self.MyQuery += " FROM " + SQLTabla
        self.MyQuery += " WHERE " + SQLWhere
        self.MyQuery += ";"


    # Función:  func_HacerCommit
    # author :
    # Estado [D]esarrollo/[O]perativa: O    
    # since :   1.0         
    # uso   :   Realizar un commit de la conexión
    def func_HacerCommit(self):
        self.MyConexion.commit() # Actualizar

    
    # Función:  func_ExecSQL
    # author :
    # Estado [D]esarrollo/[O]perativa: O    
    # since :   1.0             
    # uso   :   Ejecutar una consulta
    def func_ExecSQL(self):
        self.MyCursor.execute(self.MyQuery)

    
    # Función:  func_MostrarDatos
    # author :
    # Estado [D]esarrollo/[O]perativa: O    
    # since :   1.0             
    # uso   :   Mostrar una consulta SELECT
    def func_MostrarDatos(self):
        """Muestra los registros apuntados por un cursor."""
        registroTemp= self.MyCursor.fetchone()
        while registroTemp != False and registroTemp != None:
            print registroTemp
            registroTemp= self.MyCursor.fetchone() # Siguiente registro 


    # Función:  func_MostrarDatosCol
    # author :
    # Estado [D]esarrollo/[O]perativa: O    
    # since :   1.0             
    # uso   :   Mostrar datos formateados 
    def func_MostrarDatosCol(self):
        """Muestra en columnas los datos apuntados por el cursor."""
        registrosTemp = self.MyCursor.fetchall()
        nregistrosTemp = self.MyCursor.rowcount 
        regCabecera = True
        for registroTemp in registrosTemp:

            if regCabecera == True: # Mostar la cabecera para el listado
                print " "
                print "\n Resultado de la consulta : "+ str(nregistrosTemp)
                print "-----------------------------------------------------------------"
                regCabecera = False
            
            print str(registroTemp["id"])+ " - " + registroTemp["Nombre"]+ " - " +registroTemp["Profesion"]+ " - " +registroTemp["Muerte"]

    
    # Función:  func_ControlarID
    # author :
    # Estado [D]esarrollo/[O]perativa: O    
    # since :   1.0
    # update:   1.9
    # uso   :   Devolver siguiente valor de ID
    # param : Incrementar - Indica si incrementar o no el Id
    # return :  Valor calculado del nuevo ID
    def func_ControlarID(self, Incrementar = False):
        """Devuelve un ID para un campo clave. Si no existe ningún registro previo 
        los genera, si existen registros previos toma el mayor valor y lo aumenta."""
        SQLTemp = "SELECT * FROM "+ self.MyTabla+" WHERE 1 ORDER BY ID DESC;"
        self.MyCursor.execute(SQLTemp)
        # registrosTemp = self.MyCursor.fetchall()[-1:]
        registrosTemp = self.MyCursor.fetchone()
        nregistrosTemp = self.MyCursor.rowcount
        if nregistrosTemp == 0 : # No hay registros y se genera el índice desde 0
           self.MyID += 1 # Usar un variable para inicializar la tabla          
        else: # Hay registros previos            
           self.MyID = registrosTemp[0]                       
           self.MyID += 1           

        # Devolver el actual
        if Incrementar == False:
            if nregistrosTemp > 1:
              self.MyID = self.MyID - 1   

        return self.MyID


    # Función:  func_BorrarRegs
    # author :
    # Estado [D]esarrollo/[O]perativa: O    
    # since :   1.0             
    # uso   :   Eliminar los registros actuales
    def func_BorrarRegs(self):
        """Realiza un DELETE sobre una tabla."""
        SQLTemp = "DELETE FROM " + self.MyTabla+ ";"
        self.MyCursor.execute(SQLTemp)


    # Función:  func_DatosTest
    # author :
    # Estado [D]esarrollo/[O]perativa: O    
    # since :   1.0             
    # uso   :   Insertar una serie de datos para pruebas
    # param :   nReg - Número de registro que insertaremos
    def func_DatosTest(self, nReg):
        """Genera registros en número igual al argumento pasado."""
        for n in range(nReg):
             # Asignamos los valores para la consulta
            self.MyNewR = True # Nuevos registros en inserción
            SQLCampos = "id", "Nombre", "Profesion", "Muerte"
            SQLDatos = self.func_ControlarID(), "Zombies"+str(n),"Muertos Vivientes"+str(n),"Desmembramiento a espada"+str(n)
            self.func_Insertar(self.MyTabla, SQLCampos, SQLDatos)
            self.func_ExecSQL()


    # Función:  func_ComprobarDatos
    # author :
    # Estado [D]esarrollo/[O]perativa: O    
    # since :   1.0             
    # uso   :   Controlar la integridad de los campos datos antes de usarlos en la query
    # param :   SQLDato - Lista de los datos para la query          
    # return :  False / True si el campo está vacío
    def func_ComprobarDatos(self,SQLDatos = []):
        """Comprueba que no se pasen valores vacíos en campos. Los datos se 
        pasan como una lista."""
        campoVacio = False
        for n in range(len(SQLDatos)):
            if len(str(SQLDatos[n]))==0:
                campoVacio = True

        return campoVacio        

            
    # Función:  func_RecuperarTablas
    # author :
    # Estado [D]esarrollo/[O]perativa: D   
    # since :   1.7             
    # uso   :   Listar las tablas disponibles
    # return :  Devuelve una Lista con las tablas disponibles
    def func_RecuperarTablas(self):
        """Muestra las tablas disponibles en una BBDD. Devuelve una lista
        con las tablas disponibles"""
        TablasSQL = []
        self.MyCursor.execute('SHOW TABLES;') # Pasar las tablas al cursor
        for TablasTemp in self.MyCursor:
            for TablaTemp in TablasTemp:
                TablasSQL.append(TablaTemp) # Añadir cada tabla
            
        TablasSQL.sort() # Ordenar
        return TablasSQL

		
    # Función:  func_CrearTabla
    # author :
    # Estado [D]esarrollo/[O]perativa: D   
    # since :   1.8             
    # uso   :   Listar las tablas disponibles
    # param :   
    #	Tabla - Nombre de la nueva tabla
    #	SQLScript - Definición de los campos
    # return :  False / True (Error/Correcto)
    def func_CrearTabla(self, Tabla, SQLScript):
        """Crear una nueva tabla en la base de datos. Se le pasa el nombre
	de la nueva tabla y los campos. Ejemplo:
	func_CrearTabla(TablaPrueba","id INT, Nombre VARCHAR(100),DNI VARCHAR(20)").
	Si se pasan los datos vacíos creara una tabla de manera automática."""
        if len(Tabla) == 0 or len(SQLScript) == 0:
            Tabla = "BIBLIOTECA_TESTER"
            SQLTemp = "CREATE TABLE BIBLIOTECA_TESTER ("
            SQLTemp += "id INT, Tematica VARCHAR(50), Titulo VARCHAR(50), "
            SQLTemp += "Formato VARCHAR(50), Paginas INT, Puntuacion INT"
            SQLTemp += "); "      
        else:    
            SQLTemp = "CREATE TABLE " + Tabla + " ("
            SQLTemp += SQLScript + "); "
        try:
            self.MyCursor.execute(SQLTemp)
            self.MyConexion.commit() # Actualizar
            self.MyTabla = Tabla
            return True
        except:
            return False

            
    # Función:  func_CargarRegistroInicial
    # author :
    # Estado [D]esarrollo/[O]perativa: D   
    # since :   1.8
    # update : 2.0
    # uso   :   "Devuelve el valor de un registro SQL en forma de Lista
    # param : nIdTemp - Número ID del registro solicitado
    # return :  Un registro en forma de lista    
    def func_CargarRegistroInicial(self, nIdTemp = 0):
        """Devuelve el valor de un registro SQL en forma de Lista"""
        self.CamposInterfaz = []        
        self.MyNewR = False # Registro en selección
        SQLTemp = "SELECT * FROM "+ self.MyTabla

        # Localizar el primer registro independientemente del ID
        if nIdTemp > 0:
            SQLTemp += " WHERE Id =" +str(nIdTemp)+ " ORDER BY ID;"            
        else:
            SQLTemp += " ORDER BY ID;"
        try:
            self.MyCursor.execute(SQLTemp)
            #self.func_MostrarDatos()
            RegistroTemp = self.MyCursor.fetchone()
            if RegistroTemp != False and RegistroTemp[0] != None:                
                for CampoTemp in RegistroTemp: # Pasar los datos del registro
                    self.CamposInterfaz.append(CampoTemp)
        except:
            # Pasar una valores por defecto
            self.CamposInterfaz = [0,"Ningun registro","Ningun registro","Ningun registro",0,0]
        
        return self.CamposInterfaz

        
        
