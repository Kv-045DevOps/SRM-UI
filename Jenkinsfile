def label = "mypod-${UUID.randomUUID().toString()}"


podTemplate(label: label, annotations: [podAnnotation(key: "sidecar.istio.io/inject", value: "false")], containers: [
  containerTemplate(name: 'python-alpine', image: 'ghostgoose33/python-alp:v3', command: 'cat', ttyEnabled: true),
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
            defaultValue: '*', 
            description: 'TAG', 
            name: 'service')
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
            pathTocodeui = pwd()
            }
        }
        stage("Test image_regisrty_check"){
            container("python-alpine"){
                check_new = (sh (script: "python3 /images-registry-test.py ui-service ${imageTagUI}", returnStdout:true).trim())
                echo "${check_new}"
            }
        }
        
        stage ("Unit Tests"){
            sh 'echo "Here will be unit tests"'
        }
        stage("Test code using PyLint and version build"){
			container('python-alpine'){
				sh "python3 /pylint-test.py ${pathTocodeui}/app/app.py"
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
					sleep 20
					build(job: 'test_e2e', parameters: [[$class: 'StringParameterValue', name:"imageTagUI_", value: "${imageTagUI}"],
									   [$class: 'StringParameterValue', name:"imageTagDB_", value: "${params.imageTagDB_}"],
									   [$class: 'StringParameterValue', name:"imageTagGET_", value: "${params.imageTagGET_}"],
									   [$class: 'StringParameterValue', name:"service", value: "ui"]], wait: true)
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
