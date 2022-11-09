import os
import sys
import platform
import datetime

# if some problems happend, try remove this file
LOCK_FILE='/home/v/.cache/rsync/rsync_i.lock'
LOG_FILE='/home/v/.cache/rsync/rsync_i.log'
LOCK_FILE=sys.path[0]+os.sep+LOCK_FILE
LOG_FILE=sys.path[0]+os.sep+LOG_FILE


def sync_fns():
    log_info('starting syncs ...')
    # add your sync functions
    # sync(r'C:\Users\v\asset', r'V:\home\asset', 'V')
    sync(r'/home/v/asset', r'/run/media/v/v/home/asset', '/run/media/v/v/home/')

def chekc_disk(_disk):
    log_info(f'checking disk "{_disk}" ...')
    suffix='/'
    if platform.system()=='Windows':
        suffix=':/'
    target_root=f'{_disk}{suffix}'
    return os.path.exists(target_root)


def check_lock():
    log_info('checking lock...')
    if os.path.exists(LOCK_FILE):
        log_err('another process running, return.')
        exit(0)


def add_lock():
    log_info('adding lock file...')
    open(LOCK_FILE, "w")
    log_info('lock file added')


def rm_lock():
    log_info('deleting lock file...')
    os.remove(LOCK_FILE)
    log_info('lock file deleted')


def sync(_source_dir, _target_dir, _target_disk):
    try:
        _source_dir=_source_dir.strip()
        _target_dir=_target_dir.strip()
        _target_disk=_target_disk.strip()

        if _source_dir == "":
            log_err('_source_dir can not be empty')
            return
        if _target_dir == "":
            log_err('_target_dir can not be empty')
            return
        if _target_disk == "":
            log_err('_target_disk can not be empty')
            return

        if not chekc_disk(_target_disk):
            raise Exception(f'disk "{_target_disk}" not exist, return.')

        _source_dir=change_dir_case(_source_dir)
        _source_dir=append_dir_suffix(_source_dir)
        _target_dir=change_dir_case(_target_dir)
        _target_dir=append_dir_suffix(_target_dir)

        command='rsync'
        options='alrtux'
        params=f'{_source_dir} {_target_dir}'
        command_line=f'{command} -{options} {params}'
        log_info(f'starting sync "{_source_dir}" to "{_target_dir}" using "{command_line}" ...')
        r=os.system(command_line)
        log_info(f'sync "{_source_dir}" to "{_target_dir}" end: {r}')
    except Exception as e:
        log_err(f'sync "{_source_dir}" to "{_target_dir}" faild: {e}')


def change_dir_case(_dir):
    if platform.system()!='Windows':
        return _dir

    prefix='/cygdrive/'
    if _dir.startswith(prefix):
        return _dir

    _dir=_dir.replace(':', '')
    if '\\' in _dir:
        _dir=_dir.replace('\\', '/')
    _dir = prefix + _dir
    return  _dir

def append_dir_suffix(_dir):
    if not _dir.endswith('/'):
        _dir=_dir+'/'
    return _dir

def append_log(_time, _result, _msg):
    try:
        with open(LOG_FILE,"a") as f:
            _time=_time.strftime("%Y-%m-%d %H:%M:%S")
            line=f'[{_time}] [{_result}] {_msg}\n'
            print(line)
            f.write(line)
    except Exception as e:
        log_err(f'write log faild: {e}')

def log_info(_msg):
    log_with_print('info', _msg)
def log_err(_msg):
    log_with_print('error', _msg)

def log_with_print(_type, _msg):
    now = datetime.datetime.now()
    append_log(now, _type, _msg)

if __name__ == '__main__':
    check_lock()
    add_lock()

    try:
        sync_fns()
    finally:
        rm_lock()
