
# Welcome to your CDK Python project!

This is a blank project for CDK development with Python.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

# Setup AWS Network Landing Zone for CDK and Application deployments
This CDK stack create the environemnt for deployment to multiple accounts

refs:
- https://github.com/aws-samples/aws-cdk-pipelines-datalake-infrastructure
- https://aws.plainenglish.io/cdk-cross-account-pipelines-22e9cdc3c566 (part1)
- https://aws.plainenglish.io/cdk-cross-account-pipelines-part-2-dcb5517a0610 (part2)
- https://github.com/markilott/aws-cdk-pipelines-github
- https://rehanvdm.com/blog/4-methods-to-configure-multiple-environments-in-the-aws-cdk
- https://stackoverflow.com/questions/74854751/aws-cdk-multi-account-deploy-credentials-in-trusted-account
- https://guymorton.medium.com/cross-account-deployment-using-aws-codepipeline-and-cdk-40bca2f49de8

- *** https://kreuzwerker.de/en/post/effectively-using-cdk-pipelines-to-deploy-cdk-stacks-into-multiple-accounts
with https://www.codeconvert.ai/typescript-to-python-converter

- https://bitbucket.org/selcuk-yilmaz/multiacc-cicd-aws/src/main/
- https://nordcloud.com/tech-community/automating-cicd-pipelines/

## Prerequesites
### 0 - Update AWS CLI
refs: 
- https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html#:~:text=The%20command%20line%20installer%20is,team%20needs%20to%20pin%20versions

```
> which aws
> aws --version

# After running AWS CLI installer
> aws --version
```

### 1 - Update AWS CDK Version
Run outside project folder
```
> cdk --version
> chmod +x update_cdk.sh
> ./update_cdk.sh
> cdk --version
```
### 2 - Initialize CDK Project
1. Create New Project Directory
```
> mkdir cdk_aws_setup
> cd cdk_aws_setup
```
2. Initialize a CDK App (Python)
```
> cdk init app --language python
> cdk acknowledge 34892
```

### 3 - Setup Git to ignore file
.gitignore
```
*.swp
package-lock.json
__pycache__
.pytest_cache
.venv/
*.egg-info

# CDK asset staging directory
.cdk.staging
cdk.out/
```

### 4 - Switch to GitHub dev Branch
```
> git checkout -b dev
> git add.
> git commit -m "Initial Setup"
> git push --set-upstream origin dev
```

### 5 - Start Virtual Environment
```
# If running .venv, deactivate:
> conda deactivate
# Freeze Version
> pip freeze > requirements.txt
# Then run:
> source .venv/bin/activate
> pip install -r requirements.txt
```

### 6 - Makefile - Automates Common AWS CDK Tasks
Usage of Makefile:
```
make init
make synth
make deploy
```

### CDK Bootstrap for BUILD AWS Account
Using default profile:
```
> cdk bootstrap aws://005713840833/us-east-1
```

### CDK Bootstrap for DEV AWS Account
```
> cdk bootstrap aws://557194064282/us-east-2 --profile JP-DEV \
--cloudformation-execution-policies "arn:aws:iam::aws:policy/AdministratorAccess" \
--trust 005713840833 
```

### CDK Bootstrap for PROD AWS Account
```
> cdk bootstrap aws://152915603097/us-west-1 --profile devops-cdk \
--cloudformation-execution-policies "arn:aws:iam::aws:policy/AdministratorAccess" \
--trust 005713840833 
```

### GitHub Connection with AWS CodePipeline
```
> aws codeconnections create-connection --provider-type GitHub --connection-name MyGitHubConnection
```
