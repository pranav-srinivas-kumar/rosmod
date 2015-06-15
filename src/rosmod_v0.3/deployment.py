#!/usr/bin/python
import os,sys

from fabric.api import *
from fabric.api import task, run

from collections import OrderedDict

import multiprocessing

env.use_ssh_config = False

local_ips = ["localhost","127.0.0.1"]

def InitDeployment(self):
    self.deployed = False
    self.deploying = False
    self.runningDeployment = None
    self.runningDeploymentCanvas = None
    self.runningNodes = 0
    self.hostDict = None
    self.updatedHostDict = False

class deployed_node():
    def __init__(self,executable,libs,config,name,deploymentDir,userName,keyFile,cmdArgs='',pids=[]):
        self.name = name
        self.executable = executable
        self.libs = libs
        self.config = config
        self.deploymentDir = deploymentDir
        self.userName = userName
        self.keyFile = keyFile
        self.cmdArgs = cmdArgs
        self.pids = pids

class deployed_host():
    def __init__(self,name,userName,ipAddress,keyFile,deploymentDir,nodes=[],envVars=OrderedDict()):
        self.name = name
        self.userName = userName
        self.ipAddress = ipAddress
        self.deploymentDir = deploymentDir
        self.keyFile = keyFile
        self.nodes = nodes
        self.envVars = envVars

def getStatusFromPS(psString, name):
    pass

def getPIDsFromPS(psString, name):
    pids = []
    psString = psString.split('\n')
    psList = []
    for e in psString:
        if name in e and "grep" not in e and "dtach" not in e:
            psList.append(e)
    for e in psList:
        e.strip('\t')
        e.strip('\n')
        e.strip('\r')
    if psList == []:
        print "No running process for {}".format(name)
    else:
        for ps in psList:
            tmp = ps.split(' ')
            i = 1
            while '' == tmp[i] or ' ' == tmp[i]:
                i+=1
            pids.append(tmp[i])
            print "process {} has PID {}".format(name,pids[-1])
    return pids

@parallel
def parallelDeploy(hostDict,updateQ=None):
    host = hostDict[env.host_string]
    envVarStr = ""
    for key,value in host.envVars:
        envVarStr += "export {}={}; ".format(key,value)
    for node in host.nodes:
        executableString = node.executable
        if host.ipAddress not in local_ips:
            envVarStr = envVarStr.replace(';','')
            envVarStr += "export LD_LIBRARY_PATH={}:$LD_LIBRARY_PATH".format(node.deploymentDir)
            with prefix(envVarStr):
                env.key_filename = host.keyFile
                env.host_string = "{}@{}".format(host.userName,host.ipAddress)
                run('dtach -n `mktemp -u /tmp/dtach.XXXX` {} {}'.format(executableString,node.cmdArgs))
                pgrep = run('ps aux | grep {}'.format(executableString))
        else:
            local('{} dtach -n `mktemp -u /tmp/dtach.XXXX` {} {}'.format(envVarStr,executableString,node.cmdArgs),capture=True)
            pgrep = local('ps aux | grep {}'.format(executableString),capture=True)
        pids = getPIDsFromPS(pgrep,node.name)
        node.pids = pids
        if updateQ != None:
            updateQ.put(["Deployed {}".format(node.name),1])
    return host

@parallel
def parallelCopy(hostDict, exec_folder_path, deployment_folder_path, updateQ=None):
    host = hostDict[env.host_string]
    copyList = []
    copyList.append( 
        [os.path.join(exec_folder_path, "node/node_main"), host.deploymentDir] 
    )
    for node in host.nodes:
        copyList.append( 
            [os.path.join(deployment_folder_path + "/xml/" + host.name, node.config), node.deploymentDir]
        )
        for lib in node.libs:
            copyList.append(
                [os.path.join(exec_folder_path, lib), node.deploymentDir]
            )
        if node.deploymentDir != host.deploymentDir:
            copyList.append( [os.path.join(exec_folder_path, "node/node_main"), node.deploymentDir] )
    if host.ipAddress not in local_ips:
        env.key_filename = host.keyFile
        env.host_string = "{}@{}".format(host.userName,host.ipAddress)
        for source,dest in copyList:
            put(source,dest)
    else:
        for source,dest in copyList:
            local('cp {} {}'.format(source, dest),capture=True)
    if updateQ != None:
        updateQ.put(["Copied files to {}".format(env.host_string),1])

