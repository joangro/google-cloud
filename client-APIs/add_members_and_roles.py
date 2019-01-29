from google.oauth2 import service_account
import googleapiclient.discovery
 
 
credentials = service_account.Credentials.from_service_account_file(
    filename='PATH/TO/KEY.json',
    scopes=['https://www.googleapis.com/auth/cloud-platform'])
service = googleapiclient.discovery.build(
    'cloudresourcemanager', 'v1', credentials=credentials)
 
 
 
def modify_policy_add_member(policy, role, member):
    binding = next(b for b in policy['bindings'] if b['role'] == role)
    binding['members'].append(member)
    print(binding)
    return policy
 
def create_role_add_member(policy, role, member):
    """Adds a new member to a role binding."""
    binding = {
                'role': role,
                'members': [member]
            }
    print(binding)
    policy['bindings'].append(binding)
    return policy
 
if __name__ == "__main__":
    project_id="YOUR_PROJECT_ID"
    policy=service.projects().getIamPolicy(
                resource=project_id,
                body={},
            ).execute()
    role="ROLE_TO_GRANT"
    member="user:MEMBER_TO_ADD"
    roles = [b['role'] for b in policy['bindings']]
    if role  in roles:
        new_policy = modify_policy_add_member(policy, role, member)
    else:
        new_policy = create_role_add_member(policy, role, member)
    print(new_policy)
    policy = service.projects().setIamPolicy(
            resource=project_id,
            body={
                'policy': new_policy,
    }).execute()
