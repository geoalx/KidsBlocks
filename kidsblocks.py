#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kid Blocks — emojis + Times New Roman + embedded logos, 2-row toolbar
"""

import base64
from io import BytesIO
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

# Pillow for decoding embedded images
try:
    from PIL import Image, ImageTk
    PIL_OK = True
except Exception:
    PIL_OK = False

# ========= Embedded logos (pre-scaled PNG, base64) =========
# 1) owl
LOGO1_B64 = """
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
""".strip()

# 2) NTUA
LOGO2_B64 = """
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
""".strip()

# 3) µLab chip
LOGO3_B64 = """
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
""".strip()

# NOTE: The three base64 strings are large. If you see “(snip in this preview)” above,
# your chat viewer truncated them. Ask me to “paste full base64” and I’ll drop the
# three full strings verbatim.

# ----- World/grid metrics -----
NODE_SIZE = 100
PORT_SIZE = 12
GRID_SIZE = 20

# Colors
COLOR_BG = "#ffffff"
COLOR_OUTLINE = "#7c8aa5"
COLOR_TEXT = "#1f2937"
COLOR_BLOCK_INPUT = "#ffedd5"
COLOR_BLOCK_ADD = "#d1fae5"
COLOR_BLOCK_MUL = "#e0e7ff"
COLOR_BLOCK_OUTPUT = "#fde68a"
COLOR_PORT = "#94a3b8"
COLOR_WIRE = "#64748b"

def font_size(base, zoom):
    s = int(round(base * (0.8 + 0.2*zoom)))
    return max(8, min(36, s))

def pick_times_font(root):
    fams = set(root.tk.call("font", "families"))
    return "Times New Roman" if "Times New Roman" in fams else "Times"

# ---------- Tooltip ----------
class Tooltip:
    def __init__(self, parent, font_tuple=("Times New Roman", 12)):
        self.parent = parent
        self.tip = None
        self.label = None
        self.font_tuple = font_tuple

    def show(self, text, x_screen, y_screen):
        if self.tip is None:
            self.tip = tk.Toplevel(self.parent)
            self.tip.wm_overrideredirect(True)
            try: self.tip.attributes("-topmost", True)
            except Exception: pass
            self.label = tk.Label(
                self.tip, text=text, justify="left",
                background="#0f172a", foreground="#f8fafc",
                relief="solid", borderwidth=1, padx=12, pady=8,
                font=self.font_tuple
            )
            self.label.pack()
        else:
            self.label.configure(text=text)
        self.tip.wm_geometry("+%d+%d" % (int(x_screen+16), int(y_screen+16)))

    def hide(self):
        if self.tip is not None:
            try: self.tip.destroy()
            except Exception: pass
            self.tip = None
            self.label = None

# ---------- Model ----------
class Port:
    def __init__(self, node, kind, index=0, label=""):
        assert kind in ("in", "out")
        self.node = node
        self.kind = kind
        self.index = index
        self.label = label
    def position_world(self):
        x, y = self.node.x, self.node.y
        if self.kind == "in":
            n = len(self.node.inputs)
            yy = y + (NODE_SIZE/2 if n <= 1 else (NODE_SIZE/(n+1))*(self.index+1))
            return (x, yy)
        else:
            n = len(self.node.outputs)
            yy = y + (NODE_SIZE/2 if n <= 1 else (NODE_SIZE/(n+1))*(self.index+1))
            return (x + NODE_SIZE, yy)

class Node:
    _id_counter = 1
    def __init__(self, app, x, y, title="", fill="#e5e7eb"):
        self.app = app
        self.id = Node._id_counter; Node._id_counter += 1
        self.x = x; self.y = y
        self.title = title
        self.inputs = []; self.outputs = []
        self.selected = False
        self.value = None
        self.fill = fill
        self.sim_value = None; self.next_sim_value = None
    def bbox_world(self): return (self.x, self.y, self.x + NODE_SIZE, self.y + NODE_SIZE)
    def add_input(self, label=""):
        p = Port(self, "in", len(self.inputs), label=label); self.inputs.append(p); return p
    def add_output(self, label=""):
        p = Port(self, "out", len(self.outputs), label=label); self.outputs.append(p); return p
    def hit_test_world(self, wx, wy):
        x1, y1, x2, y2 = self.bbox_world(); return x1 <= wx <= x2 and y1 <= wy <= y2
    def port_hit_world(self, wx, wy):
        s = max(6, int(PORT_SIZE)); half = s/2
        for port in self.inputs + self.outputs:
            cx, cy = port.position_world()
            if (cx - half) <= wx <= (cx + half) and (cy - half) <= wy <= (cy + half):
                return port
        return None
    def draw(self, canvas):
        z = self.app.zoom
        x1w, y1w, x2w, y2w = self.bbox_world()
        x1, y1 = self.app.to_view_pt(x1w, y1w); x2, y2 = self.app.to_view_pt(x2w, y2w)
        outline = "#4b5563" if self.selected else COLOR_OUTLINE
        canvas.create_rectangle(x1, y1, x2, y2, fill=self.fill, outline=outline, width=max(2, int(3*z)), tags=("node", f"node{self.id}"))
        canvas.create_line(x1, y2, x2, y2, fill="#cbd5e1", width=max(2, int(3*z)))
        canvas.create_line(x2, y1, x2, y2, fill="#cbd5e1", width=max(2, int(3*z)))
        if self.title:
            canvas.create_text(x1+int(8*z), y1+int(10*z), text=self.title, anchor="w",
                               font=(self.app.FONT_FAM, font_size(9, z), "bold"), fill=COLOR_TEXT)
        if self.value is not None:
            canvas.create_text(x1+int(8*z), y2-int(10*z), text=f"τιμή: {self.value}", anchor="w",
                               font=(self.app.FONT_FAM, font_size(9, z)), fill="#374151")
        ps = max(8, int(PORT_SIZE * z)); half = ps//2
        for p in self.inputs + self.outputs:
            cxw, cyw = p.position_world(); cx, cy = self.app.to_view_pt(cxw, cyw)
            canvas.create_rectangle(cx-half, cy-half, cx+half, cy+half, fill=COLOR_PORT, outline="#475569",
                                    width=max(2, int(2*z)), tags=("port",))
    def configure(self): pass
    def evaluate(self, memo, stack): raise NotImplementedError

class InputNode(Node):
    def __init__(self, app, x, y, value=0):
        super().__init__(app, x, y, title="🔢 Είσοδος", fill=COLOR_BLOCK_INPUT)
        self.add_output("out")
        self.input_value = int(value)
        self.value = self.input_value
        self.sim_value = self.input_value
        self.next_sim_value = self.input_value
    def draw(self, canvas):
        super().draw(canvas); z = self.app.zoom
        x1w, y1w, x2w, y2w = self.bbox_world()
        x1, y1 = self.app.to_view_pt(x1w, y1w); x2, y2 = self.app.to_view_pt(x2w, y2w)
        canvas.create_text((x1+x2)//2, (y1+y2)//2, text=str(self.input_value),
                           font=(self.app.FONT_FAM, font_size(22, z), "bold"), fill="#9a3412")
    def configure(self):
        val = simpledialog.askinteger("Τιμή εισόδου", "Δώσε ακέραιο:",
                                      initialvalue=self.input_value, parent=self.app.root)
        if val is not None:
            self.input_value = int(val); self.value = self.input_value; self.app.redraw()
    def evaluate(self, memo, stack):
        memo[self] = self.input_value; self.value = self.input_value; return self.input_value

class OpNode(Node):
    def __init__(self, app, x, y, op="+", energy_cost=1.0, area_cost=1.0):
        fill = COLOR_BLOCK_ADD if op == "+" else COLOR_BLOCK_MUL
        super().__init__(app, x, y, title="", fill=fill)
        self.add_input("A"); self.add_input("B"); self.add_output("out")
        self.op = op; self.energy_cost = float(energy_cost); self.area_cost = float(area_cost)
        self.sim_value = "X"; self.next_sim_value = "X"; self.value = "X"
    def draw(self, canvas):
        super().draw(canvas); z = self.app.zoom
        x1w, y1w, x2w, y2w = self.bbox_world(); x1, y1 = self.app.to_view_pt(x1w, y1w); x2, y2 = self.app.to_view_pt(x2w, y2w)
        symbol = "➕" if self.op == "+" else "✖"
        canvas.create_text((x1+x2)//2, (y1+y2)//2, text=symbol,
                           font=(self.app.FONT_FAM, font_size(36, z), "bold"),
                           fill="#065f46" if self.op == "+" else "#3730a3")
        tag = f"Ε:{self.energy_cost:g}  Α:{self.area_cost:g}"
        canvas.create_text(x2-int(8*z), y1+int(10*z), text=tag, anchor="e",
                           font=(self.app.FONT_FAM, font_size(9, z)), fill="#334155")
    def configure(self):
        win = tk.Toplevel(self.app.root); win.title("Πράξη"); win.transient(self.app.root); win.resizable(False, False)
        choice = tk.StringVar(value=self.op); energy = tk.StringVar(value=str(self.energy_cost)); area = tk.StringVar(value=str(self.area_cost))
        frm = ttk.Frame(win, padding=12); frm.pack(fill="both", expand=True)
        ttk.Label(frm, text="Πράξη:").grid(row=0, column=0, sticky="w", pady=(0,6))
        ttk.Radiobutton(frm, text="A + B", variable=choice, value="+").grid(row=0, column=1, sticky="w", pady=(0,6))
        ttk.Radiobutton(frm, text="A × B", variable=choice, value="*").grid(row=0, column=2, sticky="w", pady=(0,6))
        ttk.Label(frm, text="Ενεργειακό κόστος ανά βήμα:").grid(row=1, column=0, sticky="w", pady=4)
        ttk.Entry(frm, textvariable=energy, width=10).grid(row=1, column=1, sticky="w", pady=4)
        ttk.Label(frm, text="Κόστος επιφάνειας:").grid(row=2, column=0, sticky="w", pady=4)
        ttk.Entry(frm, textvariable=area, width=10).grid(row=2, column=1, sticky="w", pady=4)
        result = {"ok": False}
        ttk.Button(frm, text="OK",    command=lambda:(result.__setitem__("ok", True),  win.destroy())).grid(row=3, column=0, pady=(10,0))
        ttk.Button(frm, text="Άκυρο", command=lambda:(result.__setitem__("ok", False), win.destroy())).grid(row=3, column=1, pady=(10,0))
        win.update_idletasks()
        try: win.deiconify(); win.lift(); win.focus_force(); win.wait_visibility(); win.grab_set()
        except Exception: pass
        self.app.root.wait_window(win)
        if not result["ok"]: return
        newop = choice.get()
        try:
            new_energy = max(0.0, float(energy.get())); new_area = max(0.0, float(area.get()))
        except ValueError:
            messagebox.showerror("Μη έγκυρες τιμές", "Η ενέργεια και η επιφάνεια πρέπει να είναι αριθμοί.", parent=self.app.root); return
        changed = False
        if newop in {"+", "*"} and newop != self.op: self.op = newop; changed = True
        if self.energy_cost != new_energy: self.energy_cost = new_energy; changed = True
        if self.area_cost   != new_area:   self.area_cost   = new_area;   changed = True
        if changed:
            self.fill = COLOR_BLOCK_ADD if self.op == "+" else COLOR_BLOCK_MUL
            self.app.update_area_display(); self.app.redraw()
    def evaluate(self, memo, stack):
        if self in memo: return memo[self]
        if self in stack: raise ValueError("Εντοπίστηκε κύκλος στους κόμβους.")
        stack.add(self); vals = []
        for i, pin in enumerate(self.inputs):
            src = self.app.find_connection_source(pin)
            if src is None: raise ValueError(f"Λείπει η είσοδος {i+1} στο μπλοκ #{self.id}")
            vals.append(src.node.evaluate(memo, stack))
        a, b = vals; out = a + b if self.op == "+" else a * b
        memo[self] = out; self.value = out; stack.remove(self); return out

class OutputNode(Node):
    def __init__(self, app, x, y):
        super().__init__(app, x, y, title="📤 Έξοδος", fill=COLOR_BLOCK_OUTPUT)
        self.add_input("in"); self.display_value = "X"; self.sim_value = "X"; self.next_sim_value = "X"; self.value = "X"
    def draw(self, canvas):
        super().draw(canvas); z = self.app.zoom
        x1w, y1w, x2w, y2w = self.bbox_world(); x1, y1 = self.app.to_view_pt(x1w, y1w); x2, y2 = self.app.to_view_pt(x2w, y2w)
        txt = "" if self.display_value is None else str(self.display_value)
        canvas.create_text((x1+x2)//2, (y1+y2)//2, text=txt,
                           font=(self.app.FONT_FAM, font_size(26, z), "bold"), fill="#92400e")
    def evaluate(self, memo, stack):
        if self in memo: return memo[self]
        src = self.app.find_connection_source(self.inputs[0])
        if src is None: raise ValueError(f"Λείπει είσοδος στην Έξοδο #{self.id}")
        v = src.node.evaluate(memo, set()); self.display_value = v; self.value = v; memo[self] = v; return v

class Connection:
    def __init__(self, src_port, dst_port): self.src_port = src_port; self.dst_port = dst_port
    def draw(self, canvas, zoom, to_view_pt):
        x1w, y1w = self.src_port.position_world(); x2w, y2w = self.dst_port.position_world()
        x1, y1 = to_view_pt(x1w, y1w); x2, y2 = to_view_pt(x2w, y2w); mx = (x1 + x2)//2
        canvas.create_line(x1, y1, mx, y1, mx, y2, x2, y2, smooth=True,
                           width=max(2, int(4*zoom)), fill=COLOR_WIRE, tags=("wire",))

# ---------- App ----------
class App:
    def __init__(self, root):
        self.root = root
        self.FONT_FAM = pick_times_font(root)
        root.title("Φτιάξε τον Δικό σου Επιταχυντή!")
        root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(data="""iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAMAAABHPGVmAAAB71BMVEX8xUX8yEv9yEr9yUv8wj/8w0H8xkf8x0j9x0f8wT38xEP8xkb8wDv8yU39yk76xUj/zUv/0k03g682gaz7xkj5xEb/z03/y0r7x0n6x0tDOyP8xEL/0Uw9NyT8vzn7yEz9x0r5xkr/1E//yUg4NCNGPiT/z0j2ayc2MSBMQiJHOB7qu0bvaSf4mws2hbTvv0fSqkFhVCr0mAw8Oic+WlyQbJuIcDBPRiVkTx8zfqv/nwtMPh/lt0UuLCFtXCrrZiWpijmBay1rVySvjzrGoD//y0WOdjNVSiRZUCozaoY5RD73oA4/Nh54YSVBhqmJZ5DlZyekhjdDQSh1WnX0w0lySSQ5PjK2lDt6ZixwVm7eskMzZn/XrkP/2k47XmtxYC2+mz1Uo4RdSyBURUlSnH1Plng5dYb5wkKTUSU/SkBBRzXNpkD/byheS1bWZCc4epVjQyQ8VVf/qg39pQyUezRnUWSfgjRWQyCafjM4iLbxwk0/ZXGDTCU5faOUaht9YIA/UUz9uxNGjLGDZIh6XX1NQDyHYx2ichlGPDVHlL7/xhLqlA9QiGpAbX+ziBvDkhrhkBHUiBf/yESyeRi+XiZJmcPqrRhMdFhKYkfEgRVMa0+hViaSxJxQl7v/41L21HDpmBHxpV90sb343Ij/1g8K7gX8AAAcaklEQVRo3mRW+U8bSRausrur6Gr3Yantdtttt9tXk+AIvJ5gtME2RxJQTDaOF0+yKFmi+QW0QciyUYgQGwlpl6zyA2QSdqQRGs1E84/uVyajndW+Put476tX76hHSKKQ0BRNU1RVEEVJJAqapiqK/MN/IidUBeM5NYEODe/p5+sLM7XpTDCripbQMDztx1sroANtVS0oRCsUtILISbEEUwlRpqw5Aq5CQQE/wDStIOdroITIYUWa5FawHgmGNpbCRIEpRFd1kSBC5BKKgCCiEbWQIBCDBahYq06YrpMcJ4IQJjTGmWBMZVMFAS9U4miCE0KkooKo6BaKKgRejBHCGdEV3VEdpgmSUwUj01VL3fDVVCZ0HuOUEEEZBwGDg4kanOm0yMFQpJxxahBqCMGEytHLKQgrYURwyVWkTFCa2SOyi8khAmghtSDYDvzlMI1RHqNcJ9wACzUMZhgSmBV1oggpVY5Rzk1DpxTL4kU0hZyKaXqccjVHArcWN0xO4tMFQirJ5VSAaLkcwUzIjxsGpdxkcUzRTYPHSJxT/BhUZQa4dEYwrqONSVQ3TDSBAyaTZjIMDJn0i+fb8QzkxQyKzYdCUAYbqyk6UamcSIumSbEiSOSGaQhoE6MC7SI6itiFwAw8L5WySNEwpWwGIYZRZGambNueYZphbb297BKoS/cc4BdNzIGJ4EkwDDpoEIaelQKF+Ak9zwotzzCglcnkLunA9srpZNJ3rYBPTcJgCGjIg/TrxnI6pKblr+d3PgVQKePbgWSDxeA58FANEuKWYydrfq3mJ+VTwuWX/JodSikq9oUWacarbd9fWXk258csqIoeCWQYxLF3Khvb6YBapTft5XIGwt2nC7YHF4KvavDHhCDc5FbZXlh5OKWj6Y3X0dNnyzanJlbNARPEHqy3ZrduV5oPg7IFZ2IO9g3jJG7V7rc7Hg0Df+dp2QmJl3zTXi/B0bB8noBNCnBB7j1Y3q1Utm7/L23NNt/YVDoDLOAY5mp7eNXvH562O2HZ4TAg1alpmlAqLK1Ul23fnZs7mU/XUvZK+yjtSJdmsIcMSE0whxmN2evD/pTquL7S4bB9v7YHz4Y6YemofR1F9Xr94Kq96HsO3EEGArwOFsu4J/72ymY2nx90npXTjcUayyBaOOyhJGS6UoVVW6hcH4C/W49w1SNQvSsb957be04YBJ7lLjdPMdTtdvsH+5WddChNgv1wSCYDA6eSL1qza58/f373XXtt2XJmnJiMUkXXNYBoiRyx/GeVQ8kf9Q9/o3rUrfej4abt2m657MZqTyuHB79+3wVOdFhZKXkmzGECiThBaIXui/zxx8l4gvvHbGvetXSEgkCGkhGP5JMje7X1ymEEjOtsvnpz5+9dyY7TwYvlnWXcc3O7x90vJ10J0oWC6QARQk0Eqe36pTSbaRz3xj/07tzp9cYfK89rezJYdC4QhArJySSfSEpN+tFV5flF891ldfEyu/o4fxj1o/3mVjabrVart6r5YffLl24EBbvRqJM2OEKUxj1/pbX78H7pVfvH8c8/9yT9Yfx5dsHe20ulkCMEcjlcWOH6XnKqycF+6+wsf/mhevGheXk2gJUA8pc/39A//jWEybpXV5EEaZSRE+AOhpFeWOxUn79cPe4Vfp1i9KBM9m0yjXj7hNSnFtSbMyRVWqn0D49H1bWzH7KXZ9WLs+zFh0b21v7B/rdPnjy5e/cunn8O6/X+qNLcn4K4ADHwINxLfsZMb55PTrw7EuOPvTuTtc6DN4uLb+ddyC9oyMJEpyl/favfHw7vSZCL30DuDa8P9pv5Sv6GmsN6dNq82q9AFwkiCQ4W96zALKda78a93mSCzfplcmd8vunutjY2dmwiFBxaIqFSI6w93TpEAOwPzs6qlx+AkL/8oTndrsHKs/Ub2hhG/erpQXQ8lCCfiAPTMi6TNM3EPQkyef94PFlamvTGa42aW9Y/2QEXBalJQYMmAOljxw+zG4+bncXm2mq+sZGVrrA/0JM1JLVS+uXuKOpnr6P6cFSvjzquk5HZn8tsTpmX7iyNe+Pz9vl5+x3UubeYTPEZ7jCGQ1umelVllo8gQCxGV6ej4ejmPpWBE5225omVQlampd3RQb96fXAwHEXR8e5LIyNjEQkSucULS+vtS+zXeT4PjPH79uu0xUhAFXlKq3BhHL979qvZq6jf7ctwlySjvt7vSgs/yODU9dzl1UFzNGoeD0fV6miUHbxBhOD0hINRx/K9+Xgj+3E8GXc2oND3s6tpT1YD8GAqEtguZBXqqHPZUT/6f7pqv0mmkGotf3X2dPh7ar9KhkSe2VR8Sr5udfz5VvUXgHw3AUYnHkNOQ3rXRU6WRKomFMEdf71ye3i6f0PXX7+no9nGdgxlRNFI7w4Pfk9RdqUU4gzGcR+fX21vLsTtucHaWGoy2WjEXYchhHRZU8hqJYfzBCvKIKYa2W//1hy0Bv+lxtuTsoeSgFtJaHJDwyGe0+HsK9+jSLM0sBda67Yrtl8+y0/OHm+c9SqvS6m4rEeIjvIHZZk85qUnUs+upZe++enR25m5+bn5eTxzc/PxUtoNgpgc3elsNjabrUZjszFo4vcoIz3YkL5l2zViiZlwMfv5Yql18T7/1kJVEaeqjopKoCQlOQWRr1LCUqn40l///ehtKY6c69rycZMnL5bTdhjnwrNty38x+yoZK5YWW4E7Y8cyMVkNFWX1ZBnUSh7NVvP5ajXfrLaPaji2KTKvqssqmGiywGWy4GPxpW8A4odOYGSCTMYI0usbW9ndHTswCQ8sy34NkNBKLt7a1gNvWnDJ2mxauRhhcvXRn/7+Hy6s/SeNPY8Co4wyDjMDw8DAcKcMQngkqPGBREtQUKwRDWpArK2KD4KGGJL6jivVetc29ja5yW6bpnd/aO4fuuczuHc3+1EUfHDm8/iezzmzbMbihKEyDP2WteDtByzQqAMOUiOsXZwlEAncyTJOu8Uj5V7urdWC6aGwj7daXqhRgIiqqk2kQzaV7eV487TbGTSfZVRppnJ4ePiZPivzhmCzW2hnohtg4f4BeyDA2TEM9vDk2EeAhHh7AJJQZ9bTe6DG21hZEljWwVMmBU1vRGfiKqNDhJqSh1QfSUohml+aetYG/h1NgIQiMYWe09LqDzh6IMMgfJxmuSQqJ/5AFacjNWLfxxlDoIIISiG2o4QAgkx0JwSgSZCompOjqkkXwZObm5vlk2DZ8EB7MEifI5XaT2ICELgkziGaIEaIqg3BG05GWgQSnNdCkCSMqgy/xCWiLhHGIjtJDAGGIb63odgecSv2dvnucvnt4LASot8GWBpiIFhop2Cm8UOeoXKd4bIh3rH15OhErLZy34odiyrEK/vCtl69YnyqeJwXHSwlIQPbRmh4wdsF8SzmP1qNxN6FdcoCH729rB3mATXjINFQVd7+DBLi7GYqPu96dikS8ee1EDgQ58rKSFCHjCpKHsFUsQ1dgJLBM1lVQxgycWs7shcpaKTIiTwZchYcZCo8FpQ6DYmFmWybIHbe3mMH8aleZebxsWro5BmcTq5HVyHYZauiKaKiiJryHFASkmGIujX0pry3kg55KTEWYh0w+E+s3p6BXwI9AZgC1mGjnpSp8U7WBn3Ie+ZmTlt5SYWKc/BOxo4rscmiWLiYKW2USjOlbmRL2Y2NiXJSEwTt3d59esgZIrmuI3PStziSFq6/h9xbAPvHnK6yFjKdA8QnL89la62yEcKw4bIwsqxVEJPZ2GhlcbHZXOxG03xWGZzamWsYZ3vjwcKbKCVmFaCSWbQFhE9+kCXbZu0ze5IzPIKAcwSZzatSqdbKGTrWBlkFCwRxQJ8d/HyTSV2mUvRwuS5Tl+b3k8VIktGqj+Ot+PzFxVl12KlA77Ncby9MFsQEPKjVarP0qXVkMm+IkuQVbE5SoNI2QCQwE28eb5UXojuxz6m7u4zL7XZn8HC73C4XPUmdDJYlSzJyOr7W2tvbe/AvDCsqCD7AkeDu6Q1wZNN0Xq+3/3GdqM9u5K7mGjwqKovbtT2kZjUdlVX3esPGRMW1/OMngbgyGROrC+JOLZYkn7Ez+FD7cHt/v7LS8k8rMqwDSaJAoB9mzkHeDT35eHdyPdYZjG+JHofVKSso14US8pmaRBYLIyMjU53Mz58ZN727mYeJgu+Zy87UwkJ2enijHo/HI0ut8cczrcHQ7QDIVNgtnBiQk02vj338+Afirpm+8vpY1qNsrLXm34iMAErVZWXWX5pNtFPLyAFvjUa48CVFKABJdaZKJf+GoQlDyelkdem+tSF6eBZHhNTKQC92PrRTH4Ecrg4OVpbvBvNKyMI1tJnTtfjOpq5BmfCW8MjMn++nxi4zVCnXSbt5dHTUbI7dpNwZoFx26p/+LG1HPZw3/PucWFw7LSlCwMLBLpIg7rWbvpQRUK7KbD6fPfpj8exfsFgeLRccP32IL1Sh4WWPODL1918TYykzj0N/BAjN5lFi9cRFIKn21Mzf/NtayOfTZQcz8qG2rQgWnA+UCzKSFjCRBjf59m505400v9T0j8xXvToGbvZxbWWlFqtqKt8Qq+hJF8SV6qy+fmXGdaSDYhFIAqu5oIRASA47QE63FRVKg6iebus4sE1AcowJYkzEFhYWmquxgujRxfWz2fjD+GmRZ3w+VhvyTE+NpcxGr3ZevX4NnNevOpEbmq9Up36VHDJUi8XplBmeQKSQ3cGiHZguUCT5FaxDAilE69929xGVM0O1y4zhHSrt3UemvaoqvoNRQSZudORmtU0ghNOO3KTMciVGRyNVxeNwOlXdufDhdEND4x0Q27BbPWS3bchEMUGU4leA7O5WyhosGVa7VHhYWd0MC/bwwuRvZ2bj3a6bSBcE9QIInZpU+/y3L/VsVLZZdUW7St+eZhWlz4dy9aInvaAtOt5WcfL6LlgQ083v3xDBnNGg5Scrxw8r8c2wbPcu/PrpnygXnfK/QF4/g7gv25PvP5WyGg61cpytJyKJRH3eZ+PMG2n9DoLgHHabaGbiLfrTEHjpwZzkwUmH5Bp+uI9Pi6qsbL+kciGTzP+DAAXlCvpfzkse3RYqVr6ZFxqrSg1MFjktluPQE87CmyBi8fvu/sH+QaUcVa0+jpMVE0TRfeFkLpejTIhS/tv4tv+EMkl1zvP56nrYIXs3E0+7+/jYPQKmBSYI3OXAKrYyPmr8cvBYPKee7B+MYrOA3HkPQFbSyEQIT5dzZYBkaGSPjl49R/PIZJhLgJRzQ2FZ8G4RCK5z/wg2xUEECefwgm7TsdZwF6T+/QDxNErlgtT1SOhJZFPj++ayL6fM6aJUrhOdt2Y0E9eXxMgoVyT+Eu/aELcSX3/86IJEcR57zBuKdhJoPOsFyOiwCNWYgKtGTzBdKtbrO2yivLC+zo+UPr0/b6dMlneN/UdkvXW5u+Wqv/80ux2VhbmtpacfP/afM7HQOent/wVqxcJhTwHEvyUWO18pRnNQaHJ0c6K4dDre8seLxaJ/8suXczQe5A6uOvlMcXiScnXXSgcjfL4tYUC2/E+UyT6BNHpMEGq91cp1e4JM0BOKSl4KhcTq0uPpLelIsvKtyOgopuuZ511Yjng8vzCnKxgB/0CfBZ92dw8O9ruZ0E21/gBHd7PIhRDIsbSw+nTw9PQ9Voh6wtP+1vj4/e2HtQ+3FLVabaqdypgrBAyWyWTcz4E93JxNbiYVKyPMDS897VNfqSfIJED6DixptULu9WGE/cPGTiTmjwdjG9C3xrvR8fuHYNyMtBn+5v/sq+7O6iK5ILPDYd3KCmIXBLSBTATLADFxfy+pOVAXTz0ZFsXpwsbSxbHX67B4R1rjD7NbySRZoqur9avkei72+ZK2FSVjrqvu6nJdXscKcx6dZ1mc3uBfmaAnGOEeUD1tcJAwNT44rIWYN/nYtKHyvK1RrN0Htwz4IfHfTFr7Txp7Fp9hZKYyDjPsDswwMA7DKyAhgBZpAImiPNJgjdUoGl2NJiUtMTd3W61pc7FbX+01TXzk9qb7w83+qfs5X+8+JoDRtHzmPL7nfD7nDF4JyCJNaGQ+glf/x02//PUFfvnLLz89zfQ13if5BVQuWIKgUv1rB8a9kxFSvxybjnEMBJaAo61miq2woj9Z72xdpHKGo5s+3cGdOKZrFBam7JcbG2/wovfGzEv89rI3NesKDrUMTr/PpV7//k9cn9AuBhFSv6TnZd6jeDjpESToQv1sa6piPgl21hiIwii8B5WU141QfcG6HvWW5w9q1yO7P49+Oeq16yGPA8Hv58c4J7R58B4FsnawqpnyGJQWuqMP/xcMmWPuGkZBdusnkDloPesAqeXAcpF8YO80C0Yb3l20/vE9ufRHv/Pr9+Twj9kKfizFXdNPshq8UNKNRKFzfvgONJIXx8dprjbmFfwokbKoHDBLdME04n4JXNkDkLMsQCSabQgUOrB1eJNANnf3Dn79ntnfZSD7aLUkUWGz7FHU+wEDWecU6B8f5BzaL5KLE0GJPtKJV/2K4/j9kuwQyEUWkhEtjQa0QKGxamBxbrkxBxDraplAMlfNuaW0CxYrm2F3EFbVIFeonB+eRlXRx3iXFx5jiwxHCDMQ3JKHBvoRUTEKFQIxTBnxlASBdgExEMlCv9Pt5wLzyUO7m4sWS51u2/UjMQZBLR2iKbkWX7LLlyh+INwTOCdUiSOSJ0L3+YxADJU4Pwg470QKzF2GI/A6xLQD1gmPK46h3RstT6holQ/b8aBmSFrIb+LvmpYbLi3t728unnaOyvYwpCrymJfxrjGadeNen/wJogsSU5yKmfiQhSWUXZAsYXw3RAe5XA9CIbla0Vo5nIWIBAkh4o9mtWfblm0nk5m5zNGXpoeTmQKijdAYJ7LBxxOT3LXdCgJAdWjdcF/Irp1VCoYOxeJooUKhpan4l6CCpq6EmSWzcRcmcqKClCpUsps03t3eGS62+7OUlTJIxDixFbRfPhZTTMmBJanttCGJQtowRdlJICZnOCeuq7rRYrP2fiGXGMBwrygqfr01JEsAEqOphBrUipniLorDvaZBfURJX/Ki6IPCBlsZl4nSx7gIC/z2yakWvJ/dhEo2jQ+VrRXkaiDaCmxbz799THYKaTiP80YkIWgwdwXCckT36OFQOrpvFyEkgwN1MFBpmeNlY+EJuIubmIQtHGgElBaBlDrak3UbxEzyJQrZrfJh9mR/f3+4vPH5628vkrP1bU1TadWhhsiSNsSeT3Dv08V210q+7LaXEqgViLIicV4TZ3CMqjAtIWmCIeoy/+zbCyu314zLemp2V9DhZYCcH19+wTX19OuLz18/9TLJUrGlQ+kHNQYSCPLQX7l+Zqo5uh41rUypmEYMBToHUNe6l4MIQuGCMIVONcGFv322+u8rS9pq7+Akp4WNXHaNBs/nZ+dn2ae/ff769c3e0nw2lYPwgCUshdNBkLmdrHV9U6Vr+qGWmY+Gof9k2h2ByY+jQEa8SGKRFCKnNV9/tJ6/TjZc6+XruYagJwjkyLZnLFy9b59f/C0zjMd3MqtRqL0wLClfwl1qazt1cPs2P82u6k1zbj/qeiQF50LySt6JyUmOhp3jJIIktTWs9N68evW8v559+tPTWu6epXDvZGdYLBa3FzIzdm8VmaZ1oXQk5PRwpnx5CrHcatRuqtPT+fwtoeSrTSuHrEc6SX7axE5MIvAEwbaUuuHvbzCQGkCyuYinkL1Yy64HQmwGMVxdLYZkRzG6jZAqcwj8DJ2TQXop81AFRP42dV0llJsejqiA/sFJMTJknA6jjxaDCBMfDMwSyHKBgdQjUi57sVUp+NSwHlbNUDptuLwTNkpNSCjeNXasleNsPZHeew+E/HT1LjmqMo9dpQqGQ3Nh9BHvJDUt1EmvLsrU0wbpBWbJBwYSTMe3e+drlYKs83TKdTfogqCNt0oN0s7qPeXeZa1ZskfMkOqtfV0FWL76g5gOVRFR9o35UOqpNXIyiQdBVpklGwvMXbX2/OKeVQZIAk0EpUyQYrwiio5WarS8qG7B9Lvkefni+Cj5AyA3tzc/kqP87S3Fpkfin6ivzzs+hjLP0Zt2x4pnDGqXgTBLrBnLzhyWtyrrHpNG5jiwtNeWuQTFRASa7DaSh8dbR9ZdvnpHCZjCmxBvrFUaY/B+OAhVOMKBpNJUTeb8iqz+P0itWMi17ZWtzrpABZJmLei9sm4a3b3oAAdB0hP85kKj2Z25y0/fXF2NlmeejUaj23yeQII0mQOVl4kLeye90KXoSKjharr/X5CfawUjXbcu1irrhgkIHV0xIvt5k7JLG9B+nA9LgXQiXbfJXdXq27vk9d+rVQTlNrmIMyoJfl70+dhqg3QjrTYhuFRt+X8xeV8QBGTXWueDx/TzjqqbfEQ3FUcxK3ug4hQm3gy6qsetXAEESfUjeV29oex6SO5oaPkeBJujpxgeyxetypHGNKX+SCDZn199qqwLWi61dmbVo7qimPh+XTfDZjhQz7Spr5L7JCU2FowuWDe4fYDMXT+m8LOuobBVuo8kKUBQWug5D2qGnK7VO5lsZsFNWam5d6Ew2tBx2eoXoMwNg2ikFtIS9WZmh1VIcrqJ6qjtJJfZl99e3RHY24e5zagr04AdB9w7OUGPMEyiCMd4KiyC0yqcWN1tbd5q7icEqMTmZXnNznaflUrNJl6NRqmTtCEPiDzTieY50TdIv4MJeSoo9IHQ9DUTFdcn0nMI3seY+CREPsKeq0D9GlizcU84dbo7cFDC5+e2yitbx0dHR+z9JTs7uwiNSjtwjh7aoGcqOE5bmLuaZiFHHX5IlgoJJyY+PsdBTXGc7VBgCvoWWg1nGrnkQlr6YL8LBGXekYyFzOHa+cqfV/mwG4/HE8EYbX3ZBlCkYZvpMU4z2dHdTf5ftw8Hc/31hEqnimePmUiTJB18xL54ZgeorOBvLKK6NTcDQRQz0xNi62/bog98tlGFHfbECPV1osjIMlHno8W9mcxUbSppl/YNiBS/HzGB5vHpopd6/LhvYoynwXtMYpRX8Aum4PoVesqCV5yoUgeXeryG9YQ/JjIyGvPiRmm/LHNw9b9LNIPchkEgikIFloxxnUqT1BGVg1opp+iimx6gq0pddecr9Pj9b5woNrIHGAgzfGb+TVv8++/H39f3z/PLunvEO7L6CKNDjmFxldkD+8zxqi0yGn+RyQ6iXYfTxcPMd11PV2HvOCFKiMz9hrytULbtb5fXp/v90/YZwsgUyaoQ3vZQFCShclQFtjtIbGN2PaKFR8HbsxDIsth5X+VMQp8yZI9BB4Gb7qF7qH+SxLIv55XeqQs+00+bYsbjC+WVNsShASj6w8yJSNAVYk2WV8M3MFBNjHruBec6zH0wjSDEUk2Yh6k24Ah5PzIjguclzU2TNbq5kzOVaRoCNvdGDtJWNcV+JuQ0JZKE6J6ty01AYsLp5WCQm6ShQbVRuUxllZkKwHcLg9TQg4NLtMHQSg0oKfmJszBsA8/ZliYdnOFFUNQ5VmQO5Y80xa0JhlQIWBl+gjOgCG2RZNAt0YwuBDpJamVoXzJ9dkkt66LnGl/dnL2VIHVVFZ3NNdKDBKUdH4q1qqeKLjhDz5FRL0vakxrktDZpORYNiGQdPLMURvUf8tEkLR8UNKeQEVH0F6ruS9N1GAlruKJeB+0zps4RqJKd2/SVp9xc2FlwvHXZo2Wv6RqO/s4L8ODy0BKmnLxXZDaXPAhylDLN1/QP1Sfd2oT8N3kAAAAASUVORK5CYII="""))
        

        self.nodes = []; self.connections = []
        self.dragging_node = None; self.drag_offset_world = (0,0)
        self.pending_wire_src = None; self.pending_wire_preview = None
        self.marquee_start_view = None; self.marquee_id = None; self.marquee_active = False
        self.copy_buffer = None; self.paste_bump = 0
        self.zoom = 1.0; self.sim_running = False; self.sim_after_id = None; self.sim_tick = 0
        self.last_tick_energy = 0.0; self.sim_energy_total = 0.0

        self.tooltip = Tooltip(root, font_tuple=(self.FONT_FAM, 12))

        self._bg_logo_imgs = None
        self._bg_image_ids = []

        self._make_ui(); self.redraw(); self.update_area_display(); self.update_power_display()

    # --- Coords
    def to_view_pt(self, wx, wy): return (int(wx * self.zoom), int(wy * self.zoom))
    def from_view_pt(self, vx, vy): z = self.zoom if self.zoom != 0 else 1.0; return (vx / z, vy / z)

    def _btn(self, parent, text, cmd, bg="#e5e7eb", fg="#111827"):
        return tk.Button(parent, text=text, command=cmd,
                         font=(self.FONT_FAM, 12, "bold"),
                         bg=bg, fg=fg, activebackground=bg, activeforeground=fg,
                         bd=0, padx=12, pady=8, relief="flat", cursor="hand2")
    def _spacer(self, parent, w=8): tk.Frame(parent, width=w, height=1, bg=parent["bg"]).pack(side="left")

    def _make_ui(self):
        tb_bg = "#f3f4f6"
        toolbar = tk.Frame(self.root, bg=tb_bg); toolbar.pack(side="top", fill="x")

        # Left side: TWO rows of buttons
        left = tk.Frame(toolbar, bg=tb_bg); left.pack(side="left", padx=8, pady=6, anchor="w")
        row1 = tk.Frame(left, bg=tb_bg); row1.pack(side="top", anchor="w")
        row2 = tk.Frame(left, bg=tb_bg); row2.pack(side="top", anchor="w", pady=(6,0))

        # Row 1: create + evaluate + start/stop
        self._btn(row1, "🔢 Είσοδος", self.add_input_node, bg="#c7f9cc").pack(side="left")
        self._spacer(row1)
        self._btn(row1, "➕ Κουτί",   lambda: self.add_op_node("+"), bg="#fef9c3").pack(side="left")
        self._spacer(row1)
        self._btn(row1, "✖️ Κουτί",   lambda: self.add_op_node("*"), bg="#bfdbfe").pack(side="left")
        self._spacer(row1)
        self._btn(row1, "📤 Έξοδος",  self.add_output_node, bg="#fecaca").pack(side="left")
        self._spacer(row1, 16)
        self._btn(row1, "🧠 Υπολόγισε", self.evaluate_all, bg="#ddd6fe").pack(side="left")
        self._spacer(row1)
        self._btn(row1, "▶️ Έναρξη",    self.sim_start, bg="#bbf7d0").pack(side="left")
        self._spacer(row1)
        self._btn(row1, "⏹️ Διακοπή",   self.sim_stop,  bg="#fecaca").pack(side="left")

        # Row 2: zoom + selection + help
        self._btn(row2, "🔍➖", self.zoom_out,  bg="#fde68a").pack(side="left")
        self._spacer(row2)
        self._btn(row2, "🔍➕", self.zoom_in,   bg="#fde68a").pack(side="left")
        self._spacer(row2)
        self._btn(row2, "🔁 100%", self.zoom_reset, bg="#fde68a").pack(side="left")
        self._spacer(row2, 16)
        self._btn(row2, "🧼 Καθαρισμός", self.clear_selection, bg="#fff7ae").pack(side="left")
        self._spacer(row2)
        self._btn(row2, "🗑️ Διαγραφή", self.delete_selected, bg="#fca5a5").pack(side="left")
        self._spacer(row2)
        self._btn(row2, "❓ Βοήθεια", self.show_help, bg="#bae6fd").pack(side="left")

        # Right side: vertical chips (always visible)
        right = tk.Frame(toolbar, bg=tb_bg); right.pack(side="right", padx=8, pady=6)
        self.timer_var = tk.StringVar(value="⏱️ Χρόνος: 0 s")
        self.area_var  = tk.StringVar(value="🧩 Εμβαδόν: 0")
        self.power_var = tk.StringVar(value="⚡ Ισχύς: 0")
        for var, bgcol in ((self.timer_var, "#e5e7eb"), (self.area_var, "#e5e7eb"), (self.power_var, "#e5e7eb")):
            tk.Label(right, textvariable=var, font=(self.FONT_FAM, 12, "bold"),
                     bg=bgcol, fg="#111827", padx=12, pady=6).pack(side="top", pady=2)

        # Canvas
        self.canvas = tk.Canvas(self.root, bg=COLOR_BG, width=1000, height=600, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Status
        self.status = tk.StringVar(value="Έτοιμο")
        ttk.Label(self.root, textvariable=self.status, anchor="w", font=(self.FONT_FAM, 10)).pack(side="bottom", fill="x")

        # Bindings
        self.canvas.bind("<Configure>", lambda e: self.redraw())
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind("<Double-Button-1>", self.on_double_click)
        self.canvas.bind("<Control-MouseWheel>", self.on_ctrl_wheel)
        self.canvas.bind("<Motion>", self.on_motion)
        self.canvas.bind("<Leave>", lambda e: self.tooltip.hide())
        self.canvas.bind("<Control-Button-1>", self.on_ctrl_click)
        self.root.bind("<Control-c>", self.on_copy)
        self.root.bind("<Control-v>", self.on_paste)
        self.root.bind("<Control-x>", self.on_cut)
        self.root.bind("<Delete>", self.on_delete_key)
        self.root.bind("<Control-plus>", self.on_zoom_in_key)
        self.root.bind("<Control-KP_Add>", self.on_zoom_in_key)
        self.root.bind("<Control-equal>", self.on_zoom_in_key)
        self.root.bind("<Control-minus>", self.on_zoom_out_key)
        self.root.bind("<Control-KP_Subtract>", self.on_zoom_out_key)
        self.root.bind("<Control-0>", self.on_zoom_reset_key)

    # --- Background logos (each shown once)
    def _b64_to_photo(self, b64):
        if not b64 or not PIL_OK: return None
        try:
            img = Image.open(BytesIO(base64.b64decode(b64))).convert("RGBA")
            return ImageTk.PhotoImage(img)
        except Exception:
            return None

    def draw_wallpaper(self):
        # clear previous
        for iid in self._bg_image_ids:
            try: self.canvas.delete(iid)
            except Exception: pass
        self._bg_image_ids.clear()

        if not PIL_OK:
            if not getattr(self, "_warned_pillow", False):
                self.status.set("Δεν υπάρχει Pillow· τα λογότυπα δεν θα εμφανιστούν (pip install pillow).")
                self._warned_pillow = True
            return

        w = self.canvas.winfo_width(); h = self.canvas.winfo_height(); margin = 16

        if self._bg_logo_imgs is None:
            self._bg_logo_imgs = [
                self._b64_to_photo(LOGO1_B64),
                self._b64_to_photo(LOGO2_B64),
                self._b64_to_photo(LOGO3_B64),
            ]

        L1, L2, L3 = (self._bg_logo_imgs + [None, None, None])[:3]
        if L1 is not None:
            self._bg_image_ids.append(self.canvas.create_image(margin, margin, image=L1, anchor="nw"))
        if L2 is not None:
            x2 = max(margin, w - L2.width() - margin)
            self._bg_image_ids.append(self.canvas.create_image(x2, margin, image=L2, anchor="nw"))
        if L3 is not None:
            x3 = max(margin, w - L3.width() - margin)
            y3 = max(margin, h - L3.height() - margin)
            self._bg_image_ids.append(self.canvas.create_image(x3, y3, image=L3, anchor="nw"))

        self.canvas._bg_keepalive = self._bg_logo_imgs  # prevent GC

    # --- Hover (Inputs & Outputs)
    def on_motion(self, event):
        wx, wy = self.from_view_pt(event.x, event.y)
        node = self.node_at_world(wx, wy)
        if isinstance(node, InputNode):
            val = node.input_value
            try: bin_s = format(val, '#b'); hex_s = format(val, '#x')
            except Exception: self.tooltip.hide(); return
            self.tooltip.show(f"Δυαδικό: {bin_s}\nΔεκαεξαδικό: {hex_s}", event.x_root, event.y_root)
        elif isinstance(node, OutputNode):
            v = node.display_value
            if isinstance(v, int):
                try: bin_s = format(v, '#b'); hex_s = format(v, '#x')
                except Exception: self.tooltip.hide(); return
                self.tooltip.show(f"Δυαδικό: {bin_s}\nΔεκαεξαδικό: {hex_s}", event.x_root, event.y_root)
            else:
                self.tooltip.show("Δυαδικό: X\nΔεκαεξαδικό: X", event.x_root, event.y_root)
        else:
            self.tooltip.hide()

    # --- Zoom
    def set_zoom(self, z):
        self.zoom = max(0.5, min(3.0, float(z))); self.status.set(f"Μεγέθυνση: {int(self.zoom*100)}%"); self.redraw()
    def zoom_in(self): self.set_zoom(self.zoom * 1.1)
    def zoom_out(self): self.set_zoom(self.zoom / 1.1)
    def zoom_reset(self): self.set_zoom(1.0)
    def on_zoom_in_key(self, e=None): self.zoom_in(); return "break"
    def on_zoom_out_key(self, e=None): self.zoom_out(); return "break"
    def on_zoom_reset_key(self, e=None): self.zoom_reset(); return "break"
    def on_ctrl_wheel(self, event): self.zoom_in() if event.delta>0 else self.zoom_out(); return "break"

    # --- Node creation
    def add_input_node(self):
        n = InputNode(self, 40, 40 + len([x for x in self.nodes if isinstance(x, InputNode)])*120, value=0)
        self.nodes.append(n); self.redraw()
    def add_op_node(self, op):
        n = OpNode(self, 300, 40 + len([x for x in self.nodes if isinstance(x, OpNode)])*120, op=op)
        self.nodes.append(n); self.update_area_display(); self.redraw()
    def add_output_node(self):
        n = OutputNode(self, 650, 40 + len([x for x in self.nodes if isinstance(x, OutputNode)])*120)
        self.nodes.append(n); self.redraw()

    # --- Selection helpers
    def clear_selection(self):
        for n in self.nodes: n.selected = False
        self.pending_wire_cancel(); self.redraw()
    def select_in_world_rect(self, wx1, wy1, wx2, wy2, add=False):
        if not add:
            for n in self.nodes: n.selected = False
        rx1, ry1 = min(wx1, wx2), min(wy1, wy2); rx2, ry2 = max(wx1, wx2), max(wy1, wy2)
        for n in self.nodes:
            nx1, ny1, nx2, ny2 = n.bbox_world()
            if not (nx2 < rx1 or nx1 > rx2 or ny2 < ry1 or ny1 > ry2): n.selected = True
        self.redraw()

    # --- Events
    def on_canvas_click(self, event):
        wx, wy = self.from_view_pt(event.x, event.y)
        port = self.port_at_world(wx, wy)
        if port:
            if port.kind == "out":
                self.pending_wire_src = port
                vx, vy = self.to_view_pt(*port.position_world())
                self.pending_wire_preview = self.canvas.create_line(vx, vy, event.x, event.y, dash=(4,2),
                                                                    width=max(2, int(3*self.zoom)), fill=COLOR_WIRE)
                self.status.set("Σύνδεση: κάνε κλικ σε θύρα ΕΙΣΟΔΟΥ για ολοκλήρωση.")
            elif port.kind == "in" and self.pending_wire_src is not None:
                self.try_create_connection(self.pending_wire_src, port)
                self.pending_wire_cancel(); self.redraw()
            return
        node = self.node_at_world(wx, wy)
        if node:
            for n in self.nodes: n.selected = False
            node.selected = True; self.dragging_node = node; self.drag_offset_world = (wx - node.x, wy - node.y)
            self.status.set(f"Επιλέχθηκε μπλοκ #{node.id}. Διπλό κλικ για ρυθμίσεις."); self.redraw(); return
        # marquee
        self.marquee_active = True; self.marquee_start_view = (event.x, event.y)
        self.marquee_id = self.canvas.create_rectangle(event.x, event.y, event.x, event.y,
                                                       outline="#60a5fa", width=2, dash=(3,2))
    def on_double_click(self, event):
        wx, wy = self.from_view_pt(event.x, event.y); node = self.node_at_world(wx, wy)
        if node: node.configure(); self.redraw()
    def on_ctrl_click(self, event):
        wx, wy = self.from_view_pt(event.x, event.y); node = self.node_at_world(wx, wy)
        if node: node.selected = not node.selected; self.redraw()
    def on_canvas_drag(self, event):
        if self.dragging_node:
            wx, wy = self.from_view_pt(event.x, event.y); gs = GRID_SIZE
            nx = max(0, int((wx - self.drag_offset_world[0]) // gs * gs))
            ny = max(0, int((wy - self.drag_offset_world[1]) // gs * gs))
            self.dragging_node.x = nx; self.dragging_node.y = ny; self.redraw()
        elif self.pending_wire_src is not None and self.pending_wire_preview is not None:
            vx1, vy1 = self.to_view_pt(*self.pending_wire_src.position_world()); mx = (vx1 + event.x)//2
            self.canvas.coords(self.pending_wire_preview, vx1, vy1, mx, vy1, mx, event.y, event.x, event.y)
        elif self.marquee_active and self.marquee_id is not None:
            x0, y0 = self.marquee_start_view; self.canvas.coords(self.marquee_id, x0, y0, event.x, event.y)
    def on_canvas_release(self, event):
        self.dragging_node = None
        if self.marquee_active:
            x0, y0 = self.marquee_start_view; wx1, wy1 = self.from_view_pt(x0, y0); wx2, wy2 = self.from_view_pt(event.x, event.y)
            self.select_in_world_rect(wx1, wy1, wx2, wy2, add=False)
            self.canvas.delete(self.marquee_id); self.marquee_active = False; self.marquee_id = None; self.marquee_start_view = None
    def on_right_click(self, event):
        wx, wy = self.from_view_pt(event.x, event.y); node = self.node_at_world(wx, wy)
        if node:
            menu = tk.Menu(self.root, tearoff=0, font=(self.FONT_FAM, 10))
            menu.add_command(label="Ρυθμίσεις...", command=node.configure)
            menu.add_separator()
            menu.add_command(label="Υπολόγισε από εδώ", command=lambda n=node: self.evaluate_from_node(n))
            menu.add_separator(); menu.add_command(label="Διαγραφή", command=lambda n=node: self.delete_node(n))
            menu.tk_popup(event.x_root, event.y_root)
        else:
            menu = tk.Menu(self.root, tearoff=0, font=(self.FONT_FAM, 10))
            menu.add_command(label="Προσθήκη Εισόδου", command=self.add_input_node)
            menu.add_command(label="Προσθήκη μπλοκ +", command=lambda: self.add_op_node("+"))
            menu.add_command(label="Προσθήκη μπλοκ ×", command=lambda: self.add_op_node("*"))
            menu.add_command(label="Προσθήκη Εξόδου", command=self.add_output_node)
            menu.tk_popup(event.x_root, event.y_root)

    # --- Hit testing
    def node_at_world(self, wx, wy):
        for n in reversed(self.nodes):
            if n.hit_test_world(wx, wy): return n
        return None
    def port_at_world(self, wx, wy):
        for n in reversed(self.nodes):
            p = n.port_hit_world(wx, wy)
            if p: return p
        return None

    def redraw(self):
        self.canvas.delete("all"); self.canvas.configure(bg=COLOR_BG)
        self.draw_wallpaper()
        for node in self.nodes: node.draw(self.canvas)
        for conn in self.connections: conn.draw(self.canvas, self.zoom, self.to_view_pt)

    # --- Node/connection ops
    def delete_node(self, node):
        if node in self.nodes:
            self.nodes.remove(node)
            self.connections = [c for c in self.connections if c.src_port.node is not node and c.dst_port.node is not node]
            self.update_area_display(); self.redraw()
    def try_create_connection(self, src_port, dst_port):
        if src_port.kind != "out" or dst_port.kind != "in":
            self.status.set("Μη έγκυρη σύνδεση: από ΕΞΟΔΟ σε ΕΙΣΟΔΟ μόνο."); return
        if src_port.node is dst_port.node:
            self.status.set("Μη έγκυρη σύνδεση: όχι στον ίδιο κόμβο."); return
        replaced = any(c.dst_port is dst_port for c in self.connections)
        self.connections = [c for c in self.connections if c.dst_port is not dst_port] + [Connection(src_port, dst_port)]
        self.status.set("Αντικατάσταση σύνδεσης." if replaced else "Η σύνδεση δημιουργήθηκε.")
    def pending_wire_cancel(self):
        if self.pending_wire_preview is not None: self.canvas.delete(self.pending_wire_preview)
        self.pending_wire_src = None; self.pending_wire_preview = None
    def find_connection_source(self, dst_port):
        for c in self.connections:
            if c.dst_port is dst_port: return c.src_port
        return None

    # --- Evaluate
    def evaluate_all(self):
        if self.sim_running: self.status.set("Σταμάτησε την προσομοίωση πριν τον υπολογισμό."); return
        try:
            memo = {}
            for n in self.nodes:
                if isinstance(n, OutputNode): n.display_value = "X"
                n.value = None
            for n in self.nodes:
                if isinstance(n, OutputNode): n.evaluate(memo, set())
            self.status.set("Ο υπολογισμός ολοκληρώθηκε."); self.redraw()
        except Exception as e:
            messagebox.showerror("Σφάλμα υπολογισμού", str(e), parent=self.root)
    def evaluate_from_node(self, node):
        try:
            memo = {}
            for n in self.nodes:
                n.value = None
                if isinstance(n, OutputNode): n.display_value = "X"
            val = node.evaluate(memo, set())
            messagebox.showinfo("Τιμή", f"Μπλοκ #{node.id} = {val}"); self.redraw()
        except Exception as e:
            messagebox.showerror("Σφάλμα υπολογισμού", str(e), parent=self.root)

    # --- Clipboard & delete
    def on_delete_key(self, event=None):
        to_delete = {n for n in self.nodes if n.selected}
        if not to_delete: self.status.set("Δεν έχει επιλεγεί τίποτα για διαγραφή."); return
        self.connections = [c for c in self.connections if c.src_port.node not in to_delete and c.dst_port.node not in to_delete]
        self.nodes = [n for n in self.nodes if n not in to_delete]
        self.update_area_display(); self.status.set(f"Διαγράφηκαν {len(to_delete)} μπλοκ."); self.redraw()
    def delete_selected(self): self.on_delete_key()
    def on_copy(self, event=None):
        selected = [n for n in self.nodes if n.selected]
        if not selected: self.status.set("Τίποτα για αντιγραφή (επέλεξε μπλοκ)."); return
        minx = min(n.x for n in selected); miny = min(n.y for n in selected)
        items = []; idmap = {}
        for n in selected:
            if isinstance(n, InputNode):
                payload = ("Input", n.x - minx, n.y - miny, n.input_value)
            elif isinstance(n, OpNode):
                payload = ("Op", n.x - minx, n.y - miny, n.op, n.energy_cost, n.area_cost)
            elif isinstance(n, OutputNode):
                payload = ("Output", n.x - minx, n.y - miny)
            else: continue
            idmap[n] = len(items); items.append(payload)
        conns = []
        for c in self.connections:
            if c.src_port.node in idmap and c.dst_port.node in idmap:
                conns.append( (idmap[c.src_port.node], c.src_port.index, idmap[c.dst_port.node], c.dst_port.index) )
        self.copy_buffer = {"items": items, "conns": conns}; self.paste_bump = 0
        self.status.set(f"Αντιγράφηκαν {len(items)} μπλοκ.")
    def on_paste(self, event=None):
        if not self.copy_buffer: self.status.set("Το πρόχειρο είναι άδειο."); return
        bump = 30 + self.paste_bump; self.paste_bump += 20
        items = self.copy_buffer["items"]; conns = self.copy_buffer["conns"]; new_nodes = []
        for payload in items:
            kind = payload[0]; dx, dy = payload[1], payload[2]
            if kind == "Input":  n = InputNode(self, dx + bump, dy + bump, value=payload[3])
            elif kind == "Op":  n = OpNode(self, dx + bump, dy + bump, op=payload[3], energy_cost=payload[4], area_cost=payload[5])
            elif kind == "Output": n = OutputNode(self, dx + bump, dy + bump)
            else: continue
            new_nodes.append(n); self.nodes.append(n)
        for (si, spi, di, dpi) in conns:
            src_node = new_nodes[si]; dst_node = new_nodes[di]
            self.connections.append(Connection(src_node.outputs[spi], dst_node.inputs[dpi]))
        for n in self.nodes: n.selected = False
        for n in new_nodes: n.selected = True
        self.update_area_display(); self.status.set(f"Επικολλήθηκαν {len(new_nodes)} μπλοκ."); self.redraw()
    def on_cut(self, event=None):
        self.on_copy()
        if self.copy_buffer: self.on_delete_key()
        else: self.status.set("Τίποτα για αποκοπή.")

    # --- Help
    def show_help(self):
        msg = (
            "Οδηγίες:\n"
            "• Σύρε μπλοκ, σύνδεσε Έξοδο → Είσοδο. Διπλό κλικ στην Είσοδο για τιμή.\n"
            "• Διπλό κλικ στο ➕/✖️ για αλλαγή πράξης, ενέργειας και επιφάνειας.\n"
            "• Έναρξη: βήματα των 1s. Αν κάποια είσοδος είναι 'X', η έξοδος γίνεται 'X'.\n"
            "\n"
            "Συντομεύσεις:\n"
            "• Πολλαπλή επιλογή (marquee / Ctrl-κλικ)\n"
            "• Ctrl+C / Ctrl+V / Ctrl+X, Delete\n"
            "• Ζουμ: Ctrl + / Ctrl - / Ctrl 0, Ctrl + ροδέλα ποντικιού\n"
        )
        messagebox.showinfo("Βοήθεια", msg, parent=self.root)

    # --- Displays
    def update_timer_label(self): self.timer_var.set(f"⏱️ Χρόνος: {self.sim_tick} s")
    def update_area_display(self):
        total_area = sum(float(n.area_cost) for n in self.nodes if isinstance(n, OpNode))
        self.area_var.set(f"🧩 Εμβαδόν: {total_area:g}")
    def update_power_display(self): self.power_var.set(f"⚡ Ισχύς: {self.last_tick_energy:g} /s")

    # --- Simulation
    def sim_reset(self):
        self.sim_tick = 0; self.last_tick_energy = 0.0; self.sim_energy_total = 0.0
        for n in self.nodes:
            if isinstance(n, InputNode):
                n.sim_value = n.input_value; n.next_sim_value = n.input_value; n.value = n.sim_value
            elif isinstance(n, OpNode):
                n.sim_value = "X"; n.next_sim_value = "X"; n.value = "X"
            elif isinstance(n, OutputNode):
                n.sim_value = "X"; n.display_value = "X"; n.value = "X"
        self.update_power_display(); self.status.set("Μηδενισμός προσομοίωσης (t=0s)."); self.update_timer_label(); self.redraw()
    def sim_start(self):
        if self.sim_running: return
        self.sim_running = True; self.sim_reset()
        self.sim_after_id = self.root.after(1000, self.sim_step); self.update_timer_label()
        self.status.set("Έναρξη προσομοίωσης.")
    def sim_stop(self):
        if not self.sim_running:
            self.sim_tick = 0; self.last_tick_energy = 0.0; self.update_timer_label(); self.update_power_display(); return
        self.sim_running = False
        if self.sim_after_id is not None:
            try: self.root.after_cancel(self.sim_after_id)
            except Exception: pass
            self.sim_after_id = None
        self.sim_tick = 0; self.last_tick_energy = 0.0
        self.update_timer_label(); self.update_power_display(); self.status.set("Διακοπή και μηδενισμός χρόνου.")
    def sim_step(self):
        if not self.sim_running: return
        tick_energy = 0.0
        for n in self.nodes:
            if isinstance(n, InputNode):
                n.next_sim_value = n.input_value
            elif isinstance(n, OpNode):
                in_vals = []; ready = True
                for pin in n.inputs:
                    src = self.find_connection_source(pin)
                    if src is None: ready = False; break
                    v = src.node.sim_value
                    if v == "X" or v is None: ready = False; break
                    in_vals.append(v)
                if ready and len(in_vals) == 2:
                    a, b = in_vals
                    try:
                        n.next_sim_value = a + b if n.op == "+" else a * b
                        tick_energy += float(n.energy_cost)
                    except Exception:
                        n.next_sim_value = "X"
                else:
                    n.next_sim_value = "X"
            elif isinstance(n, OutputNode):
                src = self.find_connection_source(n.inputs[0])
                n.sim_value = "X" if src is None else (src.node.sim_value if src.node.sim_value is not None else "X")
        for n in self.nodes:
            if isinstance(n, (InputNode, OpNode)): n.sim_value = n.next_sim_value; n.value = n.sim_value
        for n in self.nodes:
            if isinstance(n, OutputNode):
                src = self.find_connection_source(n.inputs[0])
                n.display_value = "X" if src is None else (src.node.sim_value if src.node.sim_value is not None else "X")
                n.value = n.display_value
        self.last_tick_energy = tick_energy; self.sim_energy_total += tick_energy; self.update_power_display()
        self.sim_tick += 1; self.update_timer_label(); self.status.set(f"t={self.sim_tick}s"); self.redraw()
        if self.sim_running: self.sim_after_id = self.root.after(1000, self.sim_step)

def main():
    root = tk.Tk()
    try:
        style = ttk.Style()
        if "vista" in style.theme_names(): style.theme_use("vista")
        elif "clam" in style.theme_names(): style.theme_use("clam")
    except Exception: pass
    App(root); root.mainloop()

if __name__ == "__main__":
    main()
