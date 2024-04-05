import pytest
from enum import Enum

class Persona:

    def __init__(self, nombre, dni, direccion, sexo):
        self.nombre = nombre
        self.dni = dni
        self.direccion = direccion
        if sexo not in ['V', 'M', 'OTRO']:
            raise Exception("El sexo debe ser 'V', 'M' u 'OTRO'")
        self.sexo = sexo

class PeriodoAsignatura(Enum):
    CUATRIMESTRE_1 = 1
    CUATRIMESTRE_2 = 2
    ANUAL = 3

class Asignatura:
    def __init__(self, id, nombre, grado, creditos, tipo):
        self.id = id
        self.nombre = nombre
        self.grado = grado
        self.creditos = creditos
        if not isinstance(tipo, PeriodoAsignatura):
            raise ValueError('Tipo debe ser un valor entre 1 y 3')
        self.tipo = tipo
        self.estudiantes_matriculados = []
        self.profesores = []

    def añadir_estudiantes(self, estudiante):
        self.estudiantes_matriculados.append(estudiante)
    
    def eliminar_estudiantes(self, estudiante):
        self.estudiantes_matriculados.remove(estudiante)
    
    def añadir_profesor(self, profesor):
        self.profesores.append(profesor)
    
    def eliminar_profesor(self, profesor):
        self.profesores.remove(profesor)

    def __str__(self):
        return f"Asignatura: {self.nombre}\nGrado: {self.grado}\nCréditos: {self.creditos}\nPeriodo: {str(self.tipo)}"

class Estudiante(Persona):

    def __init__(self, nombre, dni, direccion, sexo, grado, curso):
        super().__init__(nombre, dni, direccion, sexo)
        self.grado = grado
        self.curso = curso
        self.creditos_completados = 0
        self.asignaturas_completadas = [] # [(asignatura1, calificacion1), (asignatura2, calificacion2)....]
        self.asignaturas_cursando = []    # [asignatura1, asignatura2, ...]

    def añadir_asignatura_aprobada(self, asignatura, calificacion):
        self.asignaturas_completadas.append((asignatura.nombre, calificacion))
    
    def añadir_asignatura_matriculada(self, asignatura):
        self.asignaturas_cursando.append(asignatura)
    
    def eliminar_asignatura_matriculada(self, asignatura):
        self.asignaturas_cursando.remove(asignatura)

    def __str__(self):
        return f"Estudiante: {self.nombre}\nDNI: {self.dni}\nDirección: {self.direccion}\nSexo: {self.sexo}\nGrado: {self.grado}\nCurso: {self.curso}\n"

    
class TipoDepartamento(Enum):
    DIIC = 1
    DITEC = 2
    DIS = 3

    def __str__(self):
        return self.name # A la hora de imprimir, devuelve el nombre del departamento como "str"

## PODREMOS CAMBIAR PARA PODER IMPRIMIR DEPARTAMENTO???

class MiembroDepartamento(Persona):

    def __init__(self, nombre, dni, direccion, sexo, departamento):
        super().__init__(nombre, dni, direccion, sexo)
        if not isinstance(departamento, TipoDepartamento):
            raise ValueError('El departamento debe ser uno de los tres definidos(DIIC, DITEC, DIS)')
        self.departamento = departamento

    def cambio_dep(self, nuevo_departamento):
        self.departamento = nuevo_departamento

    def __str__(self):
        return f'Nombre: {self.nombre}\nDNI: {self.dni}\nDirección: {self.direccion}\nSexo: {self.sexo}\n'
        # No se incluye el nombre del departamento en el método 'str' por el tipo de base de datos en el que se añade
        # como clave el departamento y como valor la lista de miembros, provocando que el departamento aparezca de forma
        # duplicada


