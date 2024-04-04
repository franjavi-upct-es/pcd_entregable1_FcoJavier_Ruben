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
        self.estudiantes_matriculados.append(profesor)
    
    def eliminar_profesor(self, profesor):
        self.estudiantes_matriculados.remove(profesor)

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

    def aprobar_asignatura(self, asignatura, calificacion):
        if calificacion < 5:
            raise ValueError('La asignatura debe aprobarse para ser completada.')
        self.asignaturas_completadas.append((asignatura, calificacion))
        self.creditos_completados += asignatura.creditos
        self.asignaturas_cursando.remove(asignatura)

    def añadir_asignatura_a_cursar(self, asignatura):
        if len(self.asignaturas_cursando) > 12:
            raise ValueError('No se pueden cursar más de 12 asignaturas al mismo tiempo.')
        self.asignaturas_cursando.append(asignatura)

    """
    def visualizar_boletin_de_calificaciones(self):
        for calificacion in self.asignaturas_completadas:
            print(calificacion)

    def visualizar_creditos_completados(self, dni):
        return self.creditos_completados[dni]
    """

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

    def cambiar_dep(self, nuevo_departamento):
        self.departamento = nuevo_departamento

    def __str__(self):
        return f'Nombre: {self.nombre}\nDNI: {self.dni}\nDirección: {self.direccion}\nSexo: {self.sexo}\n'


class ProfesorAsociado(MiembroDepartamento):
    def __init__(self, nombre, dni, direccion, sexo, departamento):
        super().__init__(nombre, dni, direccion, sexo, departamento)
        self.asignaturas_a_impartir = {}

    def añadir_asignatura_a_impartir(self, asignatura):
        if asignatura.grado not in self.asignaturas_a_impartir:
            self.asignaturas_a_impartir[asignatura.grado] = []  # Si el grado no está en el diccionario, añade una lista vacía
        self.asignaturas_a_impartir[asignatura.grado].append(asignatura)  # Añade la asignatura a la lista de ese grado

    def eliminar_asignatura_a_impartir(self, asignatura):
        if asignatura.grado in self.asignaturas_a_impartir and asignatura in self.asignaturas_a_impartir[asignatura.grado]:
            self.asignaturas_a_impartir[asignatura.grado].remove(asignatura)  # Elimina la asignatura de la lista de ese grado
            if not self.asignaturas_a_impartir[asignatura.grado]:  # Si la lista de ese grado está vacía, elimina el grado del diccionario
                del self.asignaturas_a_impartir[asignatura.grado]

    def __str__(self):
        return f'Nombre: {self.nombre}\nDNI: {self.dni}\nDirección: {self.direccion}\nSexo: {self.sexo}\nDepartamento: {self.departamento}\nAsignaturas a Impartir: {self.asignaturas_a_impartir}\n'



class ProfesorTitular(MiembroDepartamento):
    def __init__(self, nombre, dni, direccion, sexo, departamento, rol_investigacion):
        super().__init__(nombre, dni, direccion, sexo, departamento)
        self.asignaturas_a_impartir = {}
        self.rol_investigacion = rol_investigacion

    def añadir_asignatura_a_impartir(self, asignatura):
        if asignatura.grado not in self.asignaturas_a_impartir:
            self.asignaturas_a_impartir[asignatura.grado] = []  # Si el grado no está en el diccionario, añade una lista vacía
        self.asignaturas_a_impartir[asignatura.grado].append(asignatura)  # Añade la asignatura a la lista de ese grado

    def eliminar_asignatura_a_impartir(self, asignatura):
        if asignatura.grado in self.asignaturas_a_impartir and asignatura in self.asignaturas_a_impartir[asignatura.grado]:
            self.asignaturas_a_impartir[asignatura.grado].remove(asignatura)  # Elimina la asignatura de la lista de ese grado
            if not self.asignaturas_a_impartir[asignatura.grado]:  # Si la lista de ese grado está vacía, elimina el grado del diccionario
                del self.asignaturas_a_impartir[asignatura.grado]

    def __str__(self):
        return f'Nombre: {self.nombre}\nDNI: {self.dni}\nDirección: {self.direccion}\nSexo: {self.sexo}\nDepartamento: {self.departamento}\nAsignaturas a Impartir: {self.asignaturas_a_impartir}\nRol de Investigación: {self.rol_investigacion}'

class Investigador(MiembroDepartamento):
    def __init__(self, nombre, dni, direccion, sexo, departamento, rol_investigacion):
        super().__init__(nombre, dni, direccion, sexo, departamento)
        self.rol_investigacion = rol_investigacion

    def __str__(self):
        return f'Nombre: {self.nombre}\nDNI: {self.dni}\nDirección: {self.direccion}\nSexo: {self.sexo}\nDepartamento: {self.departamento}\nRol de Investigación: {self.rol_investigacion}'

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


    def buscar_estudiante(self, dni):
        for estudiante in self.estudiantes:
            if dni == estudiante.dni:
                return estudiante
        return "DNI no coincide"
    
    def buscar_profesor(self, dni):
        for profesor in self.profesores:
            if dni == profesor.dni:
                return profesor
        return "DNI no coincide"
    
    def buscar_investigador(self, dni):
        for investigador in self.investigadores:
            if dni == investigador.dni:
                return investigador
        return "DNI no coincide"

    def añadir_miembro_dep(self, dni):
        miembro = self.buscar_profesor(dni)

        if miembro == "DNI no coincide":
            miembro = self.buscar_investigador(dni)

        if miembro != "DNI no coincide":
            if miembro.departamento not in self.miembros_dep:
                self.miembros_dep[miembro.departamento] = []
            self.miembros_dep[miembro.departamento].append(miembro)
        else:
            return "DNI no coincide"
    
    def eliminar_miembro_dep(self, dni):
        miembro = self.buscar_profesor(dni)

        if miembro == "DNI no coincide":
            miembro = self.buscar_investigador(dni)

        if miembro != "DNI no coincide":
            self.miembros_dep[miembro.departamento].remove(miembro)
        else:
            return "DNI no coincide"
    
    def insertar_estudiante(self, nombre, dni, direccion, sexo, grado, curso):
        estudiante = Estudiante(nombre, dni, direccion, sexo, grado, curso)
        self.estudiantes.append(estudiante)
    
    def insertar_prof_asociado(self, nombre, dni, direccion, sexo, departamento):
        prof_asoc = ProfesorAsociado(nombre, dni, direccion, sexo, departamento)
        self.profesores.append(prof_asoc)
        self.añadir_miembro_dep(prof_asoc.dni)
    
    def insertar_prof_titular(self, nombre, dni, direccion, sexo, departamento, rol_investigacion):
        prof_titular = ProfesorTitular(nombre, dni, direccion, sexo, departamento, rol_investigacion)
        self.profesores.append(prof_titular)
        self.investigadores.append(prof_titular)
        self.añadir_miembro_dep(prof_titular.dni)

    def insertar_investigador(self, nombre, dni, direccion, sexo, departamento, rol_investigacion):
        inves = Investigador(nombre, dni, direccion, sexo, departamento, rol_investigacion)
        self.investigadores.append(inves)
        self.añadir_miembro_dep(inves.dni)

    def cambio_departamento(self, dni, nuevo_departamento):
        assert nuevo_departamento in TipoDepartamento, "Departamento inválido"
        miembro = self.buscar_profesor(dni)
        if miembro == "DNI no coincide":
            miembro = self.buscar_investigador(dni)
        
        if miembro != "DNI no coincide":
            self.eliminar_miembro_dep(miembro.dni)  # Pasamos el DNI del miembro
            miembro.cambio_dep(nuevo_departamento)
            self.añadir_miembro_dep(miembro.dni)  # Añadimos el miembro al nuevo departamento
        else:
            return "DNI no coincide"

    def eliminar_estudiante(self, dni):
        estudiante = self.buscar_estudiante(dni)
        if estudiante is not None:
            self.estudiantes.remove(estudiante)
        for i in self.asignaturas:
            i.eliminar_estudiante(estudiante)

    def eliminar_profesor(self, dni):
        prof = self.buscar_profesor(dni)
        if prof is not None:
            self.profesores.remove(prof)
            self.eliminar_miembro_dep(dni)
        for i in self.asignaturas:
            i.eliminar_profesor(prof)

    def eliminar_investigador(self, dni):
        inves = self.buscar_investigador(dni)
        if inves is not None:
            self.eliminar_miembro_dep(dni)
            self.eliminar_miembro_dep(dni)