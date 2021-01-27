import json
import dataclasses
from typing import List, Dict, Type, Tuple, Union, TypeVar

T = TypeVar("T", bound="JsonableDataclass")
JSON = Union[Dict[str, "JSON"], List["JSON"], str, int, float, bool, None]


class JsonableDataclass:
    __json_fields__: Tuple[str, ...] = ()

    def __init__(self, **kwargs) -> None:
        pass

    def to_dict(self, only_json: bool = False) -> Dict[str, JSON]:
        kvs: Dict[str, JSON] = dataclasses.asdict(self)
        if only_json:
            return {k: v for k, v in kvs.items() if k in self.__json_fields__}
        return kvs

    @classmethod
    def from_dict(cls: Type[T], kvs: Dict[str, JSON]) -> T:
        # TODO: nested dataclass
        return cls(**kvs)

    def to_json(self,
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
                **kw) -> str:
        return json.dumps(self.to_dict(only_json),
                          skipkeys=skipkeys,
                          ensure_ascii=ensure_ascii,
                          check_circular=check_circular,
                          allow_nan=allow_nan,
                          cls=cls,
                          indent=indent,
                          separators=separators,
                          default=default,
                          sort_keys=sort_keys,
                          **kw)

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
            **kw) -> T:
        return __dataclass__.from_dict(
            json.loads(json_str,
                       cls=cls,
                       object_hook=object_hook,
                       parse_float=parse_float,
                       parse_int=parse_int,
                       parse_constant=parse_constant,
                       object_pairs_hook=object_pairs_hook,
                       **kw))  # type: ignore