class ProfesorAsociado(MiembroDepartamento):
    def __init__(self, nombre, dni, direccion, sexo, departamento):
        super().__init__(nombre, dni, direccion, sexo, departamento)
        self.asignaturas_a_impartir = {}

    def añadir_asignatura_a_impartir(self, asignatura):
        if asignatura.grado not in self.asignaturas_a_impartir:
            self.asignaturas_a_impartir[asignatura.grado] = []  # Si el grado no está en el diccionario, añade una lista vacía
        self.asignaturas_a_impartir[asignatura.grado].append(asignatura.nombre)  # Añade la asignatura a la lista de ese grado

    def eliminar_asignatura_a_impartir(self, asignatura):
        if asignatura.grado in self.asignaturas_a_impartir and asignatura.nombre in self.asignaturas_a_impartir[asignatura.grado]:
            self.asignaturas_a_impartir[asignatura.grado].remove(asignatura.nombre)  # Elimina la asignatura de la lista de ese grado
            if not self.asignaturas_a_impartir[asignatura.grado]:  # Si la lista de ese grado está vacía, elimina el grado del diccionario
                del self.asignaturas_a_impartir[asignatura.grado]

    def __str__(self):
        return f'Nombre: {self.nombre}\nDNI: {self.dni}\nDirección: {self.direccion}\nSexo: {self.sexo}\n'



class ProfesorTitular(MiembroDepartamento):
    def __init__(self, nombre, dni, direccion, sexo, departamento, area_investigacion):
        super().__init__(nombre, dni, direccion, sexo, departamento)
        self.asignaturas_a_impartir = {}
        self.area_investigacion = area_investigacion

    def añadir_asignatura_a_impartir(self, asignatura):
        if asignatura.grado not in self.asignaturas_a_impartir:
            self.asignaturas_a_impartir[asignatura.grado] = []  # Si el grado no está en el diccionario, añade una lista vacía
        self.asignaturas_a_impartir[asignatura.grado].append(asignatura.nombre)  # Añade la asignatura a la lista de ese grado

    def eliminar_asignatura_a_impartir(self, asignatura):
        if asignatura.grado in self.asignaturas_a_impartir and asignatura.nombre in self.asignaturas_a_impartir[asignatura.grado]:
            self.asignaturas_a_impartir[asignatura.grado].remove(asignatura.nombre)  # Elimina la asignatura de la lista de ese grado
            if not self.asignaturas_a_impartir[asignatura.grado]:  # Si la lista de ese grado está vacía, elimina el grado del diccionario
                del self.asignaturas_a_impartir[asignatura.grado]

    def __str__(self):
        return f'Nombre: {self.nombre}\nDNI: {self.dni}\nDirección: {self.direccion}\nSexo: {self.sexo}\nÁrea de investigación: {self.area_investigacion}\n'

class Investigador(MiembroDepartamento):
    def __init__(self, nombre, dni, direccion, sexo, departamento, area_investigacion):
        super().__init__(nombre, dni, direccion, sexo, departamento)
        self.area_investigacion = area_investigacion

    def __str__(self):
        return f'Nombre: {self.nombre}\nDNI: {self.dni}\nDirección: {self.direccion}\nSexo: {self.sexo}\nÁrea de investigación: {self.area_investigacion}\n'

class Universidad:

    def __init__(self, nombre, ciudad, codpostal, estudiantes = None, investigadores=None, profesores=None, asignaturas=None, miembros_dep=None):
        self.nombre = nombre
        self.ciudad = ciudad
        self.codpostal = codpostal
        self.estudiantes = estudiantes if estudiantes is not None else []
        self.profesores = profesores if profesores is not None else []
        self.investigadores = investigadores if investigadores is not None else []
        self.asignaturas = asignaturas if asignaturas is not None else []
        self.miembros_dep = miembros_dep if miembros_dep is not None else {} # NOS SERVIRA PARA MOSTRAR UNA LISTA DE MIEMBROS PERTENENECIENTES A CADA DEPARTAMENTO

