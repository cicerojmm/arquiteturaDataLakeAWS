import pytest
import boto3
import logging
from utils.files_utils import get_cloudformation_templates

logging.basicConfig(level=logging.INFO)
cloudformation_client = boto3.client('cloudformation')

class TestValidacaoTemplates():
    
    def test_validacao_templates(self):
        cf_templates = get_cloudformation_templates()
        for cf_template in cf_templates:
            logging.info('Validating CF template {}'.format(cf_template['filename']))
            cloudformation_client.validate_template(
                TemplateBody=cf_template['template_body']
            )