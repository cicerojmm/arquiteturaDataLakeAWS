import boto3
import logging
from botocore.exceptions import ClientError
from utils.files_utils import get_cloudformation_templates

logging.getLogger().setLevel(logging.INFO)
cloudformation_client = boto3.client('cloudformation')


def create_stack(stack_name, template_body, **kwargs):
    cloudformation_client.create_stack(
        StackName=stack_name,
        TemplateBody=template_body,
        Capabilities=['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM'],
        TimeoutInMinutes=30,
        OnFailure='ROLLBACK'
    )

    cloudformation_client.get_waiter('stack_create_complete').wait(
        StackName=stack_name,
        WaiterConfig={'Delay': 5, 'MaxAttempts': 600}
    )

    cloudformation_client.get_waiter('stack_exists').wait(StackName=stack_name)
    logging.info(f'CREATE COMPLETE')


def update_stack(stack_name, template_body, **kwargs):
    try:
        cloudformation_client.update_stack(
            StackName=stack_name,
            Capabilities=['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM'],
            TemplateBody=template_body
        )

    except ClientError as e:
        if 'No updates are to be performed' in str(e):
            logging.info(f'SKIPPING UPDATE: No updates to be performed at stack {stack_name}')
            return e

    cloudformation_client.get_waiter('stack_update_complete').wait(
        StackName=stack_name,
        WaiterConfig={'Delay': 5, 'MaxAttempts': 600}
    )

    cloudformation_client.get_waiter('stack_exists').wait(StackName=stack_name)
    logging.info(f'UPDATE COMPLETE')


def get_existing_stacks():
    response = cloudformation_client.list_stacks(
        StackStatusFilter=['CREATE_COMPLETE', 'UPDATE_COMPLETE', 'UPDATE_ROLLBACK_COMPLETE']
    )

    return [stack['StackName'] for stack in response['StackSummaries']]

def create_or_update_stack():
    templates = get_cloudformation_templates()
    existing_stacks = get_existing_stacks()

    for template in templates:
        stack_name = template['stack_name']
        template_body = template['template_body']
        
        if stack_name in existing_stacks:
            logging.info(f'UPDATING STACK {stack_name}')
            update_stack(stack_name, template_body)
        else:
            logging.info(f'CREATING STACK {stack_name}')
            create_stack(stack_name, template_body)


if __name__ == '__main__':
    create_or_update_stack()