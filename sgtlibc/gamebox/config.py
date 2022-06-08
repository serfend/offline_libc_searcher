from ..ROPgadgets import ELF


class GameBoxConfig:
    def __init__(self, is_local: bool = True, file: str = None, remote: str = None, arch: str = 'amd64', os: str = 'linux', log_level: str = 'debug', auto_load: bool = False, auto_show_rop: bool = False, auto_start_game: bool = True, auto_show_summary: bool = False):
        '''
        if auto_load is True, it would auto load its context.amd you can use `pc`/`uc` also, instead of `p32`/`u32` or `p64`/`u64`.
        if auto_show_rop is True, equal to call `elf.get_rop()`
        if auto_show_summary is True, elf summary info will be show on screen
        '''
        self.is_local = is_local
        self.file = file
        self.remote = remote
        self.auto_load = auto_load
        self.elf = ELF(file, checksec=auto_show_summary) if auto_load else None
        if self.elf:
            pass
            if auto_show_rop:
                self.elf.get_rop()
        self.auto_start_game = auto_start_game
        self.arch = self.elf.arch if self.elf else arch
        self.os = os
        self.log_level = log_level
        pass

    @property
    def tube_remote(self):
        r = self.remote
        if not r:
            return None
        host, port = r.split(':')
        return (host, port)

    def __repr__(self) -> str:
        r = []
        r.append(self.file or 'NO FILE')
        r.append(self.remote or 'NO REMOTE')
        r.append('LOCAL' if self.is_local else 'REMOTE')
        return '|'.join(r)
