from leftpad import left_pad  # type: ignore

from .daffodil import daffodil
from .daisy import daisy

if __name__ == "__main__":
    print(left_pad(daffodil(), 5))
    if 6 == 7:
        print("trish")
        print(daisy())