# Los métodos de búsqueda se podrán como privados ya que servirán sólamente de apoyo

    def __buscar_estudiante(self, dni):
        for estudiante in self.estudiantes:
            if dni == estudiante.dni:
                return estudiante
        return "DNI no coincide"
    
    def __buscar_profesor(self, dni):
        for profesor in self.profesores:
            if dni == profesor.dni:
                return profesor
        return "DNI no coincide"
    
    def __buscar_investigador(self, dni):
        for investigador in self.investigadores:
            if dni == investigador.dni:
                return investigador
        return "DNI no coincide"

    def __buscar_asignatura(self, id):
        for asignatura in self.asignaturas:
            if id == asignatura.id:
                return asignatura
        return "Asignatura no encontrada"


    def añadir_miembro_dep(self, dni):
        miembro = self.__buscar_profesor(dni)

        if miembro == "DNI no coincide":
            miembro = self.__buscar_investigador(dni)

        if miembro != "DNI no coincide":
            if miembro.departamento not in self.miembros_dep:
                self.miembros_dep[miembro.departamento] = []
            self.miembros_dep[miembro.departamento].append(miembro)
        else:
            return "DNI no coincide"
    
    def eliminar_miembro_dep(self, dni):
        miembro = self.__buscar_profesor(dni)

        if miembro == "DNI no coincide":
            miembro = self.__buscar_investigador(dni)

        if miembro != "DNI no coincide":
            self.miembros_dep[miembro.departamento].remove(miembro)
        # Como el número de departamentos es fijo, aunque se quede sin miembros, no desaparecerá el departamento
        else:
            return "DNI no coincide"
    
    def insertar_estudiante(self, nombre, dni, direccion, sexo, grado, curso):
        estudiante = Estudiante(nombre, dni, direccion, sexo, grado, curso)
        self.estudiantes.append(estudiante)
    
    def insertar_prof_asociado(self, nombre, dni, direccion, sexo, departamento):
        prof_asoc = ProfesorAsociado(nombre, dni, direccion, sexo, departamento)
        self.profesores.append(prof_asoc)
        self.añadir_miembro_dep(prof_asoc.dni)
    
    def insertar_prof_titular(self, nombre, dni, direccion, sexo, departamento, area_investigacion):
        prof_titular = ProfesorTitular(nombre, dni, direccion, sexo, departamento, area_investigacion)
        inves = Investigador(nombre, dni, direccion, sexo, departamento, area_investigacion)
        self.profesores.append(prof_titular)
        self.investigadores.append(inves)
        self.añadir_miembro_dep(prof_titular.dni)

    def insertar_investigador(self, nombre, dni, direccion, sexo, departamento, area_investigacion):
        inves = Investigador(nombre, dni, direccion, sexo, departamento, area_investigacion)
        self.investigadores.append(inves)
        self.añadir_miembro_dep(inves.dni)
    
    def insertar_asignatura(self, id, nombre, grado, creditos, tipo):
        assert tipo in PeriodoAsignatura, "Tipo de asignatura inválido, la asignatura debe ser anual o cuatrimestral (primer o segundo cuatrimestre)"
        asignatura = Asignatura(id, nombre, grado, creditos, tipo)
        self.asignaturas.append(asignatura)

    def cambio_departamento(self, dni, nuevo_departamento):
        assert nuevo_departamento in TipoDepartamento, "Departamento inválido, el departamento debe ser uno de los tres definidos (DIIC, DITEC, DIS)"
        miembro = self.__buscar_profesor(dni)
        if miembro == "DNI no coincide":
            miembro = self.__buscar_investigador(dni)
            
        
        if miembro != "DNI no coincide":
            self.eliminar_miembro_dep(miembro.dni)  # Eliminamos al miembro de su antiguo dep
            miembro.cambio_dep(nuevo_departamento) # Actualizamos info nuevo dep
            self.añadir_miembro_dep(miembro.dni)  # Añadimos el miembro al nuevo departamento
            return f"{miembro.nombre} se ha cambiado al departamento {miembro.departamento}"
        else:
            return "DNI no coincide"


    def eliminar_estudiante(self, dni):
        estudiante = self.__buscar_estudiante(dni)
        if estudiante is not None:
            self.estudiantes.remove(estudiante)
            for asignatura in estudiante.asignaturas_cursando:
                asignatura.eliminar_estudiantes(estudiante)

    def eliminar_profesor(self, dni):
        prof = self.__buscar_profesor(dni)
        inves = self.__buscar_investigador(dni)

        if prof is not None:
            self.profesores.remove(prof)
            self.eliminar_miembro_dep(dni)
            for asignatura in prof.asignaturas_a_impartir:
                asignatura.eliminar_profesor(prof)

        if inves is not None and inves != prof:  # Asegurarse de que no se utiliza el mismo objeto, nos permitirá 
            try:                                  # tratar cuando tratamos de eliminar un P.titular, también lo borramos como investigador.
                self.investigadores.remove(inves)
            except ValueError:
                print(f"DNI no coincide")


    def eliminar_investigador(self, dni):
        inves = self.__buscar_investigador(dni)
        if inves is not None:
            self.investigadores.remove(inves)
            self.eliminar_miembro_dep(dni)
    
    def añadir_asignatura_a_cursar(self, dni, id_asig):
        asignatura = self.__buscar_asignatura(id_asig)
        estudiante = self.__buscar_estudiante(dni)
        if len(estudiante.asignaturas_cursando) > 12:
            raise ValueError('No se pueden cursar más de 12 asignaturas al mismo tiempo.')
        estudiante.añadir_asignatura_matriculada(asignatura)
        asignatura.añadir_estudiantes(estudiante)
        print(f"{estudiante.nombre} se ha matriculado en la asignatura de {asignatura.nombre}\n")

    def aprobar_asignatura(self, dni, id_asig, calificacion):
        if calificacion < 5:
            raise ValueError('La asignatura debe aprobarse para ser completada.')
        asignatura = self.__buscar_asignatura(id_asig)
        estudiante = self.__buscar_estudiante(dni)
        estudiante.añadir_asignatura_aprobada(asignatura, calificacion)
        estudiante.creditos_completados += asignatura.creditos
        estudiante.eliminar_asignatura_matriculada(asignatura)
        asignatura.eliminar_estudiantes(estudiante)
        print(f"{estudiante.nombre} ha aprobado la asignatura {asignatura.nombre} con una calificación de {calificacion}\n")

    
    def visualizar_boletin_de_calificaciones(self, dni):
        estudiante = self.__buscar_estudiante(dni)
        print(f"Boletín de Calificaciones de {estudiante.nombre}:\n")
        for asig, nota in estudiante.asignaturas_completadas:
            
            print(f"{asig}: {nota}\n")
            
    

    def visualizar_creditos_completados(self, dni):
        estudiante = self.__buscar_estudiante(dni)
        print(f"{estudiante.nombre} lleva {estudiante.creditos_completados} créditos completados.\n")


    def visualizar_est_matriculados_y_profesores_asig(self, id_asig):
        asignatura = self.__buscar_asignatura(id_asig)
        print(f"Profesores y estudiantes de {asignatura.nombre}: \n Profesores:")
        for p in asignatura.profesores:
            print(f"{p.nombre}\n")
        print("Alumnos matriculados:")
        for e in asignatura.estudiantes_matriculados:
            print(f"{e.nombre}\n")


    def asignar_profesorado_a_asignatura(self, dni, id_asig):
        prof = self.__buscar_profesor(dni)
        asignatura = self.__buscar_asignatura(id_asig)
        prof.añadir_asignatura_a_impartir(asignatura)
        asignatura.añadir_profesor(prof)
        print(f"Al profesor {prof.nombre} se le ha asignado la asignatura de {asignatura.nombre} para el grado de {asignatura.grado}\n")
    

    def eliminar_profesorado_de_asignatura(self, dni, id_asig):
        prof = self.__buscar_profesor(dni)
        asignatura = self.__buscar_asignatura(id_asig)
        prof.eliminar_asignatura_a_impartir(asignatura)
        asignatura.eliminar_profesor(prof)
        print(f"El profesor {prof.nombre} dejará de impartir la asignatura de {asignatura.nombre} en el grado de {asignatura.grado}\n")


    def visualizar_asignaturas_de_profesor(self, dni):
        prof = self.__buscar_profesor(dni)
        print(f"El profesor/a {prof.nombre} está impartiendo clase en: \n ")
        for curso, asignaturas in prof.asignaturas_a_impartir.items():
            print(f"Grado: {curso}, Asignaturas: {asignaturas}")


    def buscar_en_departamentos(self, dni):
        miembro = self.__buscar_profesor(dni)
        if miembro == "DNI no coincide":
            miembro = self.__buscar_investigador(dni)
        
        if miembro != "DNI no coincide":
            return miembro.departamento # Devuelve el departamento del miembro al que corresponda el dni
        return "DNI no coincide"

    def print_miembros_dep(self):
        for tipo, miembros in self.miembros_dep.items():
            print(f'Departamento: {tipo}\nMiembros:')
            for member in miembros:
                print(member)
                

    def __str__(self):
        txt = f"Universidad: {self.nombre}\n"
        
        txt += "** Profesores **\n"
        for profesor in self.profesores:
            txt += str(profesor) + "\n"
        
        txt += "** Investigadores **\n"
        for investigador in self.investigadores:
            txt += str(investigador) + "\n"

        txt += "** Estudiantes **\n"
        for estudiante in self.estudiantes:
            txt += str(estudiante) + "\n"
                
        return txt

