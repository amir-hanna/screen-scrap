#!/usr/bin/python3

import requests
import re
from datetime import datetime
from datetime import date
import t_stamp

def get_current_dtt():
    # dd/mm/YY H:M:S
    return (
                f"{(datetime.now()).strftime('%d/%m/%Y %H:%M:%S')}" 
                f"\n----------------------------\n" 
           )

def scrap_page(str_url, reg_search, int_seconds):
    try:
        if t_stamp.too_recent(int_seconds):
            return (f"{get_current_dtt()}Too early to check.", False)
    except Exception as e:
            return (f"{get_current_dtt()}Timestamp Read Error:\n{str(e)}", False)

    try:
        page = requests.get(str_url)
    except Exception as e:
        return (f"{get_current_dtt()}{str(e)}", False)


    if page.status_code != requests.codes.ok:
        return (f"{get_current_dtt()}Download Error.", False)

    x = re.search(reg_search, page.text, flags=re.DOTALL)

    ts_error = ""
    r_days = (date(2021, 12, 11) - date.today()).days

    if x:
        try:
            t_stamp.write_ts()
        except Exception as e:
            ts_error = "Timestamp Write Error:\n" + str(e) + "\n\n"

        
        return (f"{get_current_dtt()}{ts_error}Found. ({r_days})", False)

    return (f"{get_current_dtt()}Not Found. ({r_days})", True)


def main():
    import tkinter as tk
    from tkinter import messagebox

    root = tk.Tk()
    root.withdraw()

    # URL of page to be scrapped
    URL = ""
    # Text to be searched in the page. Can also be a regular expression
    txt = ""
        
    messagebox.showinfo("Screen Scrap", scrap_page(URL, txt, 3 * 60 * 60 -20)[0])



if __name__ == "__main__":
    main()
