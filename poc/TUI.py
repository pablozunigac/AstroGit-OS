import sys

from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, VSplit, Window
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import Box, Button, Frame, Label

# MENU
OPCIONES = {
    "1. CANONICAL STATES",
    "2. SUBSYSTEMS STATES",
    "3. COMPOUND STATES",
    "- CONFIG",
    "- EXIT",
}

# Variable global para mantener el texto de la pantalla de detalles
texto_detalle = Label(text="SELECT AN OPTION & PRESS ENTER")


def crear_tui():
    kb = KeyBindings()
    lista_botones = []

    # SELECTING AN OPTION
    def accionar_boton(nombre_opcion):
        def handler():
            if nombre_opcion == "- EXIT":
                sys.exit(0)
            else:
                texto_detalle.text = f"--- [ MÓDULO: {nombre_opcion.upper()} ] ---\n\n{OPCIONES[nombre_opcion]}\n\n(PRESS 'Tab' TO BACK TO MENU)"

        return handler

    # Generamos los botones dinámicamente basados en nuestro diccionario
    for nombre in OPCIONES:
        btn = Button(text=nombre, handler=accionar_boton(nombre))
        lista_botones.append(btn)

    # 3. Atajos de teclado esenciales
    @kb.add("tab")
    def ir_al_siguiente(event):
        """Moverse entre botones con el Tabulador"""
        event.app.layout.focus_next()

    @kb.add("s-tab")
    def ir_al_anterior(event):
        """Moverse hacia atrás con Mayús + Tab (Shift+Tab)"""
        event.app.layout.focus_previous()

    @kb.add("c-c")
    def salir_forzado(event):
        """Cerrar la consola inmediatamente con Ctrl + C"""
        event.app.exit()

    # 4. Diseño de la interfaz (Layout)
    # Columna izquierda: Menú de botones estructurado verticalmente
    columna_menu = Frame(
        title="Menú de Control", body=HSplit(lista_botones, padding=2), width=40
    )

    # Columna derecha: Espacio dinámico para ver el contenido de la opción
    columna_contenido = Frame(
        title="Panel de Visualización", body=Box(texto_detalle, padding=1)
    )

    # Unimos ambas columnas en una vista horizontal (Split)
    diseño_principal = VSplit(
        [
            columna_menu,
            Window(width=2, char="│"),  # Línea divisoria estética
            columna_contenido,
        ]
    )

    # 5. Inicialización de la Aplicación
    app = Application(
        layout=Layout(diseño_principal),
        key_bindings=kb,
        full_screen=True,  # Hace que use toda la ventana de la terminal
    )

    return app


if __name__ == "__main__":
    aplicacion = crear_tui()
    aplicacion.run()