# Tests unitarios

def test_insertar_estudiante():
    uni = Universidad("UPCT", "Cartagena", 30390)
    uni.insertar_estudiante("John Doe", "87654321C", "123 Main St", "V", "Data Science", "1st")
    assert len(uni.estudiantes) >= 1
    assert uni.estudiantes[0].nombre == "John Doe"

def test_insertar_prof_asociado():
    uni = Universidad("UPCT", "Cartagena", 30390)
    uni.insertar_prof_asociado("Jane Smith", "23456789D", "456 Elm St", "M", TipoDepartamento(1))
    assert len(uni.profesores) >= 1
    assert uni.profesores[0].nombre == "Jane Smith"

def test_insertar_prof_titular():
    uni = Universidad("UPCT", "Cartagena", 30390)
    uni.insertar_prof_titular("Alice Johnson", "34567890E", "789 Oak St", "OTRO", TipoDepartamento(2), "Computer Science")
    assert len(uni.profesores) > 0
    assert len(uni.investigadores) > 0
    assert uni.profesores[0].nombre == "Alice Johnson"

def test_eliminar_estudiante():
    uni = Universidad("UPCT", "Cartagena", 30390)
    uni.insertar_estudiante("John Doe", "87654321C", "123 Main St", "V", "Data Science", "1st")
    uni.eliminar_estudiante("87654321C")
    assert len(uni.estudiantes) < 1

