import pytest
from enum import Enum

class EmptyException(Exception):
    pass


class Persona:

    def __init__(self, nombre, dni, direccion, sexo):
        self.nombre = nombre
        self.dni = dni
        self.direccion = direccion
        if sexo not in ['V', 'M', 'OTRO']:
            raise EmptyException("El sexo debe ser 'V', 'M' u 'OTRO'")
        self.sexo = sexo

class PeriodoAsignatura(Enum):
    CUATRIMESTRE_1 = 1
    CUATRIMESTRE_2 = 2
    ANUAL = 3

class Asignatura:
    def __init__(self, nombre, grado, creditos, tipo):
        self.nombre = nombre
        self.grado = grado
        self.creditos = creditos
        if not isinstance(tipo, PeriodoAsignatura):
            raise ValueError('Tipo debe ser un valor entre 1 y 3')
        self.tipo = tipo

class Estudiante(Persona):

    estudiantes = {}

    def __init__(self, nombre, dni, direccion, sexo, grado, curso):
        super().__init__(nombre, dni, direccion, sexo)
        self.grado = grado
        self.curso = curso
        self.creditos_completados = 0
        self.asignaturas_completadas = [] # [(asignatura1, calificacion1), (asignatura2, calificacion2)....]
        self.asignaturas_cursando = []    # [asignatura1, asignatura2, ...]

    def aprobar_asignatura(self, asignatura, calificacion):
        if calificacion < 5:
            raise ValueError('La asignatura debe aprobarse para ser completada.')
        self.asignaturas_completadas.append((asignatura.nombre, calificacion))
        self.creditos_completados += asignatura.creditos
        self.asignaturas_cursando.remove(asignatura.nombre)

    def añadir_asignatura_a_cursar(self, asignatura):
        if len(self.asignaturas_cursando) > 12:
            raise ValueError('No se pueden cursar más de 12 asignaturas al mismo tiempo.')
        self.asignaturas_cursando.append(asignatura.nombre)

    def visualizar_boletin_de_calificaciones(self):
        for calificacion in self.asignaturas_completadas:
            print(calificacion)

    def visualizar_creditos_completados(self):
        return self.creditos_completados
    
    def __str__(self):
        return f"Estudiante: {self.nombre}\nDNI: {self.dni}\nDirección: {self.direccion}\nSexo: {self.sexo}\nGrado: {self.grado}\nCurso: {self.curso}\n"

    
class TipoDepartamento(Enum):
    DIIC = 1
    DITEC = 2
    DIS = 3

    def __str__(self):
        return self.name

class Departamento:
    miembros_dep = {TipoDepartamento.DIIC: [], TipoDepartamento.DITEC: [], TipoDepartamento.DIS: []}

    

class MiembroDepartamento(Persona):

    miembros = {}

    def __init__(self, nombre, dni, direccion, sexo, departamento):
        super().__init__(nombre, dni, direccion, sexo)
        if not isinstance(departamento, TipoDepartamento):
            raise ValueError('El departamento debe ser uno de los tres definidos(DIIC, DITEC, DIS)')
        self.departamento = departamento

    def cambiar_departamento(self, nuevo_departamento):
        Departamento.eliminar_miembro_dep(self)  # Pasamos el objeto completo para poder acceder a su DNI
        Departamento.añadir_miembro_dep(self)
        self.departamento = nuevo_departamento

    def __str__(self):
        return f'Nombre: {self.nombre}\nDNI: {self.dni}\nDirección: {self.direccion}\nSexo: {self.sexo}\nDepartamento: {self.departamento}\n'

    
    

##############################################################################
class Profesor(MiembroDepartamento):
    def __init__(self, nombre, dni, direccion, sexo, departamento, cv, doctorado, perfil_linkedin):
        super().__init__(nombre, dni, direccion, sexo, departamento)
        self.__cv = cv
        self.doctorado = doctorado
        self.perfil_linkedin = perfil_linkedin
        self.asignaturas_a_impartir = {}  # Ahora es un diccionario

    def añadir_asignatura_a_impartir(self, asignatura):
        if asignatura.grado not in self.asignaturas_a_impartir:
            self.asignaturas_a_impartir[asignatura.grado] = []  # Si el grado no está en el diccionario, añade una lista vacía
        self.asignaturas_a_impartir[asignatura.grado].append(asignatura.nombre)  # Añade la asignatura a la lista de ese grado

    def eliminar_asignatura_a_impartir(self, asignatura):
        if asignatura.grado in self.asignaturas_a_impartir and asignatura.nombre in self.asignaturas_a_impartir[asignatura.grado]:
            self.asignaturas_a_impartir[asignatura.grado].remove(asignatura.nombre)  # Elimina la asignatura de la lista de ese grado
            if not self.asignaturas_a_impartir[asignatura.grado]:  # Si la lista de ese grado está vacía, elimina el grado del diccionario
                del self.asignaturas_a_impartir[asignatura.grado]

class ProfesorAsociado(Profesor):
    def __init__(self, nombre, dni, direccion, sexo, departamento, cv, doctorado, perfil_linkedin):
        super().__init__(nombre, dni, direccion, sexo, departamento, cv, doctorado, perfil_linkedin)
        self.asignaturas_a_impartir = {}

    def __str__(self):
        return f'Nombre: {self.nombre}\nDNI: {self.dni}\nDirección: {self.direccion}\nSexo: {self.sexo}\nDepartamento: {self.departamento}\nCV: {self.cv}\nDoctorado: {self.doctorado}\nPerfil LinkedIn: {self.perfil_linkedin}\nAsignaturas a Impartir: {self.asignaturas_a_impartir}'

class ProfesorTitular(Profesor):
    def __init__(self, nombre, dni, direccion, sexo, departamento, cv, doctorado, perfil_linkedin, area_investigacion, rol_investigacion):
        super().__init__(nombre, dni, direccion, sexo, departamento, cv, doctorado, perfil_linkedin)
        self.asignaturas_a_impartir = {}
        self.area_investigacion = area_investigacion
        self.rol_investigacion = rol_investigacion

    def __str__(self):
        return f'Nombre: {self.nombre}\nDNI: {self.dni}\nDirección: {self.direccion}\nSexo: {self.sexo}\nDepartamento: {self.departamento}\nCV: {self.cv}\nDoctorado: {self.doctorado}\nPerfil LinkedIn: {self.perfil_linkedin}\nAsignaturas a Impartir: {self.asignaturas_a_impartir}\nÁrea de Investigación: {self.area_investigacion}\nRol de Investigación: {self.rol_investigacion}'


#########################################################################

class Investigador(MiembroDepartamento):
    def __init__(self, nombre, dni, direccion, sexo, departamento, cv, area_investigacion, rol_investigacion, financiacion, papers_publicados):
        super().__init__(nombre, dni, direccion, sexo, departamento)
        self.__cv = cv
        self.area_investigacion = area_investigacion
        self.rol_investigacion = rol_investigacion
        self.__financiacion = financiacion
        self.papers_publicados = papers_publicados

    def __str__(self):
        return f'Nombre: {self.nombre}\nDNI: {self.dni}\nDirección: {self.direccion}\nSexo: {self.sexo}\nDepartamento: {self.departamento}\nÁrea de Investigación: {self.area_investigacion}\nRol de Investigación: {self.rol_investigacion}\nPresupuesto: {self.presupuesto}\nPapers Publicados: {self.papers_publicados}'


def test_persona_creation():
    persona = Persona("John Doe", "12345678A", "Calle Falsa 123", "V")
    assert persona.nombre == "John Doe"
    assert persona.direccion == "Calle Falsa 123"
    assert persona.sexo == "V"
    print(persona)

def test_persona_invalid_sex():
    with pytest.raises(EmptyException):
        Persona("John Doe", "12345678A", "Calle Falsa 123", "INVALID")

def test_asignatura_creation():
    asignatura = Asignatura("Matemáticas", "Ingeniería", 6, PeriodoAsignatura(2))
    assert asignatura.nombre == "Matemáticas"
    assert asignatura.grado == "Ingeniería"
    assert asignatura.creditos == 6
    assert asignatura.tipo == PeriodoAsignatura(2)

def test_asignatura_invalid_type():
    with pytest.raises(TypeError):
        Asignatura("Matemáticas", "Ingeniería", 6, PeriodoAsignatura(2))

if __name__=="__main__":
    r = Estudiante("FJMM", "26649110E", "Orellana, 22", "M", "MED", "1º")
    print(r)

    s = MiembroDepartamento("Antonio Galindo", "12345678B", "Hiedra 50", "V", TipoDepartamento(2))
    t = MiembroDepartamento("Rubén Gil", "22985630M", "Fuster 1", "V", TipoDepartamento(2))

    Departamento.añadir_miembro_dep(s)
    Departamento.añadir_miembro_dep(t)
    t.cambiar_departamento(TipoDepartamento(1))
    print(Departamento())
    Departamento.eliminar_miembro_dep("22985630M")
    print(Departamento())
    Departamento.buscar_miembro_dep("22985630M")
