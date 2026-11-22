# Se importa ABC y abstractmethod para definir una clase base abstracta en POO
from abc import ABC, abstractmethod


# Se define una excepción personalizada heredando de Exception para errores de negocio
class ErrorOperacionEstacion(Exception):
    """Excepción personalizada para errores en operaciones de la estación."""

    # Se inicializa la excepción con un mensaje descriptivo y un código de error opcional
    def __init__(self, mensaje: str, codigo: str = "ERR_ESTACION"):
        # Se asigna el código de error como atributo de la instancia
        self.codigo = codigo
        # Se llama al constructor de la clase padre Exception con un texto formateado
        super().__init__(f"[{codigo}] {mensaje}")


# Se define la clase abstracta RecursoOperativo como plantilla para recursos gestionables
class RecursoOperativo(ABC):
    # Se define el método abstracto que las clases hijas deberán implementar
    @abstractmethod
    def registrar_movimiento(self, cantidad: float) -> None:
        pass


# Se define la clase TanqueCombustible que hereda de RecursoOperativo
class TanqueCombustible(RecursoOperativo):
    # Se inicializa un tanque con nombre, capacidad máxima y volumen inicial en galones
    def __init__(
        self, nombre: str, capacidad_maxima: float, volumen_actual: float = 0.0
    ):
        # Se valida que la capacidad máxima sea un número positivo
        if capacidad_maxima <= 0:
            # Se lanza ValueError si la capacidad máxima no es válida
            raise ValueError("La capacidad máxima del tanque debe ser mayor que cero.")
        # Se valida que el volumen inicial no sea negativo
        if volumen_actual < 0:
            # Se lanza ValueError si el volumen inicial es negativo
            raise ValueError("El volumen inicial no puede ser negativo.")
        # Se valida que el volumen inicial no supere la capacidad máxima
        if volumen_actual > capacidad_maxima:
            # Se lanza la excepción personalizada si se excede el límite del tanque
            raise ErrorOperacionEstacion(
                f"El volumen inicial ({volumen_actual}) supera la capacidad ({capacidad_maxima}).",
                codigo="CAP_EXCEDIDA",
            )

        # Se guarda el nombre del tanque como atributo de instancia
        self.nombre = nombre
        # Se guarda la capacidad máxima permitida
        self.capacidad_maxima = capacidad_maxima
        # Se guarda el volumen actual disponible en galones
        self.volumen_actual = volumen_actual

    # Se implementa el método para despachar (restar) combustible con control de errores
    def registrar_movimiento(self, cantidad: float) -> None:
        # Se inicia el bloque protegido para capturar errores durante el despacho
        try:
            # Se convierte la cantidad a flotante y se verifica que sea mayor que cero
            monto = float(cantidad)
            # Se comprueba que no se intente despachar cero o un valor negativo
            if monto <= 0:
                # Se lanza ValueError si la cantidad a despachar no es positiva
                raise ValueError("La cantidad a despachar debe ser mayor que cero.")
            # Se verifica si hay suficiente combustible en el tanque
            if monto > self.volumen_actual:
                # Se lanza la excepción personalizada por falta de inventario
                raise ErrorOperacionEstacion(
                    f"Inventario insuficiente en {self.nombre}. Disponible: {self.volumen_actual:.2f} gal.",
                    codigo="SIN_INVENTARIO",
                )

            # Se descuenta el volumen despachado del volumen actual
            self.volumen_actual -= monto
        # Se captura cualquier error de tipo o valor inválido
        except (ValueError, TypeError) as exc:
            # Se relanza el error con un mensaje claro para el nivel superior
            raise ErrorOperacionEstacion(
                f"Dato inválido en despacho ({self.nombre}): {exc}",
                codigo="DATO_INVALIDO",
            ) from exc
        # Se ejecuta el bloque else únicamente si el try terminó sin excepciones
        else:
            # Se confirma que la operación se completó correctamente
            print(
                f"✔ Despacho exitoso en {self.nombre}: -{monto:.2f} gal | Saldo: {self.volumen_actual:.2f} gal."
            )
        # Se ejecuta el bloque finally siempre, ocurra o no una excepción
        finally:
            # Se registra un mensaje de auditoría o cierre de transacción
            print(f"ℹ Cierre de operación en tanque '{self.nombre}'.\n")

    # Se define un método auxiliar para abastecer (sumar) combustible al tanque
    def abastecer(self, cantidad: float) -> None:
        # Se valida que la cantidad a ingresar sea numérica y positiva
        try:
            # Se convierte el valor recibido a número flotante
            ingreso = float(cantidad)
            # Se verifica que el ingreso sea mayor que cero
            if ingreso <= 0:
                # Se lanza ValueError si el valor no es positivo
                raise ValueError("El volumen de abastecimiento debe ser positivo.")
            # Se comprueba que al sumar no se supere la capacidad máxima del tanque
            if self.volumen_actual + ingreso > self.capacidad_maxima:
                # Se lanza la excepción personalizada por riesgo de rebose
                raise ErrorOperacionEstacion(
                    f"Abastecimiento excede la capacidad de {self.nombre} (Máx: {self.capacidad_maxima:.2f} gal).",
                    codigo="REBOSE_TANQUE",
                )

            # Se suma el combustible al volumen actual
            self.volumen_actual += ingreso
            # Se muestra el nuevo saldo del tanque
            print(
                f"✔ Abastecimiento exitoso en {self.nombre}: +{ingreso:.2f} gal | Saldo: {self.volumen_actual:.2f} gal."
            )
        # Se capturan errores de conversión o reglas de negocio
        except (ValueError, ErrorOperacionEstacion) as exc:
            # Se imprime el detalle del error sin detener todo el programa
            print(f"✘ Error al abastecer {self.nombre}: {exc}")
        # Se asegura un mensaje final de control
        finally:
            # Se indica el fin del intento de abastecimiento
            print(f"ℹ Verificación de nivel finalizada en '{self.nombre}'.\n")


