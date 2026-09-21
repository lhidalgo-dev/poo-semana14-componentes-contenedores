# restaurante_app — Semana 14

**Estudiante:** Leython Josue Hidalgo Valdez  
**Asignatura:** Programación Orientada a Objetos  
**Tema:** Componentes y contenedores  

---

## Propósito de esta semana

Esta entrega evoluciona `restaurante_app` a partir de la base gráfica construida
en la Semana 13. El objetivo central es aplicar correctamente **componentes y
contenedores de Tkinter/ttk** para transformar la interfaz de productos en una
experiencia de gestión completa: registro, consulta, actualización y
eliminación, manteniendo la arquitectura modular y la persistencia en JSON ya
existentes. No se modifica la estructura de carpetas ni las clases base: la
evolución ocurre principalmente dentro de `ui/main_view.py` y se amplía
`RestauranteServicio` con las operaciones que la nueva interfaz necesita.

## Estructura del proyecto

```
restaurante_app/
├── datos/
│   ├── productos.json
│   └── usuarios.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   └── usuario.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
└── main.py
```

## Responsabilidad de cada capa

| Capa | Responsabilidad |
|------|------------------|
| `modelos/` | Representan `Producto` y `Usuario`, con validaciones mediante `property` (código, precio, categoría, stock, credenciales). |
| `servicios/archivo_servicio.py` | Lee y escribe los archivos JSON de `datos/`, manejando `FileNotFoundError`, `json.JSONDecodeError` y `PermissionError`. |
| `servicios/restaurante_servicio.py` | Convierte los datos JSON en objetos, valida el acceso, y expone el CRUD completo de productos (`registrar_producto`, `buscar_producto_por_codigo`, `actualizar_producto`, `eliminar_producto`, `guardar_productos`). |
| `ui/` | Vistas Tkinter (`LoginView`, `MainView`) que solicitan las operaciones a `RestauranteServicio`; no leen ni escriben los archivos JSON directamente. |
| `main.py` | Crea la única ventana principal (`Tk`), prepara los servicios y controla el cambio entre vistas. |

## Componentes y contenedores utilizados

- **`Frame`**: contenedores para separar encabezado, barra de navegación, área
  de contenido y barra de estado dentro de `MainView`.
- **`LabelFrame`**: agrupa visualmente el formulario ("Datos del producto") y
  el listado ("Productos registrados" / "Consulta de usuarios"), dejando clara
  la separación entre la zona de captura de datos y la de presentación.
- **`Entry`**: campos de código, nombre y precio del producto, y credenciales
  de acceso.
- **`ttk.Combobox`** (modo `readonly`): selector de categoría restringido a
  las categorías válidas del modelo (`ENTRADA`, `PLATO_FUERTE`, `POSTRE`,
  `BEBIDA`, `SNACK`), evitando que el usuario escriba una categoría inválida.
- **`ttk.Spinbox`**: selector numérico para el stock del producto, apropiado
  para una cantidad entera acotada.
- **`ttk.Treeview` + `ttk.Scrollbar`**: tablas con encabezados para mostrar
  productos y usuarios de forma organizada, con desplazamiento vertical.
- **`ttk.Button` / `ttk.Style`**: botones de acción (`Registrar`,
  `Cargar / Consultar`, `Actualizar`, `Eliminar`, `Limpiar`) conectados
  mediante `command=`, con estilos que distinguen visualmente acciones
  primarias, secundarias y destructivas.
- **Gestores de geometría**: `pack()` para la estructura general de la
  ventana (encabezado, navegación, contenido, estado) y `grid()` dentro del
  formulario y del área de productos, para alinear etiquetas, campos y el
  bloque formulario/listado con precisión.

## Mejoras realizadas en la interfaz

- La sección **Productos** pasó de una lista de solo lectura a un panel
  completo con formulario y tabla, organizados en contenedores independientes.
- Se agregó la sección **Inicio** con tarjetas resumen (cantidad de productos
  y usuarios registrados), aprovechando contenedores reutilizables.
