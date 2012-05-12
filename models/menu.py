# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = ' '.join(word.capitalize() for word in request.application.split('_'))
response.subtitle = T('customize me!')

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'
response.meta.copyright = 'Copyright 2011'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Home'), False, URL('default','index'), []),
    ('Pacientes', False, URL('paciente','index')),
    ('Medicamentos', False, URL('medicamento','index')),
    ('Dosificaciones', False, URL('dosis','index'))
    ]




def menuser():
    '''
    Esta función emula a la existente auth.navbar(), agregándole las firmas de
    usuario a los enlaces de rebote (opcionales).
    '''
    
    ulink = ''

    def nextgo(c='',f='',a=request.args,v=request.vars):
        urlnext = dict(_next=URL(c=c, f=f, args=a, vars=v, user_signature = True))
        return urlnext

    if auth.is_logged_in():
        menuser_item = CAT(
            LI(A(auth.user.first_name.capitalize(),' ',
                 auth.user.last_name.capitalize(),
                          _class="noprint brand")),
            LI(A(T('Salir'), _class="noprint", _title=T('Salir del Sistema'), _href=URL('default','user',args='logout',vars=nextgo(c='ads',f='index')))),
            LI(A(T('Mis Datos'), _class="noprint", _title='Cambiar Nombre, E-Mail o Contraseña de Supervisión', _href=URL('default','user',args='profile',vars=nextgo()))),
            LI(A(T('Contraseña'), _class="noprint", _title=T('Cambiar Contraseña de Usuario'),_href=URL('default','user',args='change_password',vars=nextgo()))),
            
        )
    else:
        menuser_item = LI(A(T('Identificarse'),  _class="noprint", _href=URL('default','user',args='login')))
        if not 'register' in auth.settings.actions_disabled:
            menuser_item.append(LI(A(T('Registrarse'),  _class="noprint", _href=URL('default','user',args='register'))))
        menuser_item.append(LI(A(T('¿Contraseña Perdida?'), _class="noprint",  _href=URL('default','user',args='request_reset_password'))))
            
        
 
    menuser = UL(menuser_item, _class='nav pull-right')
        
    #ulink = ' | '.join([i.xml() for i in menuser_item])
        
    return menuser
