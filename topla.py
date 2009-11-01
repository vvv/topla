#!/usr/bin/env python

import struct
import sys

def pla_header(n_tracks):
    assert type(n_tracks) is int and n_tracks > 0
    assert n_tracks <= 0xff, 'too many entries for a playlist: %d' % n_tracks
    return '\x00' + struct.pack('B', n_tracks) + '\x00\x01\x00\x00\x00\x00'

def pla_entry(dir_entry_off):
    assert type(dir_entry_off) is int and dir_entry_off >= 0
    seg, seg_off = divmod(dir_entry_off, 512)
    assert seg_off % 32 == 0 and seg >> 32 == 0, \
        'invalid directory table entry offset: 0x%x' % dir_entry_off
    return '\x01\x40' + struct.pack('>H', seg_off/32) + struct.pack('>L', seg)

def pla(de_offsets):
    return pla_header(len(de_offsets)) \
        + reduce(str.__add__, map(pla_entry, de_offsets))

def test():
    def _fails(func, *args):
        try: func(*args)
        except AssertionError: return True

    assert pla_entry(0x0004bfc0) == '\x01\x40\x00\x0e\x00\x00\x02\x5f'
    assert pla_entry(0x0004c0a0) == '\x01\x40\x00\x05\x00\x00\x02\x60'
    assert pla_entry(0x0004c100) == '\x01\x40\x00\x08\x00\x00\x02\x60'
    assert pla_entry(0x1166fe40) == '\x01\x40\x00\x02\x00\x08\xb3\x7f'
    assert pla_entry(0x1166fe80) == '\x01\x40\x00\x04\x00\x08\xb3\x7f'
    assert pla_entry(0x1166fec0) == '\x01\x40\x00\x06\x00\x08\xb3\x7f'
    assert pla_entry(0x1166ff00) == '\x01\x40\x00\x08\x00\x08\xb3\x7f'
    assert pla_entry(0x1166ff40) == '\x01\x40\x00\x0a\x00\x08\xb3\x7f'
    assert pla_header(1) == '\x00\x01\x00\x01\x00\x00\x00\x00'
    assert pla_header(4) == '\x00\x04\x00\x01\x00\x00\x00\x00'
    assert _fails(pla_header, 256)

if __name__ == '__main__':
    # test()
    xs = []
    for s in sys.stdin:
        xs.append(int(s, 16))
    sys.stdout.write(pla(xs))