- La barra de navegación resalta la sección activa (`MenuActivo.TButton`)
  para orientar mejor al usuario.
- La sección **Usuarios** ahora presenta la información en una tabla
  (`Treeview`) en lugar de etiquetas apiladas manualmente.
- Cada operación sobre productos actualiza inmediatamente la tabla y la barra
  de estado inferior, confirmando el resultado al usuario.

## Operaciones implementadas sobre productos

| Operación | Acción en la interfaz | Método en `RestauranteServicio` |
|-----------|------------------------|----------------------------------|
| Registrar | Botón **Registrar** | `registrar_producto(codigo, nombre, precio, categoria, stock)` |
| Consultar | Botón **Cargar / Consultar** (por código) | `buscar_producto_por_codigo(codigo)` |
| Actualizar | Botón **Actualizar** | `actualizar_producto(codigo, nombre, precio, categoria, stock)` |
| Eliminar | Botón **Eliminar** | `eliminar_producto(codigo)` |

Todas las validaciones (campos vacíos, precio no numérico o negativo,
categoría inválida, stock no entero o negativo, código duplicado) se
resuelven dentro del modelo `Producto` y de `RestauranteServicio`; la interfaz
únicamente captura los datos y muestra el resultado mediante `messagebox`.

## Persistencia

Los cambios sobre productos (registrar, actualizar, eliminar) se guardan de
inmediato en `datos/productos.json` a través de
`RestauranteServicio.guardar_productos()`, que delega la escritura en
`ArchivoServicio`. Al reabrir la aplicación, los datos modificados se
mantienen.

## Flujo de la aplicación

```
Inicio de la aplicación
        ↓
main.py prepara Tkinter y los servicios
        ↓
LoginView → validación mediante RestauranteServicio
        ↓
MainView
        ↓
Inicio (resumen) | Usuarios (consulta) | Productos (formulario + tabla)
        ↓
Registrar | Cargar/Consultar | Actualizar | Eliminar
        ↓
RestauranteServicio procesa la operación y persiste en productos.json
        ↓
Actualización de la tabla y de la barra de estado
```

## Credenciales de acceso (demostración)

| Usuario | Contraseña |
|---------|------------|
| `leython` | `rest2026` |
| `admin` | `admin123` |

## Nota educativa sobre autenticación

El acceso de esta etapa es una **simulación pedagógica**. Las contraseñas se
guardan en JSON en texto plano únicamente con fines didácticos; esto no
representa una práctica segura para un sistema real.

## Requisitos

- Python 3.10 o superior
- Tkinter disponible en la instalación de Python (no requiere dependencias externas)

## Cómo ejecutar

```bash
cd restaurante_app
python main.py
```

En Windows, si `python` no está disponible en la terminal, puede usarse:

```bash
py main.py
```

## Pruebas realizadas

1. Se ejecuta `main.py` y la aplicación inicia sin errores.
2. El acceso mediante usuario y contraseña continúa funcionando.
3. La interfaz principal se muestra correctamente después del acceso.
4. La sección **Usuarios** permite consultar la información registrada en una tabla.
5. La sección **Productos** presenta un formulario organizado mediante componentes y contenedores.
6. Se registra un nuevo producto y aparece de inmediato en la tabla.
7. Se carga/consulta un producto existente mediante su código.
8. Se actualiza la información de un producto y los cambios se conservan.
9. Se elimina un producto y deja de aparecer en la tabla.
10. Las modificaciones se mantienen después de cerrar y volver a ejecutar la aplicación.
11. La interfaz solicita las operaciones a `RestauranteServicio` y no manipula directamente `productos.json`.
12. La navegación y los controles resultan claros: barra superior, formulario, tabla y barra de estado.

## Próxima evolución

En las siguientes semanas se incorporará la gestión completa de ventas y
pedidos dentro de la misma arquitectura de componentes y contenedores.
