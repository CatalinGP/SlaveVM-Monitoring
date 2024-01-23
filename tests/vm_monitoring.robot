*** Settings ***
Library           SSHLibrary
Library           config_accessor.py

*** Test Cases ***
Monitor VM Status
    ${host}=        Get Config Value    host
    ${user}=        Get Config Value    user
    ${key}=         Get Config Value    key
    Open Connection    ${host}    username=${user}    private_key_file=${key}
    Start Command      bash /path/to/status_script.sh
    ${output}=         Read Command Output
    Log                ${output}
    [Teardown]         Close All Connections
