from typing import Literal, TypeAlias


OperationOption: TypeAlias = Literal["encrypt", "decrypt"]
ModeOption: TypeAlias = Literal["ECB", "CBC"]