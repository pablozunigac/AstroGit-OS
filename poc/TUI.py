import sys
from datetime import datetime, timezone

from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings, KeyPressEvent
from prompt_toolkit.layout.containers import HSplit, VSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import Box, Frame

# HARDWARE SUBSYSTEM ENTITIES (For Query, Management, Update)
HARDWARE_ENTITIES = {
    "1": (
        "DOME",
        "Dome management, shutter control, windscreen, and environmental status.",
    ),
    "2": (
        "MOUNT",
        "Telescope mount, altazimuth axes drive, and tracking telemetry.",
    ),
    "3": (
        "OPTICS",
        "Mirrors, adaptive optics, and active collimation.",
    ),
    "4": (
        "INSTRUMENTATION",
        "Imagers, spectrographs, and science acquisition sensors.",
    ),
}

# RECONCILIATION / TOPOLOGY ENTITIES (For Config)
CONFIG_ENTITIES = {
    "1": (
        "RECONCILIATION",
        "State convergence policy, auto-heal triggers, and drift resolution.",
    ),
    "2": (
        "SUMMIT NODE",
        "Summit local node synchronization and real-time edge parameters.",
    ),
    "3": (
        "BASE NODE",
        "Base station staging repository and local cache parameters.",
    ),
    "4": (
        "CLOUD NODE",
        "Cloud replica synchronization, long-term history, and remote upstream.",
    ),
}

# MAIN MENU STRUCTURE
MENU_STRUCTURE = {
    "1": {
        "label": "OVERVIEW",
        "desc": "Executive SCADA dashboard: global state, network drift, and system health.",
        "type": "ACTION",
    },
    "2": {
        "label": "QUERY",
        "desc": "Query live subsystem state vectors (As-Is), telemetry, and metric drifts.",
        "type": "SUBMENU",
        "items": HARDWARE_ENTITIES,
    },
    "3": {
        "label": "MANAGEMENT",
        "desc": "Manage local staging drafts, branch isolation, and configuration diffs.",
        "type": "SUBMENU",
        "items": HARDWARE_ENTITIES,
    },
    "4": {
        "label": "UPDATE",
        "desc": "Authorize state changes, commit, merge, and promote baseline state (To-Be).",
        "type": "SUBMENU",
        "items": HARDWARE_ENTITIES,
    },
    "5": {
        "label": "CONFIG",
        "desc": "Reconciliation engine settings, node synchronization, and network parameters.",
        "type": "SUBMENU",
        "items": CONFIG_ENTITIES,
    },
}


class AppState:
    def __init__(self) -> None:
        self.level: str = "HOME"  # "HOME" or "SUBMENU"
        self.module_key: str | None = None
        self.entity_key: str | None = None
        self.focus_index: int = 0  # Index for Tab / Arrow navigation


state = AppState()
left_text_control = FormattedTextControl()
right_header_control = FormattedTextControl()
right_body_control = FormattedTextControl()


def render_scada_overview() -> str:
    """Generates a minimal, executive SCADA-like dashboard overview."""
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    return (
        f"TIMESTAMP : {now_utc}\n"
        f"ENGINE    : ASTROGIT-OS CORE v0.2\n"
        f"HEALTH    : NOMINAL [100%]\n"
        f"DRIFT     : 0.005s (SYNCHRONIZED)\n"
        f"──────────┬────────────────────────────────────────────────────\n"
        f" SUBSYS   │ STATE      LATENCY      LAST COMMITTED BASELINE    \n"
        f"──────────┼────────────────────────────────────────────────────\n"
        f" DOME     │ OK         835   ms     commit-e8f192a (5m ago)    \n"
        f" MOUNT    │ OK         55    ms     commit-e8f192a (5m ago)    \n"
        f" OPTICS   │ OK         34    ms     commit-a410f91 (1h ago)    \n"
        f" INSTR    │ ACTIVE     12    ms     commit-a410f91 (1h ago)    \n"
        f"──────────┴────────────────────────────────────────────────────\n"
        f" TOPOLOGY : SUMMIT [PRIMARY] <-> BASE [SYNC] <-> CLOUD [OK] "
    )


def get_current_options() -> list[tuple[str, str]]:
    """Returns a list of tuples (key_str, label_str) for the active level."""
    if state.level == "HOME" or state.module_key is None:
        opts = [(k, str(v["label"])) for k, v in MENU_STRUCTURE.items()]
        opts.append(("0", "EXIT"))
        return opts
    else:
        mod = MENU_STRUCTURE[state.module_key]
        items = mod.get("items", {})
        opts = [(k, items[k][0]) for k in items]
        opts.append(("8", "BACK"))
        opts.append(("9", "HOME"))
        opts.append(("0", "EXIT"))
        return opts


