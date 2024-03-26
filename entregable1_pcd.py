import pytest

class EmptyException(Exception):
    pass

class Persona:
    def __init__(self, nombre, dni, direccion, sexo):
        self.nombre = nombre
        self.__dni = dni
        self.direccion = direccion
        if sexo not in ['V', 'M']:
            raise EmptyException("El sexo debe ser 'V' o 'M'")
        self.sexo = sexo

class Estudiante(Persona):
    def __inti__(self, nombre, dni, direccion, sexo, asignaturas):
        super().__init__(nombre, dni, direccion, sexo)
        self.asignaturas = asignaturas

class Profesor(Persona):
    def __inti__(self, nombre, dni, direccion, sexo, asignaturas):
        super().__init__(nombre, dni, direccion, sexo)
        self.asignaturas = asignaturas

class ProfesorAsociado(Profesor):
    def __init__(self, nombre, dni, direccion, sexo, asignaturas):
        super().__init__(nombre, dni, direccion, sexo, asignaturas)

class ProfesorTitular(Profesor):
    def __init__(self, nombre, dni, direccion, sexo, asignaturas):
        super().__init__(nombre, dni, direccion, sexo, asignaturas)

class Investigador(ProfesorTitular):
    def __init__(self, nombre, dni, direccion, sexo, asignaturas, area_investigacion):
        super().__init__(nombre, dni, direccion, sexo, asignaturas)
        self.area_investigacion = area_investigacion