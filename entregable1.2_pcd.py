import pytest
from enum import Enum

class Persona:
    def __init__(self, nombre, dni, direccion, sexo):
        self.nombre = nombre
        if len(dni) != 9:
            raise Exception("Formato DNI incorrecto")
        self.dni = dni
        self.direccion = direccion
        if sexo not in ["V", "M"]:
            raise ValueError("El sexo debe ser 'V' o 'M'")
        self.sexo = sexo
        
        def __str__(self):
            return f"Nombre: {self.nombre}\nDNI: {self.dni}\nDirección: {self.direccion}\nSexo: {self.sexo}"
        
    class PeriodoAsignatura(Enum):
        CUATRIMESTRE_1 = 1
        CUATRIMESTRE_2 = 2
        ANUAL = 3
        
        def __str__(self):
            return self.nombre
    
class Asignatura:
    def __init__(self, nombre, grado, creditos, tipo):
        self.nombre = nombre
        self.grado = grado
        self.creditos = float(creditos)
        if not isinstance(tipo, PeriodoAsignatura):
            raise ValueError("Tipo debe ser un valor entre 1 y 3")
        self.tipo = tipo
            
class Estudiante(Persona):
    
    estudiantes = {}
    
    def __init__(self, nombre, dni, direccion, sexo, grado, curso):
        super().__init__(nombre, dni, direccion, sexo)
        self.grado = grado
        self.curso = curso
        self.creditos_completados = 0
        self.asignaturas_completadas = []
        self.asignaturas_cursando = []
        
    def aprobar_asignatura(self, asignatura, calificacion):
        assert asignatura < 5, "Asignatura no aprobada"
        self.asignaturas_completadas.append((asignatura.nombre, calificacion))
        self.creditos_completados += asignatura.creditos
        self.asignaturas_cursando.remove(asignatura.nombre)
        
    def añadir_asignatura_a_cursar(self, asignatura):
        assert len(self.asignaturas_cursando) > 12, 'No se pueden cursar más de 12 asignaturas al mismo tiempo.'
        self.asignaturas_cursando.append(asignatura.nombre)
        
    def __str__(self):
        return f"Estudiante: {self.nombre}\nDNI: {self.dni}\nDirección: {self.direccion}\nSexo: {self.sexo}\nGrado: {self.grado}\nCurso: {self.curso}\n"
    
    @classmethod
    def añadir_estudiante(cls, estudiante):
        cls.estudiantes[estudiante.dni] = estudiante

    @classmethod
    def eliminar_estudiante(cls, dni):
        if dni in cls.estudiantes:
            del cls.estudiantes[dni]
        else:
            print("El DNI no coincide.")
            
class TipoDepartamento(Enum):
    DIIC = 1
    DITEC = 2
    DIS = 3

    def __str__(self):
        return self.name

class Departamento:
    miembros_dep = {TipoDepartamento.DIIC: [], TipoDepartamento.DITEC: [], TipoDepartamento.DIS: []}

    @classmethod
    def añadir_miembro_dep(cls, miembro):  # OBJETO MIEMBRO DE DEPARTAMENTO
        cls.miembros_dep[miembro.departamento].append(miembro)

    @classmethod
    def eliminar_miembro_dep(cls, dni):
        for tipo in TipoDepartamento:
            for miembro in cls.miembros_dep[tipo]:
                if miembro.dni == dni:
                    cls.miembros_dep[tipo].remove(miembro)
                    return
        return "DNI no encontrado"

    @classmethod
    def buscar_miembro_dep(cls, dni):
        for tipo in TipoDepartamento:
            for miembro in cls.miembros_dep[tipo]:
                if miembro.dni == dni:
                    return miembro.nombre
        return "DNI no coincide"

    @classmethod
    def __str__(cls):
        return '\n'.join(
            f'Departamento: {tipo}\nMiembros:\n' + 
            '\n'.join(
                f"\tNombre: {member.nombre}\n\t"
                f"DNI: {member.dni}\n\t"
                f"Dirección: {member.direccion}\n\t"
                f"Sexo: {member.sexo}\n\t"
                for member in cls.miembros_dep[tipo]
            )
            for tipo in TipoDepartamento
        )
    
class MiembroDepartamento(Persona):
    def __init__(self, nombre, dni, direccion, sexo, departamento):
        super().__init__(nombre, dni, direccion, sexo)
        if not isinstance(departamento, TipoDepartamento):
            raise ValueError('El departamento debe ser uno de los tres definidos(DIIC, DITEC, DIS)')
        self.departamento = departamento
        Departamento.añadir_miembro_dep(self)

    def cambiar_departamento(self, nuevo_departamento):
        Departamento.eliminar_miembro_dep(self.dni)  # Pasamos el DNI del miembro
        self.departamento = nuevo_departamento
        Departamento.añadir_miembro_dep(self)  # Añadimos el miembro al nuevo departamento

    def __str__(self):
        return f'Nombre: {self.nombre}\nDNI: {self.dni}\nDirección: {self.direccion}\nSexo: {self.sexo}\nDepartamento: {self.departamento}\n'
    
if __name__ == "__main__":
    s = MiembroDepartamento(nombre="Rubén Gil Martínez", dni="26649110E", direccion="Orellana 22", sexo="V", departamento=TipoDepartamento(2))
    
    dep = Departamento()
    dep.añadir_miembro_dep(s)