"""Dataclass Related Tools

This module is used to build dataclass related tools.

:Copyright: Copyright (C) 2021-2021  yanyongyu
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/yanyongyu/CAI/blob/master/LICENSE
"""
import json
import copy
from dataclasses import _is_dataclass_instance, fields, MISSING, is_dataclass
from typing import IO, Any, List, Dict, Type, Tuple, Union, TypeVar, Mapping, Collection

T = TypeVar("T", bound="JsonableDataclass")
JSON = Union[Dict[str, "JSON"], List["JSON"], str, int, float, bool, None]


def _asdict(obj: Any) -> Any:
    if _is_dataclass_instance(obj):
        result = []
        for f in fields(obj):
            value = _asdict(getattr(obj, f.name))
            result.append((f.name, value))
        return dict(result)
    elif isinstance(obj, Mapping):
        return dict((_asdict(k), _asdict(v)) for k, v in obj.items())
    elif isinstance(
        obj, Collection
    ) and not isinstance(obj, str) and not isinstance(obj, bytes):
        return list(_asdict(v) for v in obj)
    else:
        return copy.deepcopy(obj)


def _convert_type(type_, value):
    if type_ is None or type_ == Any or isinstance(
        type_, TypeVar
    ) or type_ is Ellipsis:
        return value
    elif is_dataclass(type_):
        return _fromdict(type_, value)
    return type_(value)


def _fromdict(cls, kvs):
    kvs = kvs.copy()

    init_kwargs = {}
    for field in fields(cls):
        if not field.init:
            continue

        field_value = kvs.get(field.name, MISSING)
        field_type = field.type
        if field_value is MISSING:
            continue

        if is_dataclass(field_type):
            if is_dataclass(field_value):
                value = field_value
            else:
                value = _fromdict(field_type, field_value)
            init_kwargs[field.name] = value
        elif hasattr(field_type, "__origin__"
                    ) and issubclass(field_type.__origin__, Mapping):
            k_type, v_type = getattr(field_type, "__args__", (Any, Any))
            init_kwargs[field.name] = field_type.__origin__(
                zip(
                    [
                        (
                            _convert_type(k_type,
                                          key), _convert_type(v_type, value)
                        ) for key, value in field_value.items()
                    ]
                )
            )  # type: ignore
        elif hasattr(field_type, "__origin__"
                    ) and issubclass(field_type.__origin__, Collection):
            type_ = getattr(field_type, "__args__", (Any,))[0]
            init_kwargs[field.name] = field_type.__origin__(
                _convert_type(type_, value) for value in field_value
            )  # type: ignore
        elif hasattr(
            field_type, "__origin__"
        ) and field_type.__origin__ is Union:
            value = field_value
            for type_ in field_type.__args__:
                try:
                    value = _convert_type(type_, field_value)
                    break
                except Exception:
                    continue
            init_kwargs[field.name] = value
        else:
            init_kwargs[field.name] = field_value

    return cls(**init_kwargs)


class JsonableDataclass:
    __json_fields__: Tuple[str, ...] = ()

    def __init__(self, **kwargs) -> None:
        pass

    def to_dict(self, only_json: bool = False) -> Dict[str, JSON]:
        kvs: Dict[str, JSON] = _asdict(self)
        if only_json:
            return {k: v for k, v in kvs.items() if k in self.__json_fields__}
        return kvs

    @classmethod
    def from_dict(cls: Type[T], kvs: Dict[str, JSON]) -> T:
        return _fromdict(cls, kvs)

    def to_json(
        self,
        only_json: bool = True,
        *,
        skipkeys=False,
        ensure_ascii=True,
        check_circular=True,
        allow_nan=True,
        cls=None,
        indent=None,
        separators=None,
        default=None,
        sort_keys=False,
        **kw
    ) -> str:
        return json.dumps(
            self.to_dict(only_json),
            skipkeys=skipkeys,
            ensure_ascii=ensure_ascii,
            check_circular=check_circular,
            allow_nan=allow_nan,
            cls=cls,
            indent=indent,
            separators=separators,
            default=default,
            sort_keys=sort_keys,
            **kw
        )

    @classmethod
    def from_json(
        __dataclass__: Type[T],  # type: ignore
        json_str: str,
        *,
        cls=None,
        object_hook=None,
        parse_float=None,
        parse_int=None,
        parse_constant=None,
        object_pairs_hook=None,
        **kw
    ) -> T:
        return __dataclass__.from_dict(
            json.loads(
                json_str,
                cls=cls,
                object_hook=object_hook,
                parse_float=parse_float,
                parse_int=parse_int,
                parse_constant=parse_constant,
                object_pairs_hook=object_pairs_hook,
                **kw
            )
        )  # type: ignore

    def to_file(
        self,
        fp: IO[str],
        only_json: bool = True,
        *,
        skipkeys=False,
        ensure_ascii=True,
        check_circular=True,
        allow_nan=True,
        cls=None,
        indent=None,
        separators=None,
        default=None,
        sort_keys=False,
        **kw
    ) -> None:
        return json.dump(
            self.to_dict(only_json),
            fp,
            skipkeys=skipkeys,
            ensure_ascii=ensure_ascii,
            check_circular=check_circular,
            allow_nan=allow_nan,
            cls=cls,
            indent=indent,
            separators=separators,
            default=default,
            sort_keys=sort_keys,
            **kw
        )

    @classmethod
    def from_file(
        __dataclass__: Type[T],  # type: ignore
        fp: IO[str],
        *,
        cls=None,
        object_hook=None,
        parse_float=None,
        parse_int=None,
        parse_constant=None,
        object_pairs_hook=None,
        **kw
    ) -> T:
        return __dataclass__.from_dict(
            json.load(
                fp,
                cls=cls,
                object_hook=object_hook,
                parse_float=parse_float,
                parse_int=parse_int,
                parse_constant=parse_constant,
                object_pairs_hook=object_pairs_hook,
                **kw
            )
        )  # type: ignore