def test_eliminar_profesor():
    uni = Universidad("UPCT", "Cartagena", 30390)
    uni.insertar_prof_asociado("Jane Smith", "23456789D", "456 Elm St", "M", TipoDepartamento(1))
    uni.eliminar_profesor("23456789D")
    assert len(uni.profesores) == 0

def test_eliminar_investigador():
    uni = Universidad("UPCT", "Cartagena", 30390)
    uni.insertar_investigador("Alice Johnson", "34567890E", "789 Oak St", "OTRO", TipoDepartamento(2), "Computer Science")
    uni.eliminar_investigador("34567890E")
    assert len(uni.profesores) < 1

def test_insertar_asignatura():
    uni = Universidad("UPCT", "Cartagena", 30390)
    uni.insertar_asignatura("9990007", "Calculus", "Mathematics", 6,  PeriodoAsignatura(2))
    assert len(uni.asignaturas) > 0
    assert uni.asignaturas[0].id == "9990007"

def test_cambio_departamento():
    uni = Universidad("UPCT", "Cartagena", 30390)
    uni.insertar_prof_titular("Alice Johnson", "34567890E", "789 Oak St", "OTRO", TipoDepartamento(2), "Computer Science")
    uni.cambio_departamento("34567890E", TipoDepartamento(1))
    assert uni.profesores[0].departamento == TipoDepartamento(1)
    
