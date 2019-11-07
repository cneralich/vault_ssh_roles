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

## 3. Add the public key to all target host's SSH configuration

#### TEAM 1
##### 1) From the Target Machine
```
curl -o /etc/ssh/trusted-user-ca-keys-team-1.pem <YOUR_VAULT_ADDR>/v1/ssh-client-signer-team-1/public_key
```
##### 2) Add TrustedUserCAKeys /etc/ssh/trusted-user-ca-keys-team-1.pem to /etc/ssh/sshd_config
```
TrustedUserCAKeys /etc/ssh/trusted-user-ca-keys-team-1.pem
```
##### 3) Restart SSH -> service ssh restart, service sshd restart

#### TEAM 2
##### 1) From the Target Machine
```
curl -o /etc/ssh/trusted-user-ca-keys-team-2.pem <YOUR_VAULT_ADDR>/v1/ssh-client-signer-team-2/public_key
```
##### 2) Add TrustedUserCAKeys /etc/ssh/trusted-user-ca-keys-team-2.pem to /etc/ssh/sshd_config
```
TrustedUserCAKeys /etc/ssh/trusted-user-ca-keys-team-2.pem
```
##### 3) Restart SSH -> service ssh restart, service sshd restart

## 4. Create a Templated policy per Signing Engine (i.e. one per Team)

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

## 5. Create an Entity and Aliases for Each Team Member (docs [here](https://learn.hashicorp.com/vault/identity-access-management/iam-identity))

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

## 6. Create a Role per User per Team
Run the create_roles.py script and pass in all team names and members, accordingly.

## 7. Users Authenticate to Vault (via preferred/configured method), request a key signature, and save signed key to disk:

#### BOB
```
vault write -field=signed_key ssh-client-signer-team-1/sign/bob public_key=@$HOME/.ssh/id_rsa.pub > signed-cert.pub
```

#### SALLY
```
vault write -field=signed_key ssh-client-signer-team-2/sign/sally public_key=@$HOME/.ssh/id_rsa.pub > signed-cert.pub
```

## 8. Users use signed keys to SSH into Target Machine

#### BOB
```
ssh -i signed-cert.pub -i ~/.ssh/id_rsa bob@example.com
```

#### SALLY
```
ssh -i signed-cert.pub -i ~/.ssh/id_rsa sally@example.com
```

