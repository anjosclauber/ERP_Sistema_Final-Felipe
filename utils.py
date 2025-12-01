import tkinter as tk
from decimal import Decimal, InvalidOperation

def centralizar(win, w=900, h=600):
    win.update_idletasks()
    sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
    x, y = (sw - w)//2, (sh - h)//2
    win.geometry(f"{w}x{h}+{x}+{y}")

def make_decimal_validator(entry: tk.Entry, allow_negative=False, max_decimals=None):
    def _validate(P):
        if P == "":
            return True
        try:
            d = Decimal(P.replace(",", "."))
            if not allow_negative and d < 0:
                return False
            if max_decimals is not None:
                tup = d.as_tuple()
                scale = -tup.exponent if tup.exponent < 0 else 0
                if scale > max_decimals:
                    return False
            return True
        except InvalidOperation:
            return False
    vcmd = (entry.register(_validate), "%P")
    entry.config(validate="key", validatecommand=vcmd)
