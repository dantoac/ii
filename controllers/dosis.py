# coding: utf8

@auth.requires_login()
def index():
    if 'medicamento_desconocido' in request.args or  'paciente_desconocido' in request.args:
        response.flash = 'Debe primero escoger un Paciente y luego un Medicamento'

    data = db(db.dosis).select()

    tabla = TABLE(THEAD(TR(
        TH('Paciente'),
        TH('Medicamento'),
        TH('Dosis'),
        TH('Medicado'),
        TH('Detalle'),
        TH(),
        )))
    
    for d in data:

        edad = request.now.year - d.paciente.fecha_nacimiento.year
        
        tabla.append(TR(
            TD(d.paciente.nombre_completo,BR(),
               SPAN(d.paciente.peso,'kg, ',edad,' años', _class='label')
               ),
            TD(d.medicamento.nombre),
            TD(d.cantidad,d.metrica,' cada ',d.horas,'hr por ',d.dias,' días'),
            TD(d.comienza),
            TD(d.detalle or EM('Sin detalle')),
            TD(A('Modificar',
                 _href = URL(f='nueva', args = d.id,
                             vars = dict(paciente = d.paciente, medicamento = d.medicamento)),
                 _class='btn btn-mini btn-danger'))
            ))
                
    return locals()

@auth.requires_login()
def nueva():
    paciente = db.paciente(request.vars.paciente) or redirect(URL(f='index', args='paciente_desconocido'))
    medicamento = db.medicamento(request.vars.medicamento) or redirect(URL(f='index',args='medicamento_desconocido'))
    
    cantidad = paciente.peso * medicamento.cantidad
    metrica = medicamento.metrica
    
    db.dosis.cantidad.default = cantidad
    #db.dosis.cantidad.writable = False
    db.dosis.metrica.default = metrica
    #db.dosis.metrica.writable = False
    db.dosis.paciente.default = paciente.id
    db.dosis.paciente.writable = False
    db.dosis.medicamento.default = medicamento.id
    db.dosis.medicamento.writable = False
    
    form = SQLFORM(db.dosis, request.args(0),
                   submit_button = 'Registrar Dosis')

    if form.process().accepted:
        if request.args:
            session.flash = 'Modificación de registro exitosa'
        else:
            session.flash = 'Nuevo registro agregado'
        redirect(URL(f='index'))

    
    
    return locals()
    
