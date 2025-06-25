# Filtro de Citas Médicas Dinámico

En primer lugar se leyó el enunciado y se desarrollo la hoja "Apuntes Iniciales" para entender un poco el problema.
Con estos apuntes y leyendo el enunciado se fue desarrollando paso a paso el ejercicio.

---

## 1. Reformulación del problema

En Cero se gestionan miles de citas médicas de distintos centros de salud en varios países.

La plataforma debe ser adaptable y fácil de modificar; ya que se deben hacer constantes mejoras o ajustes según lo que requiera el cliente.

Algunas de las restricciones:

- Tipo de tto.
- Exámenes con distintas cantidades de  confirmación (0-X)
- Datos Doctores: Rut, Nombre, Centro Médico, # Contacto, Especialidad, Tipo Tto.
- Filtros combinados: Tipo tto, Centro Médico, Especialidad
- Exclusiones específicas*
- Recordatorios

Cada centro médico tiene sus **propias reglas y tienen agendas individuales.**

Sistemas Proporcionan APIs con **datos** distintos según la institución, pero mantienen **generalidad**.

Se cargan las citas programadas **diariamente** en cada sistema y se aplican las reglas correspondientes.

Es decir, se debe notificar a que pacientes corresponde contactar y contactarlos.

El objetivo inicial es diseñar el filtro de las citas. El **output**: citas que cumplan con las restricciones específicas de cada centro. 

Filtros **dinámicos y adaptables:** Cada centro, doctor, tto, etc. puede tener sus propias reglas o cambiarlas durante el tiempo.

MVE: Desarrollar soluciones **funcionales**, que pueden ser no las más desarrolladas, pero que si cumplen con el objetivo inicial y se pueden (deben) ir **mejorando con flujo del proceso** a través del feedback, observaciones u otras posibles modificaciones.

## 2. Supuestos del problema

- Todos los centros usan la **misma estructura de citas** (`bbdd.json`).
- Cada centro médico tiene su propio archivo de reglas (`rules_Centro_X.json`).
- Las reglas pueden contener:
  - `condiciones` (campos que deben cumplirse)
  - `accion` con una o más:
    - `dias_antes`: contacto único
    - `contactos_multiple`: varios días de contacto
    - `excluir`: excluir completamente si se cumplen condiciones
    - `excluir_edad_mayor`: excluir si edad > X
- Se puede acceder a campos anidados con `"paciente.edad"`, `"profesional.rut"`, etc.
- La ejecución ocurre diariamente, y se evalúa si **hoy** corresponde contactar o no.
- Se incluyen condiciones especiales como `"fin_de_semana": true`.
- Se pueden agregar nuevas condiciones fácilmente (como `paciente.apellido`, `especialidad`, etc.).
- El teléfono del paciente se incluye en el resultado.

---

## 3. Diseño conceptual del MVE

Se construyó un **script funcional y extensible** con las siguientes características:

- El sistema carga las citas desde un archivo JSON común (`bbdd.json`).
- Aplica filtros distintos por centro médico, según archivos separados de reglas.
- Las reglas están en formato JSON y son fáciles de modificar.
- La estructura es modular:
  - Separación entre lógica de evaluación, condiciones, exclusiones y fechas.
- El sistema imprime una lista con las citas que deben ser **notificadas hoy** por cada centro.

Esto permite escalar rápidamente a nuevos centros médicos con reglas diferentes, sin modificar el código.

---

## 4. Explicación técnica del código

El archivo `main.py` ejecuta todo el proceso. Los pasos clave:

# 1. Carga de citas

Lee las citas desde `bbdd.json`.

# 2. Funciones auxiliares

- `obtener_valor`: permite acceder a campos anidados.
- `cumple_condiciones`: verifica si una cita cumple los filtros definidos.
- `es_exclusion`: aplica exclusiones como edad máxima o `excluir: true`.
- `corresponde_fecha`: valida si hoy es el día correcto para notificar.

# 3. Lógica central

La función `filtrar_citas_por_reglas` recorre cada cita y regla:
- Si cumple condiciones → revisa si debe notificarse hoy.
- Si aplica → se agrega al resultado.
- Soporta reglas con múltiples fechas (`contactos_multiple`).

# 4. Ejecución por centro

El script recorre todos los centros (A, B, C), carga sus reglas y filtra solo sus citas.

# 5. Output

Imprime por pantalla un JSON con las citas que deben notificarse hoy por centro.

---

##
