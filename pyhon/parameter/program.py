from typing import List, TYPE_CHECKING, Dict

from pyhon.parameter.enum import HonParameterEnum

if TYPE_CHECKING:
    from pyhon.commands import HonCommand


class HonParameterProgram(HonParameterEnum):
    _FILTER = ["iot_recipe", "iot_guided"]

    def __init__(self, key: str, command: "HonCommand", group: str) -> None:
        super().__init__(key, {}, group)
        self._command = command
        if "PROGRAM" in command.category:
            self._value: str = command.category.split(".")[-1].lower()
        else:
            self._value: str = command.category
        self._programs: Dict[str, "HonCommand"] = command.categories
        self._typology: str = "enum"

    @property
    def value(self) -> str | float:
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        if value in self.values:
            self._command.category = value
        else:
            raise ValueError(f"Allowed values {self.values}")

    @property
    def values(self) -> List[str]:
        values = [v for v in self._programs if all(f not in v for f in self._FILTER)]
        return sorted(values)

    @property
    def ids(self):
        values = {
            int(p.parameters["prCode"].value): n
            for i, (n, p) in enumerate(self._programs.items())
            if "iot_" not in n and p.parameters.get("prCode")
        }
        return dict(sorted(values.items()))