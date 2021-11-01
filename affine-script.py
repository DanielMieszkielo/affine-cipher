from dataclasses import dataclass, asdict
from enum import Enum
from typing import Optional
import json
import sys


class OperationType(Enum):
    encrypt = "encrypt"
    decrypt = "decrypt"


@dataclass
class Data:
    a: int
    b: int
    operation: OperationType
    plainText: Optional[str] = None
    cryptogram: Optional[str] = None


class Affine:
    def __init__(self, a: int, b: int):
        self.a = a
        self.b = b
        self.m = 26
        self.char_offset = ord("A")

    def encrypt(self, message: str) -> str:
        return "".join(self._encrypt_character(char) for char in message)

    def decrypt(self, encrypted_message: str) -> str:
        return "".join(self._decrypt_character(char) for char in encrypted_message)

    def _encrypt_character(self, char: str) -> str:
        x = self._to_int(char)
        return self._to_str((self.a * x + self.b) % self.m)

    def _decrypt_character(self, char: str) -> str:
        x = self._to_int(char)
        return self._to_str((pow(self.a, -1, self.m) * (x - self.b)) % self.m)

    def _to_int(self, char: str) -> int:
        return ord(char) - self.char_offset

    def _to_str(self, x: int) -> str:
        return chr(x + self.char_offset)


def load_json(file_path: str) -> Data:
    with open(file_path) as file:
        return Data(**json.loads(file.read()))


def save_json(file_path: str, data: Data) -> None:
    with open(file_path, "w") as file:
        file.write(json.dumps(asdict(data)))


def run_script(file_path: str):
    data = load_json(file_path)

    affine = Affine(a=data.a, b=data.b)

    if data.operation == OperationType.encrypt.value:
        data.cryptogram = affine.encrypt(data.plainText)
    elif data.operation == OperationType.decrypt.value:
        data.plainText = affine.decrypt(data.cryptogram)

    save_json(file_path, data)


if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Need to specify a json file as a first argument")
        exit()

    run_script(sys.argv[1])
