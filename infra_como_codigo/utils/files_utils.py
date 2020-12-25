import os
import re

def _get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path).replace('utils/', '')

def get_cloudformation_templates(reverse=False):
    folder_templates = 'templates-cloudformation'
    cf_templates = []
    files = os.listdir(_get_abs_path(folder_templates))
    files.sort(reverse=reverse)

    for filename in files:
        path = _get_abs_path(folder_templates) + "/" + filename
        with open(path) as f:
            template_body = f.read()
        cf_template = {
            'stack_name': 'cfn-' + filename.split('.')[1],
            'template_body': template_body,
            'filename': filename
         }
        cf_templates.append(cf_template)

    return cf_templates