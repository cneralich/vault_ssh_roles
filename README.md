# VAULT SSH ROLES
This script can be used to programmatically create SSH Roles for your team members, with proper permissions assigned.  

## SETUP STEPS

## 1. Create separate signing engines (One per team)

### TEAM 1
vault secrets enable -path=ssh-client-signer-team-1 ssh

### TEAM 2
vault secrets enable -path=ssh-client-signer-team-2 ssh

## 2. Create a Role per User per Team
Run the create_roles.py script and pass in all team names and members, accordingly.

## 3. Create a Templated policy per Signing Engine (i.e. one per Team)

```
path "ssh-client-signer-team-1/sign/{{identity.entity.name}}" {
    capabilities = ["create","update"]
}
EOF
```

```
path "ssh-client-signer-team-2/sign/{{identity.entity.name}}" {
    capabilities = ["create","update"]
}
EOF
```

### 4. Users Authenticate to Vault (via preferred/configured method) and request a key signature:

#### SALLY
vault write ssh-client-signer-team-1/sign/sally public_key=@$HOME/.ssh/id_rsa.pub

#### BOB
vault write ssh-client-signer-team-2/sign/bob public_key=@$HOME/.ssh/id_rsa.pub
