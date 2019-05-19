## VAULT SSH ROLES
This script can be used to programmatically create SSH Roles for your team members, with proper policy assigments.  

This script could be used in conjunction with a templated policy for ease of setup:

path "ssh-client-signer-team-1/sign/{{identity.entity.name}}" {
    capabilities = ["create","update"]
}
EOF