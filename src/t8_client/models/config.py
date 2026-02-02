from dataclasses import dataclass


@dataclass
class Unit:
    id: int
    factor: float
    label: str
    property_name: str
    property_label: str
    
    @staticmethod
    def parse_unit(dict_obj: dict) -> "Unit":
        return Unit(
            id=dict_obj["id"],
            factor=dict_obj["factor"],
            label=dict_obj["label"],
        )
    def set_property(self, property_name: str, property_label: str) -> None:
        self.property_name = property_name
        self.property_label = property_label

@dataclass
class ProcMode:
    name: str
    max_freq: int
    min_freq: int
    
    def parse_obj(dict_obj: dict) -> "ProcMode":
        return ProcMode(
            name=dict_obj["name"],
            max_freq=dict_obj["max_freq"],
            min_freq=dict_obj["min_freq"],
        )