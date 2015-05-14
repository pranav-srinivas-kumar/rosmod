#!/usr/bin/python
'''
This Program is designed to be the user interface
for the ROSMOD modeling language.  It has the ability
to create, load, display, edit, and export ROSMOD models.

Additionally, it supports the interaction with analysis
tools through the use of toolbar buttons and subprocesses.
'''

import wx
import wx.stc as stc
import sys, os, inspect
import copy
import multiprocessing
from threading import Thread
from fabric.api import *

from collections import OrderedDict
from wx.lib.floatcanvas import NavCanvas, FloatCanvas, Resources, Utilities
try:
    import numpy
    import numpy.random as RandomArray
    haveNumpy = True
except ImportError:
            haveNumpy = False
            errorText = (
            "The FloatCanvas requires the numpy module, version 1.* \n\n"
            "You can get info about it at:\n"
            "http://numpy.scipy.org/\n\n"
            )

# THESE ARE ALL FROM OUR CODE
import project
import metaclass
from metaModel import model_dict
from terminal import *
import dialogs
import drawable
from aspect import *
from output import *
from worker import *
from toolbar import *
import deployment
from contextMenu import *
from style import *

# Network Analysis
network_analysis = os.path.realpath(os.path.abspath
                               (os.path.join
                                (os.path.split
                                 (inspect.getfile
                                  (inspect.currentframe()
                               )
                              )[0], "network_analysis/")
                            ))
if network_analysis not in sys.path:
    sys.path.insert(0, network_analysis)
import acceptance

def MakeAdd(self,kind):
    def GenericAdd(e):
        references = []
        info = self.GetActivePanelInfo()
        model = info.obj
        canvas = info.canvas
        msgWindow = info.msgWindow

        # need to call aspect function if this should add a new tab 
        # e.g. adding a package to a workspace
        for k,v in self.AspectTypes.iteritems():
            if kind in v:
                self.OnAspectCreate(kind,None)
                return

        newObj = type( "ROS_" + kind, (object, drawable.Drawable_Object,), { '__init__' : drawable.Drawable_Object.__init__ })()
        for prop in model_dict[kind].properties:
            newObj.properties[prop] = None
        newObj.kind = kind
        newObj.parent = self.activeObject
        parent = self.activeObject
        # SET REFERENCES
        refObjectTypes = model_dict[kind].out_refs
        for refObjType in refObjectTypes:
            if refObjType[1] == "project":
                references.extend(self.project.getChildrenByKind(refObjType[0]))
            elif refObjType[1] == "parent":
                references.extend(parent.properties[refObjType[2]].getChildrenByKind(refObjType[0]))
        if newObj != None:
            newObj.properties['name'] = "New" + kind
            inputs = dialogs.EditorWindow(parent = self,
                                    editDict=newObj.properties,
                                    editObj = newObj,
                                    title="Edit "+newObj.kind,
                                    references = references)
            if inputs != OrderedDict():
                self.UpdateUndo()
                for key,value in inputs.iteritems():
                    newObj.properties[key] = value
                parent.add(newObj)
                self.AspectLog(
                    "Added child {} to parent {}".format(newObj.properties['name'],parent.properties['name']),
                    msgWindow)
                drawable.Configure(model,self.styleDict)
                self.DrawModel(model,canvas) 
    return GenericAdd

