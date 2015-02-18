
export GIT_EMAIL='openstack-dev@purestorage.com'
export GIT_NAME='Pure Storage Cinder CI'

#Openstack
export UPSTREAM_GERRIT_SSH_HOST_KEY="review.openstack.org,23.253.232.87,2001:4800:7815:104:3bc3:d7f6:ff03:bf5d b8:3c:72:82:d5:9e:59:43:54:11:ef:93:40:1f:6d:a5"
export UPSTREAM_GERRIT_USER=purestorage-cinder-ci
export UPSTREAM_GERRIT_SSH_KEY_PATH=gerrit_key
export PUBLISH_HOST=${LOG_FILE_SERVER}

#Used by Nodepool
export MYSQL_ROOT_PASSWORD=changeme
export MYSQL_PASSWORD=changeme
export PROVIDER_USERNAME=jenkins
export PROVIDER_PASSWORD=jenkins
export PROVIDER_IMAGE_NAME="Ubuntu 14.04 Server"
export PROVIDER_IMAGE_SETUP_SCRIPT_NAME="prepare_node_pure.sh"
export JENKINS_API_USER=jenkins
#API Key is used if you secure your jenkins with a password
#export JENKINS_API_KEY=<hex_id>
#This credentials id is the default.  Change if needed.
export JENKINS_CREDENTIALS_ID=f4f07d8e-2634-4d01-bcf6-7b8be996e062

#TODO: automate whitespace removal
export JENKINS_SSH_PUBLIC_KEY_NO_WHITESPACE="insert jenkins_key.pub text here"
export JENKINS_SSH_KEY_PATH=jenkins_key
