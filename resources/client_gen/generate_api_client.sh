#!/usr/bin/env bash

# Instructions
# You will need Java installed on the local machine

# A new client is generated from the Swagger Def, and then manually merged into
# NiPyApi so that changes may be assessed, tests written, and trouble avoided

# Params
echo Exporting Params
export wv_client_name=${wv_client_name:-registry}

export wv_codegen_filename=${wv_codegen_filename:-swagger-codegen-cli-2.4.41.jar}
export wv_tmp_dir=${wv_tmp_dir:-${HOME}/Projects/tmp}
export wv_client_dir=${wv_tmp_dir}/${wv_client_name}
export wv_mustache_dir=./swagger_templates
export wv_api_def_dir=./api_defs

export wv_codegen_url=https://repo1.maven.org/maven2/io/swagger/swagger-codegen-cli/2.4.41/${wv_codegen_filename}
export wv_swagger_def=$(ls ${wv_api_def_dir} | grep ${wv_client_name} | sort -V | tail -1)

echo Prepping Workspace
mkdir -p ${wv_tmp_dir}
echo "{ \"packageName\": \"${wv_client_name}\" }" > ${wv_tmp_dir}/${wv_client_name}.conf.json

echo Downloading ${wv_codegen_filename}
wget -N ${wv_codegen_url} -P ${wv_tmp_dir}

java -jar ${wv_tmp_dir}/${wv_codegen_filename} generate \
    --lang python \
    --config ${wv_tmp_dir}/${wv_client_name}.conf.json \
    --api-package apis \
    --model-package models \
    --template-dir ${wv_mustache_dir} \
    --input-spec ${wv_api_def_dir}/${wv_swagger_def} \
    --output ${wv_client_dir}