@parallel
def parallelCommand(hostDict, command, updateQ):
    host = hostDict[env.host_string]
    output = ""
    if host.ipAddress not in local_ips:
        env.key_filename = host.keyFile
        env.host_string = "{}@{}".format(host.userName,host.ipAddress)
        output=run(command)
    else:
        output=local(command,capture=True)
    updateQ.put(["Ran {} on host {} with output:\n{}".format(command,env.host_string,output),1])

@parallel
def parallelStop(hostDict,updateQ=None):
    host = hostDict[env.host_string]
    if host.ipAddress not in local_ips:
        env.key_filename = host.keyFile
        env.host_string = "{}@{}".format(host.userName,host.ipAddress)
        for node in host.nodes:
            if node.pids != [] and len(node.pids) > 0:
                for pid in node.pids:
                    try:
                        run('kill -9 {}'.format(pid))
                    except SystemExit:
                        pass
            updateQ.put(["Killed {}".format(node.name),1])
            node.pids = []
    else:
        for node in host.nodes:
            if node.pids != [] and len(node.pids) > 0:
                for pid in node.pids:
                    try:
                        local('kill -9 {}'.format(pid),capture=True)
                    except SystemExit:
                        pass
            if updateQ != None:
                updateQ.put(["Killed {}".format(node.name),1])
            node.pids = []
    return host

def startMaster(self,e):
    host = self.hostDict[self.rosCoreHost.properties['name']]
    if host.ipAddress not in local_ips:
        env.key_filename = host.keyFile
        env.host_string = "{}@{}".format(host.userName,host.ipAddress)
        run('source /opt/ros/indigo/setup.bash && dtach -n `mktemp -u /tmp/dtach.XXXX` roscore')
    else:
        local('dtach -n `mktemp -u /tmp/dtach.XXXX` roscore')

def stopMaster(self,e):
    host = self.hostDict[self.rosCoreHost.properties['name']]
    if host.ipAddress not in local_ips:
        env.key_filename = host.keyFile
        env.host_string = "{}@{}".format(host.userName,host.ipAddress)
        run('pkill roscore')
    else:
        local('pkill roscore')

def startNode(self,e):
    node = self.activeObject
    if self.deployed == True and node in self.runningDeployment.children and\
       self.hostDict != None and node.properties['hardware_reference'].properties['name'] in self.hostDict.keys():
        host = self.hostDict[node.properties['hardware_reference'].properties['name']]
        nodeprops = [x for x in host.nodes if x.name == node.properties['name']][0]
        if nodeprops.pids != []:
            print >> sys.stderr, "ERROR: cannot start node which is already running."
            return
        envVarStr = ""
        for key,value in host.envVars:
            envVarStr += "export {}={}; ".format(key,value)
        executableString = nodeprops.executable
        if host.ipAddress not in local_ips:
            envVarStr = envVarStr.replace(';','')
            with prefix(envVarStr):
                env.key_filename = host.keyFile
                env.host_string = "{}@{}".format(host.userName,host.ipAddress)
                run('dtach -n `mktemp -u /tmp/dtach.XXXX` {} {}'.format(executableString,nodeprops.cmdArgs))
                pgrep = run('ps aux | grep {}'.format(executableString))
        else:
            local('{} dtach -n `mktemp -u /tmp/dtach.XXXX` {} {}'.format(envVarStr,executableString,nodeprops.cmdArgs),capture=True)
            pgrep = local('ps aux | grep {}'.format(executableString),capture=True)
        pids = getPIDsFromPS(pgrep,nodeprops.name)
        nodeprops.pids = pids
    else:
        print >> sys.stderr, "ERROR: cannot start node which is not part of current deployment."

def stopNode(self,e):
    node = self.activeObject
    if self.deployed == True and node in self.runningDeployment.children and self.hostDict != None and \
       node.properties['hardware_reference'].properties['name'] in self.hostDict.keys():
        host = self.hostDict[node.properties['hardware_reference'].properties['name']]
        nodeprops = [x for x in host.nodes if x.name == node.properties['name']][0]
        if host.ipAddress not in local_ips:
            env.key_filename = host.keyFile
            env.host_string = "{}@{}".format(host.userName,host.ipAddress)
            for pid in nodeprops.pids:
                run('kill -9 {}'.format(pid))
        else:
            for pid in nodeprops.pids:
                local('kill -9 {}'.format(pid),capture=True)
            nodeprops.pids = []
    else:
        print >> sys.stderr, "ERROR: you must be running a deployment and node must be part of current deployment!"

