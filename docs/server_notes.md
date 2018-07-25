## Install cloudstor (docker plugin to support persistent volumes)

cf. https://github.com/docker/for-aws/issues/85#issuecomment-342588884

```bash
docker plugin install --alias cloudstor:aws --grant-all-permissions docker4x/cloudstor:18.03.1-ce-aws1 CLOUD_PLATFORM=AWS DEBUG=1 AWS_REGION=us-west-2 EFS_SUPPORTED=0 AWS_STACK_ID=nostack
```