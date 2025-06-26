import datetime
import json
import os
import glob

# Obtener la fecha actual automáticamente
hoy = datetime.date.today()

# Leer citas desde archivo
with open("bbdd.json", "r", encoding="utf-8") as f:
    citas = json.load(f)

# Obtener valor anidado en la cita (por ejemplo: profesional.nombre)
def obtener_valor(cita, clave):
    partes = clave.split(".")
    valor = cita
    for parte in partes:
        valor = valor.get(parte)
        if valor is None:
            return None
    return valor

# Evaluar si una cita cumple todas las condiciones de una regla
def cumple_condiciones(cita, condiciones):
    for campo, valor_esperado in condiciones.items():
        if campo == "fin_de_semana":
            fecha_cita = datetime.date.fromisoformat(cita["fecha"])
            es_finde = fecha_cita.weekday() >= 5
            if es_finde != valor_esperado:
                return False
        else:
            valor = obtener_valor(cita, campo)
            if valor != valor_esperado:
                return False
    return True

# Evaluar si la acción excluye esta cita
def es_exclusion(cita, accion):
    if accion.get("excluir") is True:
        return True
    if "excluir_edad_mayor" in accion:
        edad = obtener_valor(cita, "paciente.edad")
        if edad is not None and edad > accion["excluir_edad_mayor"]:
            return True
    return False

# Verificar si hoy corresponde aplicar la acción
def corresponde_fecha(cita, dias_antes, fecha_actual):
    fecha_cita = datetime.date.fromisoformat(cita["fecha"])
    return fecha_cita == fecha_actual + datetime.timedelta(days=dias_antes)

# Aplicar reglas a cada cita y devolver las que deben ser notificadas hoy
def filtrar_citas_por_reglas(citas, reglas, fecha_actual):
    citas_filtradas = []

    for cita in citas:
        for regla in reglas:
            condiciones = regla.get("condiciones", {})
            accion = regla.get("accion", {})

            if cumple_condiciones(cita, condiciones):
                if es_exclusion(cita, accion):
                    continue
                if "dias_antes" in accion:
                    if corresponde_fecha(cita, accion["dias_antes"], fecha_actual):
                        citas_filtradas.append(cita)
                        break
                elif "contactos_multiple" in accion:
                    for dias in accion["contactos_multiple"]:
                        if corresponde_fecha(cita, dias, fecha_actual):
                            citas_filtradas.append(cita)
                            break
    return citas_filtradas

# Filtrar citas agrupadas por centro médico usando sus reglas respectivas
resultados_por_centro = {}

# Encontt rule files (e.g., "rules_Centro_A.json", "rules_Hospital_X.json")
rule_files = glob.glob("rules_*.json")  

for rule_file in rule_files:
    centro = rule_file.replace("rules_", "").replace(".json", "").replace("_", " ")
    with open(rule_file, "r", encoding="utf-8") as f:
        reglas = json.load(f)
    citas_centro = [c for c in citas if c["centro_medico"] == centro]
    resultados_por_centro[centro] = filtrar_citas_por_reglas(citas_centro, reglas, hoy)
#Validar
centros_validos = {c["centro_medico"] for c in citas}  
for rule_file in glob.glob("rules_*.json"):
    centro = rule_file.replace("rules_", "").replace(".json", "").replace("_", " ")
    if centro not in centros_validos:
        continue  # Omitir archivos no válidos
    

# Imprimir resultados
print("Citas que deben ser notificadas hoy por centro:")
print(json.dumps(resultados_por_centro, indent=2, ensure_ascii=False))
