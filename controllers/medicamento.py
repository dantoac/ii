# coding: utf8

@auth.requires_login()
def index():
    
    if request.vars.paciente:
        paciente = db.paciente(request.vars.paciente)
        if paciente:
            response.title = 'Medicandoa a: ',paciente.nombre_completo
    
    data = db(db.medicamento).select()
    
    tabla = TABLE(THEAD(TR(
    TH('Nombre'),
    TH('Para'),
    TH('Dosis'),
    TH(''),
    )), _class = "table")
    
    for m in data:
        if request.vars.paciente:
            dosificando = A('Dosificar', 
                       _href = URL('dosis', 'nueva', vars = {
                       'medicamento' : m.id,
                       'paciente' : request.vars.paciente
                       }), _class = 'btn btn-primary'
                       )
        else:
            dosificando = ''        
        tabla.append(TR(
        TD(A(m.nombre, _href = URL(f='nuevo',args=m.id), _class='btn btn-mini')),
        TD(", ".join(m.para)),
        TD(m.cantidad, m.metrica,'/kg'),
        TD(dosificando)
        ))
        
        
    tabla = CAT(A('Agregar Medicamento', _href = URL(f='nuevo'), _class='btn btn-success'),tabla)
    return dict(tabla = tabla)

@auth.requires_login()
def nuevo():
    response.view = 'paciente/nuevo.html'
    form = SQLFORM(db.medicamento, request.args(0),
                   submit_button = 'Registar Medicamento')
    
    if form.process().accepted:
        if request.args:
            session.flash = 'Modificación de registro exitosa'
        else:
            session.flash = 'Nuevo registro agregado'
        redirect(URL(f='index'))
    
    
    return dict(form = form)