class Example(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args,**kwargs)
        self.InitUI()
        self.Maximize()
    
    def InitUI(self):

        self.activeObject = None

        self.fileTypes = "ROSMOD Project (*.rosmod)|*.rosmod"
        self.project_path = os.getcwd()
        self.project = project.ROS_Project()

        self.undoList = []
        self.redoList = []

        # build the main frame (holds viewer in the top and the output in the bottom)
        self.viewSplitter = wx.SplitterWindow(self,wx.ID_NEW,
                                              style=wx.SP_PERMIT_UNSPLIT|wx.SP_BORDER|wx.SP_3DBORDER)
        InitAspects(self)
        deployment.InitDeployment(self)
        BuildStyleDict(self)
        # build the MenuBar,Toolbar, and Statusbar
        self.BuildMenu()
        BuildToolbar(self)
        self.BuildStatusbar()

        BuildOutput(self)
        AddAspectToolbar(self,"Software")
        self.viewSplitter.SplitHorizontally(self.activeAspect,self.output,-250)
        self.viewSplitter.Bind(wx.EVT_SPLITTER_DCLICK,self.OnSplitterDClick)
        
        self.toolbar.Realize()
        self.Layout()
        
        self.SetSize((800, 600))
        self.SetTitle('ROSMOD Editor')
        self.Centre()
        self.Show(True)

        InitWorkQueue(self)

        wx.EVT_CLOSE(self, self.OnQuit)


    def DrawModel(self, model, canvas):
        c = canvas.ViewPortCenter
        canvas.UnBindAll()
        canvas.ClearAll(ResetBB=False)
        canvas.SetProjectionFun(None)
        self.BindCanvasMouseEvents(canvas)
        width,height = drawable.Layout(model,(0,0),canvas)
        model.Draw(canvas,self.OnLeftClick,self.OnRightClick,self.OnLeftDoubleClick)
        canvas.Draw()
        if c != None:
            canvas.Zoom(1,c)

    def OnLeftClick(self, Object):
        info = self.GetActivePanelInfo()
        model = info.obj
        canvas = info.canvas
        self.activeObject = Object.Name
        drawable.Configure(model,self.styleDict)
        self.activeObject.style.overlay['overlayColor']="RED"
        kind = self.activeObject.kind
        referringObjectTypes = model_dict[kind].in_refs
        for refObjType,refName in referringObjectTypes:
            refObjs = model.getChildrenByKind(refObjType)
            for refObj in refObjs:
                if refObj.properties[refName] == self.activeObject:
                    refObj.style.overlay['overlayColor']='RED'
        similarObjectTypes = model_dict[kind].display_refs
        for refType,treePath,otherProp,localProp in similarObjectTypes:
            parentObj = self.activeObject
            for node in treePath:
                if node == "parent":
                    parentObj = parentObj.parent
            refObjs = parentObj.getChildrenByKind(refType)
            for refObj in refObjs:
                if refObj.properties[otherProp] == self.activeObject.properties[localProp]:
                    refObj.style.overlay['overlayColor']='RED'
        self.DrawModel(model,canvas)

    def OnLeftDoubleClick(self, Object):
        self.AspectEdit(None)

    def OnRightClick(self, Object):
        info = self.GetActivePanelInfo()
        canvas = info.canvas
        self.activeObject = Object.Name
        self.PopupMenu(ContextMenu(canvas,AspectContextMenu(self,self.activeObject)))           

    def AspectEdit(self, e):
        info = self.GetActivePanelInfo()
        obj = info.obj
        canvas = info.canvas
        msgWindow = info.msgWindow
        kind = self.activeObject.kind
        self.AspectLog(
            "Editing {} of type {}".format(self.activeObject.properties['name'],kind),
            msgWindow)
        references = []
        refObjectTypes = model_dict[kind].out_refs
        for refObjType in refObjectTypes:
            if refObjType[1] == "project":
                references.extend(self.project.getChildrenByKind(refObjType[0]))
            elif refObjType[1] == "parent":
                references.extend(self.activeObject.parent.properties[refObjType[2]].getChildrenByKind(refObjType[0]))
        prevProps = copy.copy(self.activeObject.properties)
        inputs = dialogs.EditorWindow(parent=self,
                                editDict=self.activeObject.properties,
                                editObj = self.activeObject,
                                title="Edit "+self.activeObject.kind,
                                references = references)
        if inputs != OrderedDict():
            self.UpdateUndo()
            for key,value in inputs.iteritems():
                self.activeObject.properties[key] = value
            if self.activeObject == obj:
                newName = self.activeObject.properties['name']
                prevName = prevProps['name']
                info.name = newName
                self.activeAspectInfo.AddPageInfo(info)
                if newName != prevName:
                    self.activeAspectInfo.DelPageInfo(prevName)
            if model_dict[self.activeObject.kind].out_refs != []:
                refKey = None
                for key in self.activeObject.properties.keys():
                    if key.find("_reference") > 0:
                        refKey = key
                        break
                prevRef = prevProps[refKey]
                newRef = self.activeObject.properties[refKey]
                if newRef != prevRef:
                    self.activeObject.children = []
            drawable.Configure(obj,self.styleDict)
            selectedPage = self.activeAspect.GetSelection()
            self.activeAspect.SetPageText(selectedPage,obj.properties['name'])
            self.DrawModel(obj,canvas)
        else:
            self.activeObject.properties = prevProps

    def AspectDelete(self, e):
        info = self.GetActivePanelInfo()
        model = info.obj
        canvas = info.canvas
        msgWindow = info.msgWindow
        if model == self.activeObject:
            if info.deletable and self.activeAspect.GetPageCount() > 1:
                wx.CallAfter(self.OnAspectDelete,e)
            else:
                dialogs.ErrorDialog(self, "Cannot delete {}".format(model.properties["name"]))
        else:
            if dialogs.ConfirmDialog(self,"Delete {}?".format(self.activeObject.properties['name'])):
                self.UpdateUndo()
                self.AspectLog("Deleting {}".format(self.activeObject.properties['name']),msgWindow)
                self.activeObject.deleteAllRefs(self.project)
                self.activeObject.delete()
                drawable.Configure(model,self.styleDict)
                self.DrawModel(model,canvas)
            self.activeObject = None

    def OnAspectCreate(self,kind,e):
        info = self.GetActivePanelInfo()
        model = info.obj
        canvas = info.canvas
        msgWindow = info.msgWindow

        newObj = type( "ROS_" + kind, (object, drawable.Drawable_Object,), { '__init__' : drawable.Drawable_Object.__init__ })()
        newObj.kind = kind
        for prop in model_dict[kind].properties:
            newObj.properties[prop] = None
        newObj.properties["name"] = "New_"+ kind

        if model.kind == model_dict[kind].parent:
            newObj.parent = model
        elif model.kind == kind:
            newObj.parent = model.parent

        # SET REFERENCES
        references = []
        refObjectTypes = model_dict[kind].out_refs
        for refObjType in refObjectTypes:
            references.extend(self.project.getChildrenByKind(refObjType))

        inputs = dialogs.EditorWindow(parent=self,
                                editObj=newObj,
                                editDict=newObj.properties,
                                title="Edit "+newObj.kind,
                                references = references)
        if inputs != OrderedDict():
            self.UpdateUndo()
            for key,value in inputs.iteritems():
                newObj.properties[key] = value
            newObj.parent.add(newObj)
            numPages = self.activeAspect.GetPageCount()
            if numPages <= 0:
                numPages = 1
            BuildModelPage(self,self.activeAspect,newObj,self.activeAspectInfo,numPages-1)
            self.activeAspect.SetSelection(numPages - 1)

    def OnAspectDelete(self, e):
        selectedPage = self.activeAspect.GetSelection()
        numPages = self.activeAspect.GetPageCount()
        modelName = self.activeAspect.GetPageText(selectedPage)
        info = self.activeAspectInfo.GetPageInfo(modelName)
        model = info.obj
        if dialogs.ConfirmDialog(self,"Delete {}?".format(modelName)):
            self.UpdateUndo()
            info.canvas.ClearAll()
            model.deleteAllRefs(self.project)
            model.delete()
            self.activeAspect.GetPage(selectedPage).DestroyChildren()
            self.activeAspectInfo.DelPageInfo(modelName)
            self.activeAspect.DeletePage(selectedPage)
            self.activeObject = None
            
    def OnPackageGenerate(self,e):
        self.GenerateCode()

    def OnDeploymentAnalyze(self, e):
        selectedPage = self.activeAspect.GetSelection()
        numPages = self.activeAspect.GetPageCount()
        modelName = self.activeAspect.GetPageText(selectedPage)
        info = self.activeAspectInfo.GetPageInfo(modelName)
        dep = info.obj
        self.AnalyzeNetwork(dep)
        self.AnalyzeTiming(dep)

    def OnDeploymentGenerate(self,e):
        self.GenerateXML()

    def BuildHostDict(self,dep,rosCoreIP=""):
        #env.warn_only = False
        env.use_ssh_config = False
        self.hostDict = {}
        env.hosts = []
        hostToNodeListMap = {}
        numNodes = 0
        for node in dep.getChildrenByKind("Node"):
            host = node.properties['hardware_reference']
            numNodes += 1
            deploymentPath = node.properties['deployment_path']
            if deploymentPath == "":
                deploymentPath = host.properties['deployment_path']
            cmdArgs = node.properties['cmd_args']
            cmdArgs += " -config {} -nodename {} -hostname {}".format(
                deploymentPath + "/" + node.properties['name'] + ".xml",
                node.properties['name'],
                host.properties['name']
            )
            libs = []
            for child in node.children:
                libs.append("lib" + child.properties['component_reference'].properties['name'] + ".so")
            newNode = deployment.deployed_node(
                name = node.properties['name'],
                executable = deploymentPath + '/node_main',
                libs = libs,
                config = node.properties['name'] + ".xml",
                deploymentDir = deploymentPath,
                userName = host.properties['username'],
                keyFile = host.properties['sshkey'],
                cmdArgs = cmdArgs
            )
            if host in hostToNodeListMap.keys():
                hostToNodeListMap[host].append( newNode )
            else:
                hostToNodeListMap[host] = [ newNode ]
        for host,nodeList in hostToNodeListMap.iteritems():
            self.hostDict[host.properties['name']] = deployment.deployed_host(
                name = host.properties['name'],
                userName = host.properties['username'],
                deploymentDir = host.properties['deployment_path'],
                ipAddress = host.properties['ip_address'],
                keyFile = host.properties['sshkey'],
                nodes = nodeList,
                envVars = []
            )
            self.hostDict[host.properties['name']].envVars.append(
                ["LD_LIBRARY_PATH","{}:$LD_LIBRARY_PATH".format(host.properties['deployment_path'])]
            )
            if rosCoreIP != "":
                self.hostDict[host.properties['name']].envVars.append(
                    ['ROS_MASTER_URI','http://{}:11311/'.format(rosCoreIP)])
                self.hostDict[host.properties['name']].envVars.append(
                    ['ROS_IP',host.properties['ip_address']]
                )
            env.hosts.append(host.properties['name'])
        return numNodes
        

    def OnDeploymentMove(self,e):
        if self.deployed == False:
            selectedPage = self.activeAspect.GetSelection()
            objName = self.activeAspect.GetPageText(selectedPage)
            info = self.activeAspectInfo.GetPageInfo(objName)
            dep = info.obj
            canvas = info.canvas
            numNodes = self.BuildHostDict(dep)
            copyProgressQ = multiprocessing.Queue()
            dlg = dialogs.RMLProgressDialog( parent = self,
                                             title="Copy Progress",
                                             progress_q = copyProgressQ,
                                             numItems=numNodes)
            workerThread = WorkerThread(
                func = lambda : deployment.copyTest(
                    self,
                    self.project.project_path + "/01-Software/" + self.project.getChildrenByKind("rml")[0].properties['name'] + "/devel/lib/",
                    self.project.project_path + "/03-Deployment/"+ dep.properties['name'],
                    copyProgressQ)
            )
            workerThread.start()
            dlg.ShowModal()
            dlg.Destroy()
        else:
            dialogs.ErrorDialog(self,"Can't copy deployment files when system is running a deployment!")

    def OnDeploymentRun(self,e):
        newObj = drawable.Drawable_Object()
        newObj.properties = OrderedDict()
        newObj.properties['command'] = ""
        inputs = dialogs.EditorWindow(parent=self,
                                editDict=newObj.properties,
                                editObj = newObj,
                                title="Input Command To Run",
                                references = [])
        if inputs != OrderedDict():
            for key,value in inputs.iteritems():
                newObj.properties[key] = value
            command = newObj.properties['command']
            selectedPage = self.activeAspect.GetSelection()
            objName = self.activeAspect.GetPageText(selectedPage)
            info = self.activeAspectInfo.GetPageInfo(objName)
            dep = info.obj
            canvas = info.canvas
            if self.deployed == False:
                self.BuildHostDict(dep)
            copyProgressQ = multiprocessing.Queue()
            dlg = dialogs.RMLProgressDialog( parent = self,
                                             title="Copy Progress",
                                             progress_q = copyProgressQ,
                                             numItems=len(self.hostDict))
            workerThread = WorkerThread(func = lambda : deployment.runCommandTest(self,
                                                                                  command,
                                                                                  copyProgressQ)
                                    )
            workerThread.start()
            dlg.ShowModal()
            dlg.Destroy()

    def OnDeploymentDeploy(self,e):
        if self.deployed == False:
            selectedPage = self.activeAspect.GetSelection()
            objName = self.activeAspect.GetPageText(selectedPage)
            info = self.activeAspectInfo.GetPageInfo(objName)
            dep = info.obj
            canvas = info.canvas
            rosCoreIP = ""
            testName = "NewTest"
            properties = OrderedDict()
            properties['name'] = testName
            properties['hardware_reference'] = None
            references = dep.properties['rhw_reference'].children
            inputs = dialogs.EditorWindow(parent=self,
                                    editDict=properties,
                                    title="Deployment Options",
                                    references = references)
            if inputs != OrderedDict():
                for key,value in inputs.iteritems():
                    properties[key] = value
                rosCoreIP = properties['hardware_reference'].properties['ip_address']
                testName = properties['name']

                numNodes = self.BuildHostDict(dep,rosCoreIP)

                deploymentProgressQ = multiprocessing.Queue()
                dlg = dialogs.RMLProgressDialog( parent = self,
                                                 title="Deployment Progress",
                                                 progress_q = deploymentProgressQ,
                                                 numItems=numNodes)
                workerThread = WorkerThread(
                    func = lambda : deployment.deployTest(
                        self,
                        deploymentProgressQ
                    )
                )
                self.updatedHostDict = False
                workerThread.start()
                dlg.ShowModal()
                dlg.Destroy()
                self.runningDeployment = dep
                self.runningDeploymentCanvas = canvas
                self.runningNodes = numNodes
                self.deployed = True
                monitorQ = multiprocessing.Queue()
                workerThread = WorkerThread(
                    func = lambda : deployment.monitorTest(
                        self,
                        monitorQ
                    )
                )
                monitorWorkItem = WorkItem(process = workerThread,
                                           queue = monitorQ,
                                           workFunc = lambda e : MonitorWorkFunc(self,e))
                self.workQueue.append(monitorWorkItem)
                workerThread.start()
        else:
            dialogs.ErrorDialog(self,"System is already running a deployment!")

    def OnDeploymentStop(self,e):
        if self.deployed == True: 
            self.deployed = False
            self.deploying = False
            deploymentProgressQ = multiprocessing.Queue()
            dlg = dialogs.RMLProgressDialog(parent = self,
                                            title="Stop Deployment Progress",
                                            progress_q = deploymentProgressQ,
                                            numItems=self.runningNodes)
            workerThread = WorkerThread(
                func = lambda : deployment.stopTest(
                    self,
                    deploymentProgressQ
                )
            )
            workerThread.start()
            dlg.ShowModal()
            dlg.Destroy()
            self.runningNodes = 0
            drawable.Configure(self.runningDeployment,self.styleDict)
            self.DrawModel(self.runningDeployment,self.runningDeploymentCanvas)
        else:
            dialogs.ErrorDialog(self,"System is not running a deployment")

    def BindCanvasMouseEvents(self,canvas):
        canvas.Bind(FloatCanvas.EVT_MOUSEWHEEL, self.OnMouseWheel)
        canvas.Bind(FloatCanvas.EVT_RIGHT_UP, self.OnRightUp) 

    def UnBindCanvasMouseEvents(self,canvas):
        canvas.Unbind(FloatCanvas.EVT_MOUSEWHEEL)
        canvas.Unbind(FloatCanvas.EVT_RIGHT_UP)

    def GetActivePanelInfo(self):
        selectedAspect = self.activeAspect
        selectedAspectInfo = self.activeAspectInfo
        selectedPage = selectedAspect.GetSelection()
        pageName = selectedAspect.GetPageText(selectedPage)
        pageInfo = selectedAspectInfo.GetPageInfo(pageName)
        return pageInfo
    def AspectLog(self, text, msgWindow):
        msgWindow.SetReadOnly(False)
        msgWindow.AppendText(text)
        if not text[-1] == "\n":
            msgWindow.AppendText("\n")
        msgWindow.SetReadOnly(True)
        msgWindow.ScrollToLine(msgWindow.GetLineCount())
    def OnMouseWheel(self,event):
        info = self.GetActivePanelInfo()
        canvas = info.canvas
        Rot = event.GetWheelRotation()
        Rot = Rot / abs(Rot) * 0.1
        if event.ControlDown(): # move left-right
            canvas.MoveImage( (Rot, 0), "Panel" )
        elif event.ShiftDown():
            canvasPos = canvas.ViewPortCenter#event.GetCoords()
            if Rot > 0:
                canvas.Zoom(1.1,canvasPos)
            else:
                canvas.Zoom(0.9,canvasPos)
        else: # move up-down
            canvas.MoveImage( (0, -Rot), "Panel" )
    def OnRightUp(self,event):
        info = self.GetActivePanelInfo()
        canvas = info.canvas
        self.activeObject = info.obj
        self.PopupMenu(ContextMenu(canvas,AspectContextMenu(self,self.activeObject)))
        
    '''
    View Menu Functions
    '''
    def UpdateMainWindow(self, e):
        self.viewSplitter.Show()
        self.viewSplitter.SplitHorizontally(self.activeAspect,self.output,self.viewSplitter.GetSashPosition())
        if self.shvw.IsChecked() and self.shop.IsChecked():
            pass
        elif self.shvw.IsChecked() and not self.shop.IsChecked():
            self.viewSplitter.Unsplit(self.output)
        elif not self.shvw.IsChecked() and self.shop.IsChecked():
            self.viewSplitter.Unsplit(self.activeAspect)
        else:
            self.viewSplitter.Hide()
        self.viewSplitter.UpdateSize()
    def OnSplitterDClick(self, e):
        self.shop.Check(False)
        self.UpdateMainWindow(e)
    def ToggleAspectView(self, e):
        self.UpdateMainWindow(e)    
    def ToggleOutputView(self, e):
        self.UpdateMainWindow(e)
    def ToggleStatusBar(self, e):
        self.GetStatusBar().Show(e.IsChecked())
    def ToggleToolBar(self, e):
        self.toolbar.Show(e.IsChecked())
        self.SendSizeEvent()

    '''
    Toolbar and File Menubar Menu Functions
    '''
    def OnPrint(self, e):
        imgName, imgPath = dialogs.RMLFileDialog(
            parent = self,
            fileTypes = "PNG Images (*.png)|*.png",
            path = self.project_path,
            prompt = "Save Aspect View As Image...",
            fd_flags = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        )
        if imgName != None and imgPath != None:
            info = self.GetActivePanelInfo()
            canvas = info.canvas
            model = info.obj
            msgWindow = info.msgWindow
            canvas.Scale = 1
            canvas.SetToNewScale(False)
            canvas._ResetBoundingBox()
            box = canvas.BoundingBox
            canvas.ViewPortCenter -= (canvas.PixelToWorld((0,0)) - numpy.array((box[0,0],box[1,1])))
            bmp = wx.EmptyBitmap(box.Width,box.Height)
            dc = wx.MemoryDC()
            dc.SelectObject(bmp)
            dc.Clear()
            canvas._DrawObjects(dc,canvas._DrawList,dc,canvas.BoundingBox)
            dc.SelectObject(wx.NullBitmap)
            if imgName[-4:] != ".png":
                imgName += ".png"
            bmp.SaveFile(imgPath+'/'+imgName,wx.BITMAP_TYPE_PNG)
            self.statusbar.SetStatusText('Saved {} to {}'.format(imgName,imgPath))

    def OnQuit(self, e):
        if dialogs.ConfirmDialog(self,"Really quit ROSMOD?"):
            self.workTimer.Stop()
            exit()

    def OnNew(self, e):
        project_path = dialogs.RMLDirectoryDialog(
            parent = self,
            prompt ="Choose New Project Location", 
            path = self.project_path,
        )
        if project_path != None:
            self.project_path = project_path
            propertiesDict = OrderedDict()
            propertiesDict['Project'] = OrderedDict()
            propertiesDict['Project']['name'] = "NewProject"
            propertiesDict['Workspace'] = OrderedDict()
            propertiesDict['Workspace']['name'] = "NewWorkspace"
            propertiesDict['Hardware'] = OrderedDict()
            propertiesDict['Hardware']['name'] = "NewHardware"
            propertiesDict['Deployment'] = OrderedDict()
            propertiesDict['Deployment']['name'] = "NewDeployment"
            w = dialogs.Wizard(self,propertiesDict)
            inputs = w.GetInput()
            if inputs != None:
                self.filename = inputs['Project']['name']
                self.project.new(project_name = self.filename,
                                 project_path = self.project_path,
                                 workspace_name = inputs['Workspace']['name'],
                                 hardware_name = inputs['Hardware']['name'],
                                 deployment_name = inputs['Deployment']['name'])
                ClearAspects(self)
                BuildAspectPages(self)
                self.statusbar.SetStatusText('Created new project: {} in: {}'.format(self.filename,self.project_path))

    def OnOpen(self, e):
        filename, model_path = dialogs.RMLFileDialog(
            parent = self,
            fileTypes = self.fileTypes,
            path = self.project_path,
            prompt = "Choose a ROS Project",
            fd_flags = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        )
        if filename != None and model_path != None:
            self.filename = filename
            self.project_path = model_path
            openProgressQ = multiprocessing.Queue()
            dlg = dialogs.RMLProgressDialog( parent = self,
                                             title="Open Project Progress",
                                             progress_q = openProgressQ,
                                             numItems=11)
            workerThread = WorkerThread(func = lambda : self.project.open(self.project_path,
                                                                          openProgressQ) )
            workerThread.start()
            dlg.ShowModal()
            dlg.Destroy()
            ClearAspects(self)
            BuildAspectPages(self)
            self.statusbar.SetStatusText('Loaded project: {} from: {}'.format(self.filename,self.project_path))

    def OnSave(self, e):
        self.project.save()
        self.statusbar.SetStatusText('Saved project as: {} in: {}'.format(self.filename,self.project_path))

    def OnSaveAs(self, e):
        properties = OrderedDict()
        properties['name'] = self.project.project_name
        inputs = dialogs.EditorWindow( parent = self,
                                 editObj = None,
                                 editDict = properties,
                                 title = 'Choose New Project Name')
        if inputs != OrderedDict():
            project_path = dialogs.RMLDirectoryDialog(
                parent = self,
                prompt ="Choose New Project Location", 
                path = self.project_path,
            )
            if project_path != None:
                self.filename = inputs['name']
                self.project_path = project_path
                self.project.save(self.filename,self.project_path)
                self.statusbar.SetStatusText('Saved project as: {} in: {}'.format(self.filename,self.project_path))

    def UpdateUndo(self):
        self.undoList.append(copy.copy(self.project))
        self.toolbar.EnableTool(wx.ID_UNDO, True)

    def OnUndo(self, e):
        if len(self.undoList) > 0:
            self.redoList.append(copy.copy(self.project))
            self.project = self.undoList.pop()
            self.toolbar.EnableTool(wx.ID_REDO, True)
            if len(self.undoList) == 0:
                self.toolbar.EnableTool(wx.ID_UNDO, False)
    def OnRedo(self, e):
        if len(self.redoList) > 0:
            self.undoList.append(copy.copy(self.project))
            self.project = self.redoList.pop()
            self.toolbar.EnableTool(wx.ID_UNDO, True)
            if len(self.redoList) == 0:
                self.toolbar.EnableTool(wx.ID_REDO, False)

    def OnTerminal(self, e):
        self.shop.Check(True)
        self.UpdateMainWindow(e)
        self.output.AddPage(TermEmulatorDemo(self.output), "Terminal",select=True)

    '''
    Tools Menubar Menu Functions
    '''
    def GenerateCode(self):
        self.project.generate_workspace()
        dialogs.InfoDialog(self,"Generated ROS Workspace.")
        self.statusbar.SetStatusText('Generated ROS Workspace')
    def GenerateXML(self):
        self.project.generate_xml()
        dialogs.InfoDialog(self,"Generated Deployment XML files")
        self.statusbar.SetStatusText("Generated Deployment XML files")

    def AnalyzeNetwork(self, dep):
        print "Analyzing network characteristics for deployment: {}".format(dep.properties["name"])
        properties = OrderedDict()
        properties['period'] = "5400"
        properties['numPeriods'] = "1"
        inputs = dialogs.EditorWindow( parent = self,
                                 editObj = None,
                                 editDict = properties,
                                 title = 'Network Analysis Options')
        if inputs != OrderedDict():
            period = float(inputs['period'])
            numPeriods = int(inputs['numPeriods'])
            acceptance.AnalyzeDeployment(dep,period,numPeriods)

    def AnalyzeTiming(self, dep):
        self.project.generate_cpn()
        print "Generated CPN Timing Analysis Model"

    '''
    Build the menubar which allows for operations on
    * Files: New, Open, Save, Quit
    * Aspects: Packages, Hardware, Deployment
    * Views: Toolbar, Statusbar, Aspects, Output
    * Tools: Generator, Network QoS Analysis, Timing Analysis
    '''
    def BuildMenu(self):
        self.menubar = wx.MenuBar()

        # normal file operations menu
        self.fileMenu = wx.Menu()
        self.newMI = self.fileMenu.Append(wx.ID_NEW, '&New', 'New Project')
        self.openMI = self.fileMenu.Append(wx.ID_OPEN, '&Open', 'Open existing Project')
        self.saveMI = self.fileMenu.Append(wx.ID_SAVE, '&Save', 'Save current Project')
        self.saveAsMI = self.fileMenu.Append(wx.ID_SAVEAS, 'Save &As', 'Save current Project As...')
        self.fileMenu.AppendSeparator()
        self.quitMI = wx.MenuItem(self.fileMenu, wx.ID_EXIT, '&Quit\tCtrl+W', 'Quit ROSMOD')
        self.fileMenu.AppendItem(self.quitMI)

        # aspects (of the viewer) menu for ROSMOD: packages, hardware, deployment
        self.aspectsMenu = wx.Menu()
        self.packageAMI = self.aspectsMenu.Append(wx.ID_ANY,
                                                  "Packages",
                                                  "View/Edit the packages in the model.",
                                                  kind=wx.ITEM_RADIO
                                              )
        self.hardwareAMI = self.aspectsMenu.Append(wx.ID_ANY,
                                                   "Hardware",
                                                   "View/Edit the hardware in the model.",
                                                   kind=wx.ITEM_RADIO
                                               )
        self.deploymentAMI = self.aspectsMenu.Append(wx.ID_ANY,
                                                     "Deployment",
                                                     "View/Manage the deployment of the model.",
                                                     kind=wx.ITEM_RADIO
                                                 )

        # view menu: show/hide statusbar/toolbar/viewer/output
        self.viewMenu = wx.Menu()
        self.shst = self.viewMenu.Append(wx.ID_ANY, 'Show Statusbar', 'Show Statusbar', kind=wx.ITEM_CHECK)
        self.shtl = self.viewMenu.Append(wx.ID_ANY, 'Show Toolbar', 'Show Toolbar', kind=wx.ITEM_CHECK)
        self.shvw = self.viewMenu.Append(wx.ID_ANY, 'Show Viewer', 'Show Viewer', kind=wx.ITEM_CHECK)
        self.shop = self.viewMenu.Append(wx.ID_ANY, 'Show Output', 'Show Output', kind=wx.ITEM_CHECK)
        self.viewMenu.Check(self.shst.GetId(), True)
        self.viewMenu.Check(self.shtl.GetId(), True)
        self.viewMenu.Check(self.shvw.GetId(), True)
        self.viewMenu.Check(self.shop.GetId(), True)

        # add the menus to the menubar
        self.menubar.Append(self.fileMenu, '&File')
        self.menubar.Append(self.viewMenu, '&View')
        self.menubar.Append(self.aspectsMenu, '&Aspects')
        self.SetMenuBar(self.menubar)
        
        # set up the events for the items in the menubar
        self.RegisterMenuEvents()

    '''
    Bind menu items to functions for event processing
    '''
    def RegisterMenuEvents(self):
        # file menu
        self.Bind(wx.EVT_MENU, self.OnNew, self.newMI)
        self.Bind(wx.EVT_MENU, self.OnOpen, self.openMI)
        self.Bind(wx.EVT_MENU, self.OnSave, self.saveMI)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, self.saveAsMI)
        self.Bind(wx.EVT_MENU, self.OnQuit, self.quitMI)
        # aspect menu
        self.Bind(wx.EVT_MENU, lambda e : OnAspect(self,"Software",e), self.packageAMI)
        self.Bind(wx.EVT_MENU, lambda e : OnAspect(self,"Hardware",e), self.hardwareAMI)
        self.Bind(wx.EVT_MENU, lambda e : OnAspect(self,"Deployment",e), self.deploymentAMI)
        # view menu
        self.Bind(wx.EVT_MENU, self.ToggleStatusBar, self.shst)
        self.Bind(wx.EVT_MENU, self.ToggleToolBar, self.shtl)
        self.Bind(wx.EVT_MENU, self.ToggleAspectView, self.shvw)
        self.Bind(wx.EVT_MENU, self.ToggleOutputView, self.shop)

    '''
    Build the Statusbar which provides extra information about
    all the objects and menus in ROSMOD.  It also displays short
    info from the output about results of operations.
    '''
    def BuildStatusbar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText('Ready')

def main():
    ex = wx.App()
    Example(None)
    ex.MainLoop()    


if __name__ == '__main__':
    main()
