# -*- coding: utf-8 -*-

#NR (Nome-Ramal)
NR.nome.requires = IS_NOT_EMPTY(), IS_NOT_IN_DB(db, 'nome_ramal.nome')
NR.depto.requires = IS_NOT_EMPTY()
NR.ramal.requires = IS_NOT_EMPTY(), IS_NOT_IN_DB(db, 'nome_ramal.ramal')
NR.email.requires = IS_NOT_EMPTY()
