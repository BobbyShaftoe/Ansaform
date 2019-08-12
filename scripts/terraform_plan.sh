#!/usr/bin/env bash


usage () {
      echo
      echo "  USAGE: $`basename $0`  COMMAND [-hj] [-t path, -p path]"
      echo "    -t   Path to terraform.tfvars"
      echo "    -p   Path to write plan output"
      echo "    -j   Use json format"
      echo "    -h   Display this help"
      echo
}

[[ -z "$1" ]] && { usage; exit 1; }

while getopts "hjp:t:" opt; do
  case "${opt}" in
    h)
      usage
      shift "$((OPTIND -1))"
      exit 0
      ;;
    j)
      JSON_OPTION='-json'
      FILE_EXTENSION='.json'
      ;;
    p)
      OUTPUT_PLAN_PATH="$OPTARG"
      ;;
    t)
      TFVARS_PATH="$OPTARG"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      usage
      exit 1
      ;;
  esac
done


echo "terraform plan -var-file=${TFVARS_PATH} -out ${OUTPUT_PLAN_PATH}"

terraform plan "-var-file=${TFVARS_PATH}" "-out=${OUTPUT_PLAN_PATH}"


echo "terraform show ${JSON_OPTION} ${OUTPUT_PLAN_PATH}  \
 | python -m json.tool > show_${OUTPUT_PLAN_PATH}${FILE_EXTENSION}"

terraform show "${JSON_OPTION}" "${OUTPUT_PLAN_PATH}" \
 | python -m json.tool > "show_${OUTPUT_PLAN_PATH}${FILE_EXTENSION}"




