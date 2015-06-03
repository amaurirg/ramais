# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################


def index():
    num_ramal = '' 
    form =  SQLFORM.factory(
        Field('keyword', requires = IS_NOT_EMPTY(error_message=''), label='Buscar por nome, ramal ou departamento'),
        formstyle = 'divs',
        submit_button = 'Localizar'
        )
    response.flash = 'Digite um nome ou ramal para a localização!'
    if form.process().accepted:
        num_ramal = db(NR.nome.like('%'+form.vars.keyword+'%')).select() | db(NR.ramal.like(form.vars.keyword)).select() | db(NR.depto.like('%'+form.vars.keyword+'%')).select()
        if not num_ramal:
            response.flash = 'Ramal não encontrado!' 
        else:
            response.flash = 'Ramal localizado!'
    elif form.errors:
        response.flash = 'O campo deve ser preenchido!'        
    return dict(form=form,num_ramal=num_ramal)
    

def novo_ramal():
    form = SQLFORM(NR, formstyle = 'divs', submit_button = 'Cadastrar')
    if form.process().accepted:
        response.flash = 'Ramal criado com sucesso!'
        redirect(URL('user/logout'))
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'Erros no preenchimento ou campo vazio!'
    else:
        response.flash = 'Preencha os campos para cadastrar um novo ramal!'
    form.add_button('Voltar para Página Principal', URL('index'))
    return dict(form=form)


def atualizar_ramal():
    novo = db(NR.id == request.args(0)).select().first()
    response.flash = ''
    form = SQLFORM(NR, novo, formstyle = 'divs', submit_button = 'Alterar Ramal')
    if form.process().accepted:
        response.flash = 'Ramal alterado com sucesso!'
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'Erros no preenchimento ou campo vazio!'
    else:
        response.flash = 'Preencha os campos para alterar um ramal!'
    form.add_button('Voltar para Página Principal', URL('index'))
    return dict(form=form)


def lista_completa_de_ramais():
    todos_ramais = db(NR).select(orderby=NR.ramal)
    return dict(todos_ramais=todos_ramais)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """    
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


#@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)

