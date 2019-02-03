def label = "mypod-${UUID.randomUUID().toString()}"


podTemplate(label: label, containers: [
  containerTemplate(name: 'python-alpine', image: 'ghostgoose33/python-alp:v1', command: 'cat', ttyEnabled: true),
  containerTemplate(name: 'docker', image: 'ghostgoose33/docker-in:v1', command: 'cat', ttyEnabled: true)
],
volumes: [
  hostPathVolume(mountPath: '/var/run/docker.sock', hostPath: '/var/run/docker.sock')
], serviceAccount: "jenkins") 
{

def dockerRegistry = "100.71.71.71:5000"
def Creds = "git_cred"
def projName = "ui-service"
def imageVersion = "latest"
def imageName = "100.71.71.71:5000/ui-service:${imageVersion}"
def imageN = '100.71.71.71:5000/ui-service:'

properties([
    parameters([
        stringParam(
            defaultValue: "***", 
            description: 'C', 
            name: 'imageTagGET'),
	stringParam(
            defaultValue: "***", 
            description: '', 
            name: 'imageTagUI'),
	stringParam(
            defaultValue: "***", 
            description: '', 
            name: 'imageTagDB'),
        stringParam(
            defaultValue: '***', 
            description: '', 
            name: 'namespace')
    ])
])


node(label)
{
    try{
        stage("Pre-Test"){
            dir('get'){
            git(branch: "test", url: 'https://github.com/Kv-045DevOps/SRM-UI.git', credentialsId: "${Creds}")
            imageTagUI = (sh (script: "git rev-parse --short HEAD", returnStdout: true))
            tmp = "1"
            //imageTagGET = sh(returnStdout: true, script: "git tag -l --points-at HEAD").trim()
            pathTocodeui = pwd()
            }
        }
        stage("Test image_regisrty_check"){
            container("python-alpine"){
                check_new = (sh (script: "python3 ${pathTocodeui}/images-registry-test.py ui-service ${imageTagUI}", returnStdout:true).trim())
                echo "${check_new}"
            }
        }
        
        stage ("Unit Tests"){
            sh 'echo "Here will be unit tests"'
        }
        stage("Test code using PyLint and version build"){
			container('python-alpine'){
				pathTocode = pwd()
				sh "python3 ${pathTocodeui}/pylint-test.py ${pathTocodeui}/app/app.py"
			}
        }
        stage("Build docker image"){
			container('docker'){
				pathdocker = pwd()
                                if ("${tmp}" == "${check_new}"){
                                	sh "docker build ${pathTocodeui} -t ${imageN}${imageTagUI}"
					sh "docker images"
                                	sh "cat /etc/docker/daemon.json"
					sh "docker push ${imageN}${imageTagUI}"
					build(job: 'test_e2e', parameters: [[$class: 'StringParameterValue', name:"imageTagUI", value: "${imageTagUI}"]], wait: true)
        			} else {
            				echo "NO"
        			}
				
			}
        }
    }
    catch(err){
        currentBuild.result = 'Failure'
    }
}
}
