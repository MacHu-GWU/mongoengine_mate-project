#!/bin/bash
# -*- coding: utf-8 -*-

dir_here="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
dir_bin="$(dirname "${dir_here}")"
dir_project_root=$(dirname "${dir_bin}")

source ${dir_bin}/py/python-env.sh

# in circleci, it use the environment variable AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
# if string is null, it is not
if [ "${is_circleci}" = "Y" ]
then
    profile_arg=""
    sls_aws_profile_arg=""
else
    profile_arg="--profile ${aws_profile_for_deploy}"
    sls_aws_profile_arg="--aws-profile "${aws_profile_for_deploy}""
fi

if [ "${is_ec2}" = "Y" ]
then
    profile_arg=""
    sls_aws_profile_arg=""
fi