# Se define una función para ejecutar pruebas secuenciales de validación del código
def ejecutar_pruebas_secuenciales() -> None:
    # Se imprime un encabezado para la validación secuencial
    print("=== INICIO DE VALIDACIÓN SECUENCIAL ===\n")

    # Paso 1: Crear un objeto TanqueCombustible válido
    tanque_corriente = TanqueCombustible(
        "Tanque Corriente #1", capacidad_maxima=5000.0, volumen_actual=2500.0
    )

    # Paso 2: Probar un despacho válido
    try:
        # Se intenta despachar 350 galones
        tanque_corriente.registrar_movimiento(350)
    # Se captura la excepción personalizada si ocurre algún fallo
    except ErrorOperacionEstacion as err:
        # Se informa el error capturado
        print(f"✘ Error controlado: {err}\n")

    # Paso 3: Probar un despacho mayor al inventario disponible
    try:
        # Se intenta despachar 3000 galones cuando solo hay 2150
        tanque_corriente.registrar_movimiento(3000)
    # Se captura y muestra el error controlado de inventario insuficiente
    except ErrorOperacionEstacion as err:
        # Se imprime el mensaje de la excepción
        print(f"✘ Error controlado: {err}\n")

    # Paso 4: Probar una entrada inválida (texto en lugar de número)
    try:
        # Se pasa una cadena no numérica para forzar el manejo de conversión
        tanque_corriente.registrar_movimiento("abc")
    # Se captura el error controlado de dato inválido
    except ErrorOperacionEstacion as err:
        # Se imprime el mensaje de la excepción
        print(f"✘ Error controlado: {err}\n")

    # Paso 5: Probar abastecimiento dentro de la capacidad permitida
    tanque_corriente.abastecer(1200)

    # Paso 6: Probar abastecimiento que excede la capacidad máxima del tanque
    tanque_corriente.abastecer(5000)

    # Se imprime el cierre de las pruebas secuenciales
    print("=== FIN DE VALIDACIÓN SECUENCIAL ===")


# Se verifica si el archivo se ejecuta directamente como programa principal
if __name__ == "__main__":
    # Se invoca la función de pruebas secuenciales
    ejecutar_pruebas_secuenciales()
