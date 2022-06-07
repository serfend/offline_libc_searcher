import platform
import sgtlibc.ROPgadgets
import pytest
from .common import get_elf_resources


@pytest.mark.skipif(platform.uname()[0] == 'Windows', reason='skip windows')
@pytest.mark.skipif(platform.uname()[0] == 'Darwin', reason='skip mac')
def test_rop_get():
    path = get_elf_resources('pwn1')
    elf = sgtlibc.ROPgadgets.ELF(path)
    data = elf.get_rop()

    assert 'ret' in data and data['ret'] == 0x4005d9
    assert 'rdi' in data and data['rdi'] == 0x400a03