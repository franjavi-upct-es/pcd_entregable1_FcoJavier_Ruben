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
    def __init__(self, nombre, dni, direccion, sexo, grado):
        super().__init__(nombre, dni, direccion, sexo)
        self.grado = grado
        self.creditos_completados = 0
        self.asignaturas_completadas = []
        self.asignaturas_cursando = []

    def aprobar_asignatura(self, asignatura, creditos):
        self.asignaturas_completadas.append(asignatura)
        self.creditos_completados += creditos
        self.asignaturas_cursando.remove(asignatura)

    def añadir_asignatura_actual(self, asignatura):
        if len(self.asignaturas_cursando) > 12:
            raise ValueError('No se pueden cursar más de 12 asignaturas al mismo tiempo')
        self.asignaturas_cursando.append(asignatura)

class TipoDepartamento(Enum):
    DIIC = 1
    DITEC = 2
    DIS = 3

class Departamento:
    def __init__(self, nombre, director, area_estudio):
        self.nombre = nombre
        self.director = director
        self.area_estudio = area_estudio
        self.miembros = []

    def añadir_miembro(self, miembro):
        self.miembros.append(miembro)

    def eliminar_miembro(self, miembro):
        self.miembros.remove(miembro)


class MiembroDepartamento(Persona):
    def __init__(self, nombre, dni, direccion, sexo, departamento):
        super().__init__(nombre, dni, direccion, sexo)
        self.departamento = departamento

    def cambiar_departamento(self, nuevo_departamento):
        self.departamento.eliminar_miembro(self)
        self.departamento = nuevo_departamento
        self.departamento.añadir_miembro(self)

class ProfesorAsociado(MiembroDepartamento):
    def __init__(self, nombre, dni, direccion, sexo, departamento, cv, doctorado):
        super().__init__(nombre, dni, direccion, sexo, departamento)
        self.asignaturas_a_impartir = []
        self.__cv = cv
        self.doctorado = doctorado

    def añadir_asignatura_actual(self, asignatura):
        self.asignaturas_cursando.append(asignatura)

class ProfesorTitular(MiembroDepartamento):
    def __init__(self, nombre, dni, direccion, sexo, departamento, cv, doctorado):
        super().__init__(nombre, dni, direccion, sexo, departamento)
        self.asignaturas_a_impartir = []
        self.__cv = cv
        self.doctorado = doctorado

class Investigador(ProfesorTitular):
    def __init__(self, nombre, dni, direccion, sexo, departamento, cv, doctorado, area_investigacion, dedicacion_completa):
        if not isinstance(dedicacion_completa, bool):
            raise EmptyException('Debe ser True o False')
        super().__init__(nombre, dni, direccion, sexo, departamento, cv, doctorado)
        self.area_investigacion = area_investigacion
        if self.dedicacion_completa is False:
            self.asignaturas = []