#!/bin/bash

# Deploy multi-tier, multi-stage Infrastructure as Code
#
# In this script you choose which config json file you want to use and just
# copy that file to ``devops/config-raw.json`` then execute ``bash deploy.sh``
#
# There are several solutions to securely maintain the config file
#
# 1. put it on a s3 bucket with encryption ON, and just do
#       aws cp s3://xxx/config-raw-dev.json config-raw.json
# 2. put it on SecretManager, and use a IAM role to decrypt it with KMS,
#       usually it is the case you use a EC2 instance to deploy
# 3. maintain it locally on a trusted devops engineer's laptop
# 4. put config file on a separate GitHub repo, and use GitHub Machine User
#       to check out the repo in your CICD system.
# NOTE: don't ever check-in config file to source control!

dir_here="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
deploy_script="${dir_here}/deploy.sh"
dir_project_root=$(dirname "${dir_here}")

sudo bash "$dir_project_root/bin/lbd/build-lbd-source-code.sh"
bash "$dir_project_root/bin/lbd/upload-lbd-source.sh"

bash $deploy_script "${dir_here}/config-rdso-lab-prod.json"
