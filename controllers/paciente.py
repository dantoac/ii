# coding: utf8

@auth.requires_login()
def index():
    data = db(db.paciente).select()
    
    tabla = TABLE(THEAD(TR(
        TH('Nombre'),
        TH('Peso(kg)'),
        TH('Fecha Nacimiento'),
        TH('')
        )), _id = "tabla_pacientes")
    
    for p in data:
        edad = request.now.year - p.fecha_nacimiento.year
        tabla.append(TR(
            TD(A(p.nombre_completo,
            _href = URL(f='nuevo',args=p.id), 
            _class='btn btn-mini')),
            TD(p.peso),
            TD(p.fecha_nacimiento,' ',SPAN(edad,' años',_class='label')),
            TD(A('Aplicar medicamento',
                _href = URL('medicamento','index',vars={'paciente':p.id}),
                _class = 'btn btn-mini btn-primary'))
            ))
   
    tabla = CAT(A('Agregar Paciente',
                _href = URL(f='nuevo'),
                _class = 'btn btn-success')
                ,tabla)
    
    

    return dict(tabla = tabla)

@auth.requires_login()
def nuevo():
    
    form = SQLFORM(db.paciente, request.args(0),
                   submit_button = 'Agregar Paciente')
    
    if form.process().accepted:
        if request.args:
            session.flash = 'Modificación de registro exitosa'
        else:
            session.flash = 'Nuevo registro agregado'
        redirect(URL(f='index'))
    return locals()