def test_buscar_en_departamentos():
    uni = Universidad("UPCT", "Cartagena", 30390)
    uni.insertar_prof_titular("Alice Johnson", "34567890E", "789 Oak St", "OTRO", TipoDepartamento(2), "Computer Science")
    assert uni.buscar_en_departamentos("34567890E") == uni.profesores[0].departamento

if __name__=='__main__':
    uni = Universidad("UPCT", "Cartagena", 30390)

    # Test insertar_estudiante
    uni.insertar_estudiante("John Doe", "87654321C", "123 Main St", "V", "Data Science", "1º")
    uni.insertar_estudiante("Carlos Garcia", "12345678A", "Calle Falsa 123", "V", "Matemáticas", "1º")
    uni.insertar_estudiante("Ana Martinez", "87654321B", "Avenida Siempre Viva 456", "M", "Física", "2º")
    uni.insertar_estudiante("Pedro Lopez", "23456789C", "Paseo de la Castellana 789", "V", "Química", "3º")

    # Test insertar_prof_asociado
    uni.insertar_prof_asociado("Jane Smith", "23456789D", "456 Elm St", "M", TipoDepartamento(1))
    uni.insertar_prof_asociado("Luis Perez", "56789012G", "Calle del Sol 123", "V", TipoDepartamento(1))
    uni.insertar_prof_asociado("Maria Gomez", "67890123H", "Avenida de la Luna 456", "M", TipoDepartamento(2))

    # Test insertar_prof_titular
    uni.insertar_prof_titular("Alice Johnson", "34567890E", "789 Oak St", "OTRO", TipoDepartamento(2), "Computación")
    uni.insertar_prof_titular("Jose Ramirez", "78901234I", "Paseo de las Estrellas 789", "V", TipoDepartamento(1), "Biología")
    uni.insertar_prof_titular("Isabel Torres", "89012345J", "Calle de la Tierra 987", "M", TipoDepartamento(1), "IA Generativa")

    # Test insertar_investigador
    uni.insertar_investigador("Bob Williams", "45678901F", "987 Pine St", "V", TipoDepartamento(3), "Computación")
    uni.insertar_investigador("Antonio Ruiz", "90123456K", "Avenida del Universo 321", "V", TipoDepartamento(1), "Astronomía")
    uni.insertar_investigador("Carmen Morales", "01234567L", "Paseo de la Galaxia 654", "M", TipoDepartamento(2), "AstroFísica")

    # Insertar asignaturas
    uni.insertar_asignatura("9990123", "Machine Learning I", "Data Science", 6,  PeriodoAsignatura(2))
    uni.insertar_asignatura("9990820", "Calculo", "Matemáticas", 6,  PeriodoAsignatura(2))
    uni.insertar_asignatura("9990007", "Calculo", "Data Science", 6,  PeriodoAsignatura(2))
    uni.insertar_asignatura("9990321", "Calculo", "Física", 6,  PeriodoAsignatura(2))
    uni.insertar_asignatura("9990035", "Física", "Matemáticas", 6, PeriodoAsignatura(1))
    uni.insertar_asignatura("999006I", "Química molecular II", "Química", 6, PeriodoAsignatura(1))
    uni.insertar_asignatura("999006V", "Compuestos biorgánicos", "Química", 6, PeriodoAsignatura(1))
    uni.insertar_asignatura("99901AT", "Bases Datos II", "Data Science", 6, PeriodoAsignatura(2))
    uni.insertar_asignatura("99900XP", "Astronomía", "Física", 6, PeriodoAsignatura(2))
    uni.insertar_asignatura("999007I", "AstroFísica", "Física", 6, PeriodoAsignatura(3))
    
    "COMENTARIO: BUENAS PROFESOR, DEJAMOS LOS COMANDOS COMENTADOS PARA QUE LE SEA MÁS FÁCIL LA VISUALIZACIÓN DE LO QUE REALIZA CADA MÉTODO."
    
    "IMPRESIÓN INFO UNIVERIDAD:"
    #print(uni)
    
    "IMPRESIÓN DEPARTAMENTOS JUNTO A SUS MIEMBROS:"
    #uni.print_miembros_dep()

    "PODEMOS OBSERVAR COMO ANTONIO RUIZ Y ISABEL TORRES CAMBIAN DE DEPARTAMENTO(TAMBIÉN LO HACEN A NIVEL INTERNO)"
    #uni.cambio_departamento("89012345J", TipoDepartamento(3))
    #uni.cambio_departamento("90123456K", TipoDepartamento(2))

    #uni.print_miembros_dep()

    "ELIMINACIÓN DE OBJETOS DEL SISTEMA:"

    '''for e in uni.estudiantes:
        print(e)
    uni.eliminar_estudiante("87654321C")

    print("ALUMNO ELIMINADO DEL SISTEMA:")
    for e in uni.estudiantes:
        print(e)'''


    '''uni.print_miembros_dep()
    for p in uni.profesores:
        print(p)
    uni.eliminar_profesor("78901234I")  ERROR!!!!!!!!!

    print("PROFESOR ELIMINADO DEL SISTEMA:")
    for p in uni.profesores:
        print(p)'''
    

    
    '''for i in uni.investigadores:
        print(i)
    uni.eliminar_investigador("01234567L") 

    print("INVESTIGADOR ELIMINADO DEL SISTEMA:")
    for i in uni.investigadores:
        print(i)
    

    uni.print_miembros_dep()'''


    print()
    print("MÉTODOS ASOCIADOS A ASIGNATURAS Y ESTUDIANTES:\n")

    uni.añadir_asignatura_a_cursar("87654321C", "9990123")
    uni.añadir_asignatura_a_cursar("87654321C", "99901AT")
    
    uni.aprobar_asignatura("87654321C", "9990123", 9)
    uni.aprobar_asignatura("87654321C", "99901AT", 6)
    
    uni.visualizar_boletin_de_calificaciones("87654321C")
    uni.visualizar_creditos_completados("87654321C")


    print()
    print("MÉTODOS ASOCIADOS A ASIGNATURAS Y PROFESORES:\n")
    uni.asignar_profesorado_a_asignatura("89012345J", "9990123")
    uni.asignar_profesorado_a_asignatura("56789012G", "9990820")
    uni.visualizar_est_matriculados_y_profesores_asig("9990123") # ¿ Por qué no aparece en matriculados en Machine Learning I John Doe?
    print("No hay alumnos matriculados \n")
    uni.añadir_asignatura_a_cursar("12345678A", "9990123")              # Porque al aprobar la asignatura autómaticamente se le desmatricula.
    uni.visualizar_est_matriculados_y_profesores_asig("9990123")
    # Ahora si aparecería el alumno.

    uni.eliminar_profesorado_de_asignatura("89012345J", "9990123") # Vemos como podemos quitar el puesto de profesor en una asignatura específica
    uni.visualizar_est_matriculados_y_profesores_asig("9990123")


    # Por último, veamos todas las asignaturas que imparte un profesor:
    uni.asignar_profesorado_a_asignatura("34567890E", "9990820")
    uni.asignar_profesorado_a_asignatura("34567890E", "9990035")
    uni.asignar_profesorado_a_asignatura("34567890E", "9990007")
    uni.asignar_profesorado_a_asignatura("34567890E", "9990321")

    uni.visualizar_asignaturas_de_profesor("34567890E")