## VAULT SSH ROLES
This script can be used to programmatically create SSH Roles for your team members, with proper permissions assigned.  

# SETUP

## 1. Create separate signing engines (One per team)

### TEAM 1
vault secrets enable -path=ssh-client-signer-team-1 ssh

### TEAM 2
vault secrets enable -path=ssh-client-signer-team-2 ssh

This script could be used in conjunction with a templated policy for ease of setup.  For example:

```
path "ssh-client-signer-team-1/sign/{{identity.entity.name}}" {
    capabilities = ["create","update"]
}
EOF
```
