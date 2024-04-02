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
        return f"Estudiante: {self.nombre}\nDNI: {self.dni}\nDirección: {self.direccion}\nSexo: {self.sexo}\nGrado: {self.grado}\nCurso: {self.curso}"

    @classmethod
    def añadir_estudiante(cls, estudiante):
        cls.estudiantes[estudiante.dni] = estudiante

    @classmethod
    def eliminar_estudiante(cls, estudiante):
        if estudiante.dni in cls.estudiantes:
            del cls.estudiantes[estudiante.dni]
        else:
            print("El DNI no coincide.")


class TipoDepartamento(Enum):
    DIIC = 1
    DITEC = 2
    DIS = 3

class Departamento:
    def __init__(self, nombre, director, area_estudio):
        if not isinstance(nombre, TipoDepartamento):
            raise ValueError('El nombre de departamento debe ser uno de los tres definidos(DIIC, DITEC, DIS)')
        self.nombre = nombre
        self.director = director
        self.area_estudio = area_estudio
        self.miembros_dep = {TipoDepartamento.DIIC: [], TipoDepartamento.DITEC: [], TipoDepartamento.DIS: []}

    def añadir_miembro_dep(self, miembro):  # OBJETO MIEMBRO DE DEPARTAMENTO
        self.miembros_dep[miembro.TipoDepartamento].append(miembro)

    def eliminar_miembro_dep(self, miembro):  # OBJETO MIEMBRO DE DEPARTAMENTO
        if miembro in self.miembros_dep[miembro.TipoDepartamento]:
            self.miembros_dep[miembro.TipoDepartamento].remove(miembro)
        else:  
            return "Miembro no encontrado"

    def buscar_miembro_dep(self, dni):
        for tipo in TipoDepartamento:
            for miembro in self.miembros_dep[tipo]:
                if miembro.dni == dni:
                    return miembro
        return "DNI no coincide"

    def __str__(self):
        return f'Nombre: {self.nombre}\nMiembros: {self.miembros_dep}'

class MiembroDepartamento(Persona):

    miembros = {}

    def __init__(self, nombre, dni, direccion, sexo, departamento):
        super().__init__(nombre, dni, direccion, sexo)
        if not isinstance(departamento, TipoDepartamento):
            raise ValueError('El departamento debe ser uno de los tres definidos(DIIC, DITEC, DIS)')
        self.departamento = departamento

    def cambiar_departamento(self, nuevo_departamento):
        if not isinstance(nuevo_departamento, TipoDepartamento):
            raise ValueError('El nuevo departamento debe ser uno de los tres definidos(DIIC, DITEC, DIS)')
        self.departamento.eliminar_miembro_dep(self) # Pasamos el objeto completo para poder acceder a su DNI
        self.departamento = nuevo_departamento
        self.departamento.añadir_miembro_dep(self)

    def __str__(self):
        return f'Nombre: {self.nombre}\nDNI: {self.dni}\nDirección: {self.direccion}\nSexo: {self.sexo}\nDepartamento: {self.departamento}'

    @classmethod
    def añadir_miembros(cls, miembro):
        cls.miembros[miembro.dni] = miembro

    @classmethod
    def eliminar_miembros(cls, miembro):
        if miembro.dni in cls.miembros:
            del cls.miembros[miembro.dni]
        else:
            print("El DNI no coincide.")
    

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

    s = MiembroDepartamento("Antonio Galindo", "12345678B", "Hiedra 50", "V", TipoDepartamento.DITEC)

    dep = Departamento
    print(dep)
    dep.añadir_miembro_dep(s)