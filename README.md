# VAULT SSH ROLES
These steps can be followed to setup multiple SSH Signing Engines, and the script in this repo can be used to programmatically create SSH Roles for your team members, with proper permissions assigned.  

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

## 2. Configure Signing Engines with a CA for signing client keys (can use an existing keypair or Vault can generate a keypair for you)


#### TEAM 1
```
vault write ssh-client-signer-team-1/config/ca generate_signing_key=true
```

#### TEAM 2
```
vault write ssh-client-signer-team-2/config/ca generate_signing_key=true
```

## 3. Create a Templated policy per Signing Engine (i.e. one per Team)

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

## 4. Create an Entity and Aliases for Each Team Member (docs [here](https://learn.hashicorp.com/vault/identity-access-management/iam-identity))

#### BOB

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

#### SALLY

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

## 5. Create a Role per User per Team
Run the create_roles.py script and pass in all team names and members, accordingly.

## 6. Users Authenticate to Vault (via preferred/configured method) and request a key signature:

#### BOB
```
vault write ssh-client-signer-team-1/sign/bob public_key=@$HOME/.ssh/id_rsa.pub
```

#### SALLY
```
vault write ssh-client-signer-team-2/sign/sally public_key=@$HOME/.ssh/id_rsa.pub
```
