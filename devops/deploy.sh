#!/bin/bash

# This script deploy cloudformation take the first parameter as path of config file
# and copy that file to ``${dir_devops}/config-raw.json``, then deploy it with
# master cloudformation template

#set -e

# The master cloudformation template
raw_deploy_config_file="$1"
if ! [ -e $raw_deploy_config_file ]; then
    echo "${raw_deploy_config_file} not found"
    exit 1
fi

dry_run_arg="$2"

# Resolve path
dir_here="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
dir_devops="$dir_here"
dir_project_root=$(dirname "${dir_devops}")
dir_bin="${dir_project_root}/bin"

source "${dir_project_root}/bin/lbd/lambda-env.sh"
echo $profile_arg

## initialize
path_deploy_config_file="${dir_devops}/config-raw.json"
echo "copy deploy config file from ${raw_deploy_config_file} to ${path_deploy_config_file} ..."
rm_if_exists $path_deploy_config_file
cp $raw_deploy_config_file $path_deploy_config_file

path_generate_cf_script="${dir_devops}/generate_cf.py"
path_read_config_value_script="${dir_project_root}/config/read-config-value"
path_parameter_overrides_for_cloudformation_script="${dir_devops}/helper_get_cf_parameter_overrides.py"

# The python script generated master cloudformation template
master_template_file="${dir_devops}/99-master.json"

# The `aws cloudformation package` command packaged template file
path_packaged_cloudformation_json_file="${dir_devops}/packaged.json"

echo "generate cloudformation template and related config files, execute ${path_generate_cf_script} ..."
$bin_python ${path_generate_cf_script}

# related config from config.json file
cloudformation_parameters_config_file="${dir_devops}/config-final-for-cloudformation.json"

if ! [ -e $cloudformation_parameters_config_file ]; then
    echo "${cloudformation_parameters_config_file} not found"
    exit 1
fi

if [ -e "$path_packaged_cloudformation_json_file" ]; then
    rm $path_packaged_cloudformation_json_file
fi

get_config_value() {
    local config_key=$1
    python $path_read_config_value_script $cloudformation_parameters_config_file $config_key
}

# The AWS Profile you used to deploy the cloudformation
aws_profile="$(get_config_value "AwsProfile")"
aws_default_region="$(get_config_value "AwsRegion")"
stack_name="$(get_config_value "StackName")"
project_name=$(get_config_value "ProjectName")
project_name_slug=$(get_config_value "ProjectNameSlug")
stage=$(get_config_value "Stage")
env_name=$(get_config_value "EnvironmentName")
parameter_overrides="$(python $path_parameter_overrides_for_cloudformation_script $master_template_file $cloudformation_parameters_config_file)"

# The s3 bucket to store cloudformation template
cf_bucket=$(get_config_value "S3BucketForCf")

# in circleci, it use the environment variable AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
# for aws cli
if [ -z "$CIRCLECI" ]
then
    profile_arg="--profile $aws_profile"
else
    profile_arg=""
    export AWS_DEFAULT_REGION="$aws_default_region"
fi


package() {
    echo "Packaging all cloudformation template, run \"aws cloudformation package\" command ..."
    aws cloudformation package \
        --template-file "${master_template_file}" \
        --s3-bucket $cf_bucket \
        --use-json \
        --s3-prefix "stack/${stack_name}" \
        --output-template-file $path_packaged_cloudformation_json_file \
        --force-upload \
        $profile_arg
}

deploy() {
    echo "Deploy stack ${stack_name} based on ${path_packaged_cloudformation_json_file}"
    echo "run \"aws cloudformation deploy\" command ..."
    if [ -n "$parameter_overrides" ]
    then
        parameter_overrides_arg="--parameter-overrides $parameter_overrides"
    else
        parameter_overrides_arg=""
    fi
    aws cloudformation deploy \
        --template-file $path_packaged_cloudformation_json_file \
        --s3-bucket $cf_bucket \
        --stack-name $stack_name \
        --tags Project="$project_name_slug" Stage="$stage" EnvironmentName="$env_name" \
        --capabilities CAPABILITY_NAMED_IAM \
        $parameter_overrides_arg \
        $profile_arg
}

package
# you can pass "dryrun" as the second argument to skip real deployment
if [ "$dry_run_arg" != "dryrun" ]; then
    deploy
fi
