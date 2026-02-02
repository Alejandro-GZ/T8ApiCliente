from t8_client.models import ProcMode, Unit


def test_parse_unit() -> None:
    data = {
        "id": 1,
        "factor": 1.0,
        "label": "V",
        "property_name": "Amplitude",
        "property_label": "Volts"
    }

    obj = Unit.parse_unit(data)

    assert isinstance(obj, Unit)
    assert obj.factor == 1.0
    assert obj.id == 1
    assert obj.label == "V"
    assert obj.property_name == ""
    assert obj.property_label == ""
    
def test_set_property_unit() -> None:
    unit = Unit(id=1, factor=1.0, label="V", property_name="", property_label="")
    unit.set_property("Amplitude", "Volts")

    assert unit.property_name == "Amplitude"
    assert unit.property_label == "Volts"
    
def test_parse_obj() -> None:
    data = {
        "name": "Standard",
        "max_freq": 1000,
        "min_freq": 10
    }

    obj = ProcMode.parse_obj(data)

    assert isinstance(obj, ProcMode)
    assert obj.name == "Standard"
    assert obj.max_freq == 1000
    assert obj.min_freq == 10