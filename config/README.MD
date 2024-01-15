# Project Configuration Directory

## Overview

This directory, `config/`, is used for storing configuration files related to our project. 
These files can include environment settings, configuration parameters for different development stages, 
and other necessary configurations that are crucial for project setup and execution.

## Purpose

- **Environment Specific Settings**: It holds various settings specific to each environment like development, testing, and production.
- **Security**: To ensure sensitive information (like API keys, credentials) is not accidentally committed, these files are typically ignored in the version control system using `.gitignore`.
- **Customization**: Allows easy customization and setup for new team members or when deploying to different environments.

## Structure

The `config` directory may include files like:

- `ssh_params.sh`: Script containing parameters for SSH configurations.
- `vm_params.sh`: Script with virtual machine configuration parameters.

**Note**: The actual files are ignored in the repository for security and flexibility reasons, and only sample or template config files are provided when necessary.

### Specific File Descriptions

- `ssh_params.sh`: This script sets environment variables used for SSH connections. It typically includes SSH host, port, and user information. This is crucial for automating deployments or managing remote connections in a secure manner.

- `vm_params.sh`: Contains environment variables and settings for virtual machine configurations. This is used to standardize and automate the setup of virtual machines, ensuring consistency across different environments.


**Note**: The actual files are ignored in the repository for security and flexibility reasons, and only sample or template config files are provided when necessary.
