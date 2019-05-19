def create_roles(VAULT_ADDR, VAULT_TOKEN, team, team_members):
    import requests
    import json

    for team_member in team_members:
        vault_url = "%s/v1/ssh-client-signer-%s/roles/%s" % (VAULT_ADDR, team, team_member)
        headers = {"X-Vault-Token": "%s" % (VAULT_TOKEN)} 
        policy = {"allow_user_certificates":"true","allowed_users":"","default_extensions":[{"permit-pty":""}],"key_type":"ca","default_user":"","ttl":"30m0s"}
        policy["allowed_users"] = "%s" % (team_member)
        policy_json = json.dumps(policy)
        r = requests.post(url=vault_url, headers=headers, data=policy_json)

# To call the above, you just need to pass the required values
# create_roles("http://example-vault-addr:8200", "my-vault-token", "team-1", ["bob", "sally", "john", "jane"])



