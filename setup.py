from scripts.addbts import addbts
from scripts.resetdb import resetdb

with open('.env', 'w') as f:
    f.write(f'FB_USER="{input('Input your Facebook email: \n')}" \nFB_PASS="{input('Input your Facebook password: \n')}"')


resetdb()
addbts()