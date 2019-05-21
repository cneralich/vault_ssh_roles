# VAULT SSH ROLES
This script can be used to programmatically create SSH Roles for your team members, with proper permissions assigned.  

## SETUP STEPS

## 1. Create separate signing engines (One per team)

#### TEAM 1
```
vault secrets enable -path=ssh-client-signer-team-1 ssh
```

#### TEAM 2
```
vault secrets enable -path=ssh-client-signer-team-2 ssh
```

## 2. Create a Templated policy per Signing Engine (i.e. one per Team)

#### team-1-ssh.hcl
```
vault policy write team-1-ssh -<<EOF
path "ssh-client-signer-team-1/sign/{{identity.entity.name}}" {
    capabilities = ["create","update"]
}
EOF
```

#### team-2-ssh.hcl
```
vault policy write team-2-ssh -<<EOF
path "ssh-client-signer-team-2/sign/{{identity.entity.name}}" {
    capabilities = ["create","update"]
}
EOF
```

## 3. Create an Entity and Aliases for Each Team Member (docs [here](https://learn.hashicorp.com/vault/identity-access-management/iam-identity))

#### Bob

##### Entity
```
vault write identity/entity name="bob" policies="team-1-ssh" \
        metadata=organization="ACME Inc." \
        metadata=team="Team-1"
 ```
   
##### Alias (One per Auth Method)
```
vault write identity/entity-alias name="bob-okta" \
        canonical_id=<entity_id> \
        mount_accessor=<userpass_accessor>
```

#### Sally

##### Entity
```
vault write identity/entity name="sally" policies="team-2-ssh" \
        metadata=organization="ACME Inc." \
        metadata=team="Team-2"
 ```
   
##### Alias (One per Auth Method)
```
vault write identity/entity-alias name="sally-okta" \
        canonical_id=<entity_id> \
        mount_accessor=<userpass_accessor>
```

## 4. Create a Role per User per Team
Run the create_roles.py script and pass in all team names and members, accordingly.

## 5. Users Authenticate to Vault (via preferred/configured method) and request a key signature:

#### BOB
```
vault write ssh-client-signer-team-1/sign/bob public_key=@$HOME/.ssh/id_rsa.pub
```

#### SALLY
```
vault write ssh-client-signer-team-2/sign/sally public_key=@$HOME/.ssh/id_rsa.pub
```