def update_views() -> None:
    options = get_current_options()

    # 1. RENDER LEFT PANEL
    lines = []
    for i, (key, label) in enumerate(options):
        cursor = "► " if i == state.focus_index else "  "
        lines.append(f"{cursor}[{key}] {label}")
    left_text_control.text = "\n".join(lines)

    # 2. RENDER BREADCRUMB AND CONTROL PANEL CONTENT
    if state.level == "HOME" or state.module_key is None:
        if state.focus_index < len(MENU_STRUCTURE):
            selected_key = options[state.focus_index][0]
            selected_item = MENU_STRUCTURE[selected_key]
            route = f"ASTROGIT-OS > {selected_item['label']}"

            if selected_key == "1":  # OVERVIEW Selected
                desc = render_scada_overview()
            else:
                desc = str(selected_item["desc"])
        else:
            route = "ASTROGIT-OS > EXIT"
            desc = "Terminate active operational session."
    else:
        mod_info = MENU_STRUCTURE[state.module_key]
        mod_label = mod_info["label"]
        items = mod_info.get("items", {})
        num_items = len(items)

        if state.focus_index < num_items:
            entity_key = options[state.focus_index][0]
            entity_label, entity_desc = items[entity_key]
            route = f"ASTROGIT-OS > {mod_label} > {entity_label}"
            desc = f"Target Entity: {entity_label}\n\n{entity_desc}"
        elif options[state.focus_index][0] == "8":
            route = f"ASTROGIT-OS > {mod_label} > BACK"
            desc = "Return to previous hierarchy level."
        elif options[state.focus_index][0] == "9":
            route = f"ASTROGIT-OS > {mod_label} > HOME"
            desc = "Return directly to root menu."
        else:
            route = f"ASTROGIT-OS > {mod_label} > EXIT"
            desc = "Terminate active operational session."

    right_header_control.text = f"ROUTE: {route}"
    right_body_control.text = desc


def execute_selection() -> None:
    options = get_current_options()
    key = options[state.focus_index][0]
    process_key(key)


def process_key(key: str) -> None:
    if state.level == "HOME":
        if key == "1":
            # Overview stays on Home level, showing the SCADA dashboard
            pass
        elif key in MENU_STRUCTURE:
            state.module_key = key
            state.level = "SUBMENU"
            state.focus_index = 0
        elif key == "0":
            sys.exit(0)

    elif state.level == "SUBMENU":
        if state.module_key is not None:
            mod_info = MENU_STRUCTURE[state.module_key]
            items = mod_info.get("items", {})
            if key in items:
                state.entity_key = key
                # Entity action execution point
                pass
            elif key == "8":  # BACK (One level up)
                state.level = "HOME"
                state.module_key = None
                state.focus_index = 0
            elif key == "9":  # HOME (Reset to root)
                state.level = "HOME"
                state.module_key = None
                state.focus_index = 0
            elif key == "0":
                sys.exit(0)

    update_views()


def move_focus(delta: int) -> None:
    options = get_current_options()
    state.focus_index = (state.focus_index + delta) % len(options)
    update_views()


def create_tui() -> Application:
    kb = KeyBindings()

    # Direct digit shortcuts [0-9]
    for digit in [str(d) for d in range(10)]:

        def register_key(d: str = digit) -> None:
            @kb.add(d)
            def _(event: KeyPressEvent) -> None:
                process_key(d)

        register_key()

    @kb.add("tab")
    @kb.add("down")
    def _(event: KeyPressEvent) -> None:
        move_focus(1)

    @kb.add("s-tab")
    @kb.add("up")
    def _(event: KeyPressEvent) -> None:
        move_focus(-1)

    @kb.add("enter")
    def _(event: KeyPressEvent) -> None:
        execute_selection()

    @kb.add("c-c")
    def _(event: KeyPressEvent) -> None:
        event.app.exit()

    # Layout framing and containers
    left_panel = Frame(
        title="ASTROGIT-OS",
        body=Window(content=left_text_control, dont_extend_height=False),
        width=36,
    )

    right_panel_content = HSplit(
        [
            Window(content=right_header_control, height=1, style="bold #00ff00"),
            Window(height=1, char="─"),
            Window(content=right_body_control),
        ]
    )

    right_panel = Frame(title="CONTROL PANEL", body=Box(right_panel_content, padding=1))

    footer = Window(
        content=FormattedTextControl(
            " NAV: [Tab/Arrows/Digits]  EXEC: [Enter]  BACK: [8]  HOME: [9]  QUIT: [Ctrl+C] "
        ),
        height=1,
        style="bg:#333333 #ffffff",
    )

    body = VSplit([left_panel, Window(width=1, char="│"), right_panel])

    # Initial view state render
    update_views()

    layout = Layout(HSplit([body, footer]))
    return Application(layout=layout, key_bindings=kb, full_screen=True)


if __name__ == "__main__":
    app = create_tui()
    app.run()
