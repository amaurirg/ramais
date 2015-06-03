# =*= coding: utf-8 -*-

#Ramais
NR = db.define_table('nome_ramal',
	Field('nome', notnull=True, label="Nome"),
	Field('ramal', notnull=True, label="Ramal"),
	Field('depto', notnull=True, label="Departamento"),
	Field('email', notnull=True, label="Email"),
	format = '%(nome)s - %(ramal)s'
	)
