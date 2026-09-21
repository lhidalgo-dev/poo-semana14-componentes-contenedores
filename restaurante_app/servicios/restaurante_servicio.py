from modelos.producto import Producto
from modelos.usuario import Usuario


class RestauranteServicio:
    def __init__(self, archivo_servicio) -> None:
        self.archivo_servicio = archivo_servicio
        self.usuarios: list[Usuario] = []
        self.productos: list[Producto] = []
        self.cargar_datos()

    def cargar_datos(self) -> None:
        # Carga los datos persistidos en JSON y los convierte en objetos del dominio.
        usuarios_json = self.archivo_servicio.leer_json("usuarios.json")
        productos_json = self.archivo_servicio.leer_json("productos.json")

        self.usuarios = []
        for datos in usuarios_json:
            try:
                usuario = Usuario(
                    datos.get("identificacion", ""),
                    datos.get("nombre", ""),
                    datos.get("usuario", ""),
                    datos.get("contrasena", ""),
                )
                self.usuarios.append(usuario)
            except ValueError as error:
                print(f"Se encontro un usuario con datos invalidos: {error}")

        self.productos = []
        for datos in productos_json:
            try:
                producto = Producto(
                    datos.get("codigo", ""),
                    datos.get("nombre", ""),
                    datos.get("precio", 0),
                    datos.get("categoria", ""),
                    datos.get("stock", 0),
                )
                self.productos.append(producto)
            except ValueError as error:
                print(f"Se encontro un producto con datos invalidos: {error}")

    def validar_acceso(self, usuario: str, contrasena: str) -> Usuario | None:
        # Recorre los usuarios cargados y delega la comparacion a cada objeto.
        for usuario_registrado in self.usuarios:
            if usuario_registrado.validar_credenciales(usuario, contrasena):
                return usuario_registrado
        return None

    def listar_usuarios(self) -> list[Usuario]:
        # Entrega los usuarios cargados para que la interfaz los muestre.
        return self.usuarios.copy()

    def listar_productos(self) -> list[Producto]:
        # Entrega los productos cargados para que la interfaz los muestre.
        return self.productos.copy()

    def cantidad_usuarios(self) -> int:
        return len(self.usuarios)

    def cantidad_productos(self) -> int:
        return len(self.productos)

    def buscar_producto_por_codigo(self, codigo: str) -> Producto | None:
        # Localiza un producto ya cargado a partir de su codigo.
        codigo_normalizado = Producto.normalizar_codigo(codigo)
        for producto in self.productos:
            if producto.codigo == codigo_normalizado:
                return producto
        return None

    def guardar_productos(self) -> None:
        # Persiste el estado actual de productos en productos.json.
        datos = [producto.convertir_a_diccionario() for producto in self.productos]
        self.archivo_servicio.escribir_json("productos.json", datos)

    def registrar_producto(
        self,
        codigo: str,
        nombre: str,
        precio: float,
        categoria: str,
        stock: int,
    ) -> Producto:
        # Valida los datos mediante el modelo antes de agregar el producto.
        nuevo_producto = Producto(codigo, nombre, precio, categoria, stock)

        if self.buscar_producto_por_codigo(nuevo_producto.codigo) is not None:
            raise ValueError("Ya existe un producto registrado con ese codigo.")

        self.productos.append(nuevo_producto)
        self.guardar_productos()
        return nuevo_producto

    def actualizar_producto(
        self,
        codigo: str,
        nombre: str,
        precio: float,
        categoria: str,
        stock: int,
    ) -> Producto:
        # El codigo identifica al producto existente; el resto se actualiza.
        producto_actual = self.buscar_producto_por_codigo(codigo)

        if producto_actual is None:
            raise ValueError("No existe un producto registrado con ese codigo.")

        datos_validados = Producto(codigo, nombre, precio, categoria, stock)
        producto_actual.nombre = datos_validados.nombre
        producto_actual.precio = datos_validados.precio
        producto_actual.categoria = datos_validados.categoria
        producto_actual.stock = datos_validados.stock

        self.guardar_productos()
        return producto_actual

    def eliminar_producto(self, codigo: str) -> Producto:
        # Quita el producto de la lista en memoria y actualiza el archivo.
        producto_actual = self.buscar_producto_por_codigo(codigo)

        if producto_actual is None:
            raise ValueError("No existe un producto registrado con ese codigo.")

        self.productos.remove(producto_actual)
        self.guardar_productos()
        return producto_actual
