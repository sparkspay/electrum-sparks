# -*- coding: utf-8 -*-
#
# Electrum - lightweight Bitcoin client
# Copyright (C) 2018 The Electrum developers
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import json


def read_json(filename, default):
    path = os.path.join(os.path.dirname(__file__), filename)
    try:
        with open(path, 'r') as f:
            r = json.loads(f.read())
    except:
        r = default
    return r


class BitcoinMainnet:

    TESTNET = False
    WIF_PREFIX = 198
    ADDRTYPE_P2PKH = 38
    ADDRTYPE_P2SH = 10
    GENESIS = "00000a5c6ddfaac5097218560d5b92d416931cfeba1abf10c81d1d6a232fc8ea"
    DEFAULT_PORTS = {'t': '50001', 's': '50002'}
    DEFAULT_SERVERS = read_json('servers.json', {})
    CHECKPOINTS = read_json('checkpoints.json', [])

    XPRV_HEADERS = {
        'standard':    0x0488ade4,  # xprv
    }
    XPUB_HEADERS = {
        'standard':    0x0488b21e,  # xpub
    }
    DRKV_HEADER = 0x0488ade4
    DRKP_HEADER = 0x0488b21e
    BIP44_COIN_TYPE = 5


class BitcoinTestnet:

    TESTNET = True
    WIF_PREFIX = 240
    ADDRTYPE_P2PKH = 112
    ADDRTYPE_P2SH = 20
    GENESIS = "000005f15ec2b9e4495efb539fb5b113338df946291cccd8dfd192bb68cd6dcf"
    DEFAULT_PORTS = {'t': '51001', 's': '51002'}
    DEFAULT_SERVERS = read_json('servers_testnet.json', {})
    CHECKPOINTS = read_json('checkpoints_testnet.json', [])

    XPRV_HEADERS = {
        'standard':    0x04358394,  # tprv
    }
    XPUB_HEADERS = {
        'standard':    0x043587cf,  # tpub
    }
    DRKV_HEADER = 0x04358394  # DRKV
    DRKP_HEADER = 0x043587cf  # DRKP
    BIP44_COIN_TYPE = 1


class BitcoinRegtest(BitcoinTestnet):

    GENESIS = "00000a584fb9211f6dc67cebc024138caa9e387274bf91400cbb2aa49c53ceca"
    DEFAULT_SERVERS = read_json('servers_regtest.json', {})
    CHECKPOINTS = []


# don't import net directly, import the module instead (so that net is singleton)
net = BitcoinMainnet


def set_mainnet():
    global net
    net = BitcoinMainnet


def set_testnet():
    global net
    net = BitcoinTestnet


def set_regtest():
    global net
    net = BitcoinRegtest
