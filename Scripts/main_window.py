# -*- coding: utf-8 -*-

from .text import Text
from .zodiac import Zodiac
from .messagebox import MsgBox
from .utilities import convert_degree
from .modules import tk, swe, Thread, datetime64
from .selection import (
    PlanetSelection, SignSelection, 
    YearRangeSelection, OrbSelection
)


class MainWindow(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack()
        self.start = False
        self.left_frame = tk.Frame(master=self)
        self.left_frame.pack(side="left")
        self.right_frame = tk.Frame(master=self)
        self.right_frame.pack(side="right")
        self.selection_frame = tk.Frame(master=self.left_frame)
        self.selection_frame.pack()
        self.planet = PlanetSelection(master=self.selection_frame)
        self.planet.pack(side="left")
        self.sign = SignSelection(master=self.selection_frame)
        self.sign.pack(side="left")
        self.year_range = YearRangeSelection(master=self.left_frame)
        self.year_range.pack()
        self.orb = OrbSelection(master=self.left_frame)
        self.orb.pack()
        self.button_frame = tk.Frame(master=self.left_frame)
        self.button_frame.pack()
        self.start_button = tk.Button(
            master=self.button_frame, 
            text="Start",
            command=lambda: Thread(
                target=self.start_searching,
                daemon=True
            ).start()
        )
        self.start_button.pack(side="left")
        self.stop_button = tk.Button(
            master=self.button_frame, 
            text="Stop",
            command=self.stop_searching
        )
        self.stop_button.pack(side="right")
        self.text = Text(master=self.right_frame)
        self.text.pack(side="left")
        
    @staticmethod
    def get_selection(selection, _type):
        if _type == list:
            return [
                k for k, w in selection.widgets.items()
                if w[0].get() and k != "Select All"
            ]
        elif _type == float:
            return [
                w[0].get() for k, w in selection.widgets.items()
            ]
        elif _type == dict:
            return {
                k: w[0].get()
                for k, w in selection.widgets.items()
            }
    
    def get_all_selections(self):
        return {
            "planets": self.get_selection(self.planet, list),
            "signs": self.get_selection(self.sign, list),
            "year_range": self.get_selection(self.year_range, dict),
            "orb": self.get_selection(self.orb, float)
        }
    
    @staticmethod
    def get_dates(start, end):
        d1 = datetime64(f"{start}-01-01")
        d2 = datetime64(f"{end}-01-01")
        for i in range((d2 - d1).astype(int)):
            splitted = str(d1 + i).split("-")
            if len(splitted) == 4:
                splitted = ("-" + splitted[1], *splitted[2:])
            yield tuple(map(int, splitted))
                    
    @staticmethod  
    def is_all_signs_same(patterns):
        return True if len(set(i[1] for i in patterns)) == 1 else False

    @staticmethod
    def is_in_signs(patterns, signs):
        return True if patterns[0][1] in signs else False

    @staticmethod
    def is_conjunction(patterns, orb):
        return all(
            0 <= abs(patterns[i][-1] - j[-1]) <= orb
            for i in range(len(patterns))
            for j in patterns[i + 1:]
        )
    
    @staticmethod
    def reformat_date(date):
        return ".".join(map(lambda i: i.zfill(2), map(str, date[::-1])))

    @staticmethod
    def reformat_patterns(patterns):
        return ", ".join(
            [
                "(" + 
                i[0] + 
                " " + 
                " ".join(convert_degree(i[2], dms=True)[::-1]) + 
                ")"
                for i in patterns
            ]
        )
    
    def tag_configure(self, index):
        self.text.tag_add(
            f"name-{index}", 
            f"{index}.0", 
            f"{index}.5"
        )
        self.text.tag_add(
            f"name-{index + 1}", 
            f"{index + 1}.0", 
            f"{index + 1}.10"
        )
        self.text.tag_configure(
            f"name-{index}", 
            font="TkFixedFont 10 bold"
        )
        self.text.tag_configure(
            f"name-{index + 1}", 
            font="TkFixedFont 10 bold"
        )
        
    def stop_searching(self):
        self.start = False
        
    @staticmethod
    def has_error(selections):
        for key, value in selections.items():
            if (
                    not value 
                    or 
                    value == {'From': '', 'To': ''} 
                    or 
                    value == [""]
            ):
                MsgBox(
                    title="Warning",
                    message=f"Select {key.replace('_', ' ').title()}!",
                    level="warning"
                )
                return True
            if key == "year_range":
                for k, v in value.items():
                    if not v:
                        MsgBox(
                            title="Warning",
                            message=f"Select {k}!",
                            level="warning"
                        )
                        return True
                    try:
                        int(v)
                    except ValueError:
                        MsgBox(
                            title="Warning",
                            message=f"{k.title()} is not number!",
                            level="warning"
                        )
                        return True
                    if not -12998 <= int(v) <= 16799:
                        MsgBox(
                            title="Warning",
                            message=(
                                f"{k.title()} should be between\n"
                                f"-12998 and 16799"
                            ),
                            level="warning"
                        )
                        return True
                if int(value["From"]) >= int(value["To"]):
                    MsgBox(
                        title="Warning",
                        message=(
                            f"To can not be lower than or\n"
                            f"equal to From."
                        ),
                        level="warning"
                    )
                    return True
            elif key == "orb":
                try:
                    float(value[0])
                except ValueError:
                    MsgBox(
                        title="Warning",
                        message=f"{key.title()} is not number!",
                        level="warning"
                    )
                    return True
                
    def start_searching(self):
        self.start = True
        selections = self.get_all_selections()
        if self.has_error(selections):
            return
        self.text["state"] = "normal"
        self.text.delete("1.0", "end")
        index = 1
        for date in self.get_dates(
            *map(int, selections["year_range"].values())
        ):
            try:
                patterns = Zodiac(*date).patterns(selections["planets"])
            except swe.Error:
                MsgBox(
                    title="Warning",
                    message=(
                        "Chiron's ephemeris is limited between\n"
                        "650 and 4650."
                    ),
                    level="warning"
                )
                return
            if (
                self.is_all_signs_same(patterns)
                and
                self.is_in_signs(patterns, selections["signs"])
                and
                self.is_conjunction(patterns, float(selections["orb"][0]))
            ):
                try:
                    self.text["state"] = "normal"
                    self.text.insert(
                        "end", 
                        f"Date: {self.reformat_date(date)}\n"
                    )
                    self.text.insert(
                        "end", 
                        f"Positions: {self.reformat_patterns(patterns)}\n\n"
                    )
                    self.tag_configure(index=index)
                    index += 3
                    self.text["state"] = "disabled"
                    self.text.update()
                except tk.TclError:
                    return
            if not self.start:
                return
        self.master.after(
            0,
            lambda: MsgBox(
                title="Info",
                message=f"Search is complete.",
                level="info"
            )
        )
