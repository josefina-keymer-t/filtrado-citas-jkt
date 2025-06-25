# Filtro de Citas Médicas Dinámico

En primer lugar se leyó el enunciado y se desarrollo la hoja "Apuntes Iniciales" para entender un poco el problema.
Con estos apuntes y leyendo el enunciado se fue desarrollando paso a paso el ejercicio.
<img width="689" alt="image" src="https://github.com/user-attachments/assets/d1d76d26-425e-4198-b510-8f18c7d3eb1f" />

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
- La data viene ya estructurada y limpia.
- Dentro de la base de datos están todos los datos necesarios para mostrar las citas que se deben contactar.
- Cada centro médico tiene su propio archivo de reglas (`rules_Centro_X.json`).
- Las reglas pueden contener:
  - `condiciones` (campos que deben cumplirse)
  - `accion` con una o más:
    - `dias_antes`: contacto único
    - `contactos_multiple`: varios días de contacto
    - `excluir`: excluir completamente si se cumplen condiciones
    - `excluir_edad_mayor`: excluir si edad > X
- Se puede acceder a campos anidados con `"paciente.edad"`, `"profesional.rut"`, etc.
- La ejecución ocurre diariamente, y se evalúa si hoy corresponde contactar o no.
- Se incluyen condiciones especiales como `"fin_de_semana": true`.
- Se pueden agregar nuevas condiciones fácilmente (como `paciente.apellido`, `especialidad`, etc.).
- El teléfono del paciente se incluye en el resultado para poder contactarlo.

---

## 3. Diseño conceptual del MVE

Se construyó un **script funcional y extensible** con las siguientes características:

- El sistema carga las citas desde un archivo JSON común (`bbdd.json`).
- Aplica filtros distintos por centro médico, según archivos separados de reglas.
- Las reglas están en formato JSON y son fáciles de modificar.
- La estructura:
  - Separación entre lógica de evaluación, condiciones, exclusiones y fechas.
- El sistema imprime una lista con las citas que deben ser **notificadas hoy** por cada centro.

Esto permite escalar rápidamente a nuevos centros médicos con reglas diferentes, sin modificar el código.

---

## 4. Explicación técnica del código

El archivo `main.py` ejecuta todo el proceso. Los pasos clave:

 1. Carga de citas

Lee las citas desde `bbdd.json`.

 2. Funciones auxiliares

- `obtener_valor`: permite acceder a campos anidados.
- `cumple_condiciones`: verifica si una cita cumple los filtros definidos.
- `es_exclusion`: aplica exclusiones como edad máxima o `excluir: true`.
- `corresponde_fecha`: valida si hoy es el día correcto para notificar.

 3. Lógica central

La función `filtrar_citas_por_reglas` recorre cada cita y regla:
- Si cumple condiciones → revisa si debe notificarse hoy.
- Si aplica → se agrega al resultado.
- Soporta reglas con múltiples fechas (`contactos_multiple`).

 4. Ejecución por centro

El script recorre todos los centros (A, B, C), carga sus reglas y filtra solo sus citas.

 5. Output

Imprime por pantalla un JSON con las citas que deben notificarse hoy por centro.

---

## 5. Elementos excluidos

 1. Combinaciones OR: No se incluyen casos como “si es mayor de 60 o si la especialidad es neurología”. Esto debido a que hace más complejo el diseño de las reglas y la lógica AND cubre la mayoría de los casos iniciales.
 2. Lista simple: El output es una lista con los datos necesarios para la cita, no se quitó ningún dato de la BBDD por desconocimiento a que puede ser más importante al momento de contactar al paciente, además no entrega ningún mensaje sugerido, y muestra solo las citas de hoy, sin hacer programaciones futuras, por simplicidad y porque se hace el proceso diariamente.
 3. Verificación de consistencia de las reglas: El sistema no verifica si las reglas están mal formateadas o apuntan a campos inexistentes. Si bien esto es más importante, como modelo inicial funciona y se hicieron las verificaciones manuales correspondientes, se asume que con las reglas iniciales basta por ahora y que es posible hacer una mejora más adelante en caso de ser necesario.
 4. Lógica de contacto: No se implementó lógica condicional basada en la hora (por ejemplo, “notificar solo en la mañana”) o alguna otra restricción más personalizada, esto debido a que es solo un prototipo editable para más adelante.
 5. Condiciones por rango: Más adelante se podría permitir reglas con rangos definidos en el JSON para campos como edad o fechas.
 6. Trazabilidad de reglas: Ver y analizar que reglas se han ido modificando en cada centro de salud, para ver si alguna de estas puede ayudar para otro cliente más adelante.
 7. Interfaz de edición y visualización: Similar al punto 2; es potenciable en términos de visualización con un panel automatizado que muestre las citas con filtros específicos. También visualización para la edición de las reglas (complementario al punto anterior).

---
## 6. Valor agregado

El prototipo automatiza el proceso de filtrar citas, en vez de revisar manualmente que citas cumplen con los requisitos de cada centro. 
Es dinámico y adaptable, las reglas están separadas por centro, y son fáciles de modificar y adaptar.
Sencillo de usar para gente no técnica.
Si bien es un modelo simple, es funcional y con gran capacidad de mejora.

### Parte 3

Hola Equipo de Customer Success!

Espero que vaya muy bien su semana. Les escribo para comentarles los avances sobre el filtro de citas médicas solicitado por el cliente.
Actualmente desarrollé un prototipo en donde al ejecutar el main.py, el sistema identifca automáticamente qué pacientes deben ser contactados a día de hoy, por lo cual es importante ejecutar el código diariamente.
El filtro utiliza la base de datos unificada (bbdd) y filtra las citas, devolviendo únicamente aquellas que cumplen con las reglas definidas para cada centro médico.
Los archivos de las reglas están separados por centro con el nombre rules_Centro_X, para así poder agregar o modificar las reglas según lo que requiera cada cliente.
Las reglas actuales que maneja el sistema son:
	•	Confirmar citas X días antes (ej: 2 días antes para cardiología)
	•	Realizar múltiples contactos en fechas específicas (ej: 5, 2 y 0 días antes)
	•	Excluir pacientes por edad, profesional, especialidad, día de la semana, etc.
	•	Contactar solo si es un día fin de semana
	•	Condiciones combinadas (ej: pediatría + control + menores de 15 años)
Con este sistema queda el proceso automatizado, es flexible y fácil de modificar y mejora un montón la eficiencia del equipo.
Quedo atenta a cualquier duda o comentario que tengan al respecto, además si hay alguna regla que deseen agregar o modificar, encantada de recibirla y así poder ir potenciando aún más el prototipo.

Saludos y buena semana,

Josefina

 