@parallel
def parallelMonitor(hostDict,updateQ):
    host = hostDict[env.host_string]
    if host.ipAddress not in local_ips:
        env.key_filename = host.keyFile
        env.host_string = "{}@{}".format(host.userName,host.ipAddress)
        for node in host.nodes:
            if node.pids != [] and len(node.pids) > 0:
                for pid in node.pids:
                    try:
                        status = run('ps --no-headers -p {}'.format(pid))
                        updateQ.put(["{} UP".format(node.name),1])
                    except SystemExit:
                        updateQ.put(["{} DOWN".format(node.name),1])
                        node.pids = []
            else:
                updateQ.put(["{} DOWN".format(node.name),1])
    else:
        for node in host.nodes:
            if node.pids != [] and len(node.pids) > 0:
                for pid in node.pids:
                    try:
                        status = local('ps --no-headers -p {}'.format(pid),capture=True)
                        updateQ.put(["{} UP".format(node.name),1])
                    except SystemExit:
                        updateQ.put(["{} DOWN".format(node.name),1])
                        node.pids = []
            else:
                updateQ.put(["{} DOWN".format(node.name),1])
    return host

def deployTest(self, progress_q):
    self.hostDict = execute(parallelDeploy,self.hostDict,progress_q)

def stopTest(self, progress_q):
    self.hostDict = execute(parallelStop,self.hostDict,progress_q)
    
def monitorTest(self, progress_q):
    self.hostDict = execute(parallelMonitor,self.hostDict,progress_q)

def copyTest(self, exec_folder_path, xml_folder_path, progress_q):
    execute(parallelCopy, self.hostDict, exec_folder_path, xml_folder_path, progress_q)

def runCommandTest(self, command, progress_q):
    execute(parallelCommand, self.hostDict, command, progress_q)

class testClass:
    def __init__(self):
        pass

def main(ipaddr):
    hostDict = {}
    node = deployed_node(
        name = 'three_component_node',
        executable = '/home/jeb/node_main',
        libs = ['libComponent_1.so','libComponent_2.so','libComponent_3.so'],
        config = 'three_component_node.xml',
        deploymentDir = '/home/jeb/',
        userName = 'jeb',
        keyFile = '/home/jeb/.ssh/id_rsa_rosmod',
        cmdArgs = ' -config /home/jeb/three_component_node.xml -nodename three_component_node -hostname Laptop'
    )
    hostDict['Laptop'] = deployed_host(
        name = 'Laptop',
        userName = 'jeb',
        deploymentDir = '/home/jeb/',
        ipAddress = ipaddr,
        keyFile = '/home/jeb/.ssh/id_rsa_rosmod',
        nodes = [node],
        envVars = []
    )
    hostDict['Laptop'].envVars.append(
        ["LD_LIBRARY_PATH","/home/jeb/:$LD_LIBRARY_PATH"]
    )
    hostDict['Laptop'].envVars.append(
        ['ROS_MASTER_URI','http://{}:11311/'.format(ipaddr)])
    hostDict['Laptop'].envVars.append(
        ['ROS_IP',ipaddr]
    )

    obj = testClass()
    obj.hostDict = hostDict

    env.hosts.append('Laptop')

    copyTest(
        obj,
        '/home/jeb/Repositories/rosmod/code/samples/three_component_example/01-Software/workspace/devel/lib/',
        '/home/jeb/Repositories/rosmod/code/samples/three_component_example/03-Deployment/deployment',
        multiprocessing.Queue()
    )

    hostDict = deployTest(
        obj,
        'testTopic',
        multiprocessing.Queue()
    )

    hostDict = stopTest(
        obj,
        'testTopic',
        multiprocessing.Queue()
    )

@task
def local_test():
    main('127.0.0.1')

@task
def remote_test():
    main('192.168.1.4')

if __name__ == "__main__":
    main('127.0.0.1')
