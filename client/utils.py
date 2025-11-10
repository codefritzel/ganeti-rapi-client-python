from dataclasses import fields, is_dataclass
from typing import Any, Dict, List, Type, TypeVar, Union, cast

T = TypeVar("T")  # generic type for any dataclass


def dict_to_dataclass(cls: Type[T], data: Dict[str, Any]) -> T:
    """Convert a dict to a dataclass recursively."""
    if not is_dataclass(cls):
        raise TypeError(f"{cls} is not a dataclass type")

    kwargs: Dict[str, Any] = {}
    for field in fields(cls):
        if field.name in data:
            if is_dataclass(field.type) and isinstance(data[field.name], dict):
                kwargs[field.name] = dict_to_dataclass(cast(Type[T], field.type), data[field.name])
            else:
                kwargs[field.name] = data[field.name]
    return cls(**kwargs)


def dataclass_to_dict(obj: Any) -> Union[Dict[str, Any], List[Any], Any]:
    """Convert a dataclass to a dict recursively."""
    if is_dataclass(obj):
        result: Dict[str, Any] = {}
        for field in obj.__dataclass_fields__:
            value = getattr(obj, field)
            if value is not None:
                result[field] = dataclass_to_dict(value)
        return result
    if isinstance(obj, (list, tuple)):
        return [dataclass_to_dict(item) for item in obj]
    if isinstance(obj, dict):
        return {k: dataclass_to_dict(v) for k, v in obj.items()}
    return obj
