def prescription_img_uploader(instance, filename):
    return f'{instance.patient.user.username}/{instance.patient.name}/visits/{instance.visit_date}/{filename}'


def document_img_uploader(instance, filename):
    return f'{instance.patient.user.username}/{instance.patient.name}/{instance.doc_type}/{filename}'
