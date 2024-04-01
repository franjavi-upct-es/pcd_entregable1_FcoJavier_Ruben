import pytest
from enum import Enum

class EmptyException(Exception):
    pass


class Persona:

    def __init__(self, nombre, dni, direccion, sexo):
        self.nombre = nombre
        self.__dni = dni
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
        self.creditos = int(creditos)
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

    def aprobar_asignatura(self, asignatura, creditos, calificacion):
        if calificacion < 5:
            raise ValueError('La asignatura debe aprobarse para ser completada.')
        self.asignaturas_completadas.append((asignatura, calificacion))
        self.creditos_completados += creditos
        self.asignaturas_cursando.remove(asignatura)

    def añadir_asignatura_a_cursar(self, asignatura):
        if len(self.asignaturas_cursando) > 12:
            raise ValueError('No se pueden cursar más de 12 asignaturas al mismo tiempo.')
        self.asignaturas_cursando.append(asignatura)

    def visualizar_boletin_de_calificaciones(self):
        for calificacion in self.asignaturas_completadas:
            print(calificacion)

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

#############################################################################

class Departamento:
    def __init__(self, nombre, director, area_estudio):
        if not isinstance(nombre, TipoDepartamento):
            raise ValueError('El nombre de departamento debe ser uno de los tres definidos(DIIC, DITEC, DIS)')
        self.nombre = nombre
        self.director = director
        self.area_estudio = area_estudio
        self.miembros_dep = {}

    def añadir_miembro_dep(self, miembro):  # OBJETO MIEMBRO DE DEPARTAMENTO
        self.miembros_dep[miembro.dni] = miembro  # Usamos add en lugar de append para añadir a un conjunto

    def eliminar_miembro_dep(self, miembro):  # OBJETO MIEMBRO DE DEPARTAMENTO
        if miembro.dni in self.miembros_dep:
            del self.miembros_dep[miembro.dni]
        else:  
            return "DNI no coincide"

    def buscar_miembro_dep(self, dni):
        if self.dni in self.miembros_dep:
            return self.nombre
        else:
            return "DNI no coincide"

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

    def añadir_asignatura_a_impartir(self, grado, asignatura):
        if grado not in self.asignaturas_a_impartir:
            self.asignaturas_a_impartir[grado] = []  # Si el grado no está en el diccionario, añade una lista vacía
        self.asignaturas_a_impartir[grado].append(asignatura)  # Añade la asignatura a la lista de ese grado

    def eliminar_asignatura_a_impartir(self, grado, asignatura):
        if grado in self.asignaturas_a_impartir and asignatura in self.asignaturas_a_impartir[grado]:
            self.asignaturas_a_impartir[grado].remove(asignatura)  # Elimina la asignatura de la lista de ese grado
            if not self.asignaturas_a_impartir[grado]:  # Si la lista de ese grado está vacía, elimina el grado del diccionario
                del self.asignaturas_a_impartir[grado]

class ProfesorAsociado(Profesor):
    def __init__(self, nombre, dni, direccion, sexo, departamento, cv, doctorado, perfil_linkedin):
        super().__init__(nombre, dni, direccion, sexo, departamento, cv, doctorado, perfil_linkedin)
        self.asignaturas_a_impartir = {}




class ProfesorTitular(Profesor):
    def __init__(self, nombre, dni, direccion, sexo, departamento, cv, doctorado, perfil_linkedin, area_investigacion, rol_investigacion):
        super().__init__(nombre, dni, direccion, sexo, departamento, cv, doctorado, perfil_linkedin)
        self.asignaturas_a_impartir = {}
        self.area_investigacion = area_investigacion
        self.rol_investigacion = rol_investigacion


#########################################################################

class Investigador(MiembroDepartamento):
    def __init__(self, nombre, dni, direccion, sexo, departamento, cv, area_investigacion, rol_investigacion, financiacion, papers_publicados):
        super().__init__(nombre, dni, direccion, sexo, departamento)
        self.__cv = cv
        self.area_investigacion = area_investigacion
        self.rol_investigacion = rol_investigacion
        self.__financiacion = financiacion
        self.papers_publicados = papers_publicados