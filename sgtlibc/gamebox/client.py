from sgtlibc.ROPgadgets.ExtendELF import ELF
from .config import GameBoxConfig
from sgtpyutils.logger import logger
from typing import Tuple
import pwn
import os
import sys
from .tube import tube
client: tube = None
is_local: bool = False
tube_file: str = None
tube_remote: Tuple = None
elf: ELF = None


def attach(gdbscript: str = None):
    c = check_client()
    pwn.gdb.attach(
        target=c,
        gdbscript=gdbscript,
    )


def is_64_or_86():
    global elf
    if not elf:
        raise Exception(
            'elf not inited. you can use `start_game` and pass a file-path to init it.')
    return '64' in elf.arch


def set_config(config: GameBoxConfig = None):
    '''
    configure setting of game-box
    '''
    if not config:
        config = GameBoxConfig()
        logger.warning(f'config not specify , initialize with {config}')
    else:
        logger.info(f'config been set to :{config}')
    global tube_file
    tube_file = config.file
    global tube_remote
    tube_remote = config.tube_remote
    global is_local
    is_local = config.is_local
    global client
    client = None
    global elf
    elf = config.elf

    pwn.context.clear()
    pwn.context.log_level = config.log_level
    pwn.context.os = config.os
    pwn.context.arch = config.arch
    pwn.context.terminal = config.terminal

    if config.auto_start_game:
        start_game()


def check_client():
    global client
    '''
    check if client (remote/local) is available
    '''
    if not client:
        start_game()
        if not client:
            logger.error('client not available,please check your config')
            sys.exit(0)
    return client


def start_game(attach_to_client: bool = True):
    '''
    start a game base on current-config
    if attach_to_client is True,client will set to return-result
    '''
    global is_local
    local = is_local
    if local:
        global tube_file
        if not tube_file:
            logger.warning('local elf-file havn\'t been set')
            return None
        os.system(f'chmod 777 {tube_file}')
        r = pwn.process(tube_file)
    else:
        global tube_remote
        if not tube_remote:
            logger.warning('remote host havn\'t been set')
            return None
        r = pwn.remote(tube_remote[0], tube_remote[1])
    if attach_to_client:
        global client
        if client:
            try:
                client.close()
            except:
                pass
        client = r
    return r
