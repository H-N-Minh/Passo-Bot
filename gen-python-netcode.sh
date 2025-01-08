#!/bin/bash
##################################
# Author: Martin Wistauder
# Date: 05.10.2021
# Version: 1.0
##################################
set -e

usage='Usage: ./gen-python-netcode.sh {protobuf source dir} {output dir}
Example usage: ./gen-python-netcode.sh ./protobuf ./netcode'

# check params
[ -z $1 ] && echo -e "Error: First parameter missing.\n$usage" && exit 1 || proto_dir="$1"
[ -z $2 ] && echo -e "Error: Second parameter missing.\n$usage" && exit 1 || output_dir="$2"

# vars
proto_dir="$1"
output_dir="$2"

# generate the python netcode
mkdir -p "$output_dir"
python3 -m grpc_tools.protoc -I"$proto_dir" --python_out="$output_dir" --grpc_python_out="$output_dir" $(find "$proto_dir" -name "*.proto" -printf "%P ")
