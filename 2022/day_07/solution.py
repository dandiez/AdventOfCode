import dataclasses
from typing import Optional
from unittest import TestCase

full_path = str


@dataclasses.dataclass
class FileSystemObject:
    name: str

    @property
    def full_path(self):
        p = self.name
        parent = self.parent
        while parent != None:
            p = parent.name + "/" + p
            parent = parent.parent
        return p


@dataclasses.dataclass
class File(FileSystemObject):
    size: int
    parent: 'Dir'


@dataclasses.dataclass
class Dir(FileSystemObject):
    parent: Optional['Dir']
    dirs: dict[str, 'Dir']
    files: list[File]
    _size = None

    @property
    def size(self):
        if self._size is not None:
            return self._size
        s = sum(f.size for f in self.files)
        s += sum(d.size for d in self.dirs.values())
        self._size = s
        return self._size


@dataclasses.dataclass
class FileSystem:
    dirs: dict[full_path, Dir]
    files: dict[full_path, File]
    current_dir: Dir

    @classmethod
    def init_with_root(cls):
        root = Dir(name="/", parent=None, dirs={}, files=[])
        return FileSystem(
            dirs={"/": root},
            files={},
            current_dir=root
        )

    def cd(self, rel_dir: str):
        if rel_dir in self.current_dir.dirs:
            self.current_dir = self.current_dir.dirs[rel_dir]
        elif rel_dir.strip() == "..":
            self.current_dir = self.current_dir.parent
        else:
            print(f"cannot find relative path {rel_dir}")

    def mkdir(self, dir_name: str):
        new = Dir(name=dir_name, parent=self.current_dir, dirs={}, files=[])
        self.dirs[new.full_path] = new
        self.current_dir.dirs[dir_name] = new

    def mkfile(self, file_name: str, size: int):
        new = File(name=file_name, size=size, parent=self.current_dir)
        self.current_dir.files.append(new)
        self.files[new.full_path] = new


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    return lines


def part_1(inp):
    fsys = FileSystem.init_with_root()
    for command in inp:
        if command.startswith("$ cd"):
            dir = command[5:].strip()
            fsys.cd(dir)
        elif command.startswith("$ ls"):
            continue
        elif command.startswith("dir "):
            dir_name = command[4:].strip()
            fsys.mkdir(dir_name)
        else:
            size, fname = command.split(" ")
            fsys.mkfile(fname, int(size))

    return sum(d.size for d in fsys.dirs.values() if d.size <= 100000)


def part_2(inp):
    fsys = FileSystem.init_with_root()
    for command in inp:
        if command.startswith("$ cd"):
            dir = command[5:].strip()
            fsys.cd(dir)
        elif command.startswith("$ ls"):
            continue
        elif command.startswith("dir "):
            dir_name = command[4:].strip()
            fsys.mkdir(dir_name)
        else:
            size, fname = command.split(" ")
            fsys.mkfile(fname, int(size))

    root_size = fsys.dirs["/"].size
    total_space = 70000000
    free_space_needed = 30000000
    available_space = total_space - root_size
    all_sizes = [d.size for d in fsys.dirs.values()]
    all_sizes.sort()
    for s in all_sizes:
        if available_space + s >= free_space_needed:
            return s


def main(input_file):
    """Solve puzzle and connect part 1 with part 2 if needed."""
    # part 1
    inp = read_input(input_file)
    p1 = part_1(inp)
    print(f"Solution to part 1: {p1}")

    # part 2
    inp = read_input(input_file)
    p2 = part_2(inp)
    print(f"Solution to part 2: {p2}")
    return p1, p2


def test_sample_1(self):
    inp = read_input("sample_1")
    self.assertEqual(95437, part_1(inp))


def test_sample_2(self):
    pass


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
