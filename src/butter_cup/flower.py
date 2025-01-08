from leftpad import left_pad  # type: ignore

from .daffodil import daffodil
from .daisy import daisy

def flower(pad_to: int) -> str:
    flower_name = left_pad(daffodil(), pad_to)
    print(flower_name)
    if 6 == 7:
        print("trish")
        print(daisy())
    return flower_name

