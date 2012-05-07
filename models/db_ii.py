# coding: utf8

unidades_de_medida = ["unid.","ml"]

db.define_table("medicamento",
    Field("nombre",requires=IS_UPPER()),
    Field("para", "list:string"),
    Field("metrica", requires=IS_IN_SET(unidades_de_medida)),
    Field("cantidad","double", comment = "cantidad según kg de masa"),    
    Field("info_extra", "text"),
    format = "%(nombre)s"
    )

db.define_table("paciente",
    Field("nombre"),
    Field("apellido_p"),
    Field("apellido_m"),
    Field("peso","double", comment = "en Kilogramos"),
    Field("fecha_nacimiento","date"),
    Field("nombre_completo", compute=lambda p: '%s %s %s' \
    % (p['nombre'].capitalize(), p['apellido_p'].capitalize(), p['apellido_m'].capitalize())),
    format = "%(nombre_completo)s",
    )

db.define_table("dosis",
    Field("paciente", "reference paciente"),
    Field("medicamento", "reference medicamento"),
    Field("metrica", requires=IS_IN_SET(unidades_de_medida)),
    Field("cantidad","double"),
    Field("horas", "integer", label = "Cada cuantas horas"),
    Field("dias", "integer", default = 1, label = "Por cuantos días"),
    Field("detalle", "text"),
    Field("comienza", "datetime", default = request.now.now(),
          update = request.now.now()),
    format = "%(paciente)s - %(medicamento)s"
    )
