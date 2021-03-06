#!/bin/bash
# -*- coding: utf-8 -*-
#
# Deploy html doc to s3://<s3-bucket-name>/<dir-prefix>/<package-name>/<version>


dir_here="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
dir_bin="$(dirname "${dir_here}")"
dir_project_root=$(dirname "${dir_bin}")

source ${dir_bin}/py/python-env.sh

print_colored_line $color_cyan "[DOING] deploy ${path_sphinx_doc_build_html} to ${s3_uri_doc_versioned} ..."
deploy_doc_to_s3 ${path_sphinx_doc_build_html} ${s3_uri_doc_versioned}
