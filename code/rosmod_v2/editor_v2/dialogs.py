#!/usr/bin/python

import wx
import wx.stc as stc
from wx.lib.pubsub import Publisher

from collections import OrderedDict

class RMLProgressDialog(wx.Dialog):
    """
    Shows a Progres Gauge while an operation is taking place. May be cancellable
    which is possible when converting pdf/ps
    """
    def __init__(self, title, progress_topic, numItems=100, cancellable=False):
        """Defines a gauge and a timer which updates the gauge."""
        wx.Dialog.__init__(self, None, title=title)
        self.count = 0
        self.numItems = numItems
        self.progress = wx.Gauge(self, range=self.numItems)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.progress, 0, wx.EXPAND)

        if cancellable:
            cancel = wx.Button(self, wx.ID_CANCEL, _("&Cancel"))
            cancel.SetDefault()
            cancel.Bind(wx.EVT_BUTTON, self.on_cancel)
            btnSizer = wx.StdDialogButtonSizer()
            btnSizer.AddButton(cancel)
            btnSizer.Realize()
            sizer.Add(btnSizer, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)

        self.SetSizer(sizer)

        Publisher().subscribe(self.OnSubscribe, progress_topic)

    def OnSubscribe(self, message):
        # data passed with your message is put in message.data.
        print 'GOT MESSAGE:'
        print "\t{}".format(message.data)
        self.count += 1
        self.progress.SetValue(self.count)
        if self.count >= self.numItems:
            print "quitting progress bar"
            self.on_cancel(None)

    def on_cancel(self, event):
        """Cancels the conversion process"""
        self.Destroy()

def ProgressBarDialog(title,topic,numItems,cancellable=False):
    dlg = RMLProgressDialog(title=title,progress_topic=topic,numItems=numItems,cancellable=cancellable)
    dlg.ShowModal()
    dlg.Destroy()

def RMLFileDialog(frame,fileTypes,path,prompt,fd_flags):
    modelPath = None
    fileName = None
    dlg = wx.FileDialog(frame, prompt, path, "", fileTypes, fd_flags)
    if dlg.ShowModal() == wx.ID_OK:
        fileName = dlg.GetFilename()
        modelPath = dlg.GetDirectory()
    dlg.Destroy()
    return fileName, modelPath

def RMLDirectoryDialog(frame,path,prompt):
    workspacePath = None
    dlg = wx.DirDialog(frame, prompt, path)
    if dlg.ShowModal() == wx.ID_OK:
        workspacePath = dlg.GetPath()
    dlg.Destroy()
    return workspacePath

def InfoDialog(frame, info):
    dlg = wx.MessageDialog(frame, info, 'Info', wx.OK )
    dlg.ShowModal()
    dlg.Destroy()

def ErrorDialog(frame, msg):
    dlg = wx.MessageDialog(frame, msg, 'Error', wx.OK | wx.ICON_ERROR)
    dlg.ShowModal()
    dlg.Destroy()

def ConfirmDialog(frame, msg):
    dlg = wx.MessageDialog(frame, msg, 'Confirm', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
    retVal = dlg.ShowModal()
    dlg.Destroy()
    if retVal == wx.ID_YES:
        retVal = True
    else:
        retVal = False
    return retVal


class EditDialog(wx.Dialog):
    
    def __init__(self, *args, **kw):
        self.editDict = kw.pop('editDict', OrderedDict())
        self.editObj = kw.pop('editObj', None)
        title = kw.pop('title', "ROSMOD V2")
        self.references = kw.pop('references',[])
        super(EditDialog, self).__init__(*args,**kw)
        self.returnDict = OrderedDict()
        self.InitUI()
        self.SetTitle(title)

    def InitUI(self):
        
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        pbox = wx.FlexGridSizer(rows=len(self.editDict.keys()),cols=2,vgap=9,hgap=25)

        rNum = 0
        self.inputs = OrderedDict()
        for key,value in self.editDict.iteritems():
            label = None
            field = None
            if key == 'name' or \
               key == 'period' or \
               key == 'unit' or \
               key == 'ip_address' or \
               key == 'architecture' or \
               key == 'username' or \
               key == 'sshkey' or \
               key == 'init' or \
               key == 'cmdline_arguments':
                # anything that takes a string and shouldn't have a newline
                label = wx.StaticText(panel, label=key + ":")
                field = wx.TextCtrl(panel)
                if value != "" and value != None and value != []:
                    field.AppendText(value)
                self.inputs[key] = field
            elif key == 'fields' or \
                 key == 'request' or \
                 key == 'response' or \
                 key == 'env_variables':
                # anything that takes a multi-line string
                # supports code completion and syntax highlighting
                label = wx.StaticText(panel, label=key + ":")
                field = stc.StyledTextCtrl(panel)
                fieldStr = ''
                if value != None and value != []:
                    fieldStr = self.GenerateFieldString(value)
                field.SetText(fieldStr)
                field.EmptyUndoBuffer()
                field.Colourise(0,-1)
                field.SetMarginType(1, stc.STC_MARGIN_NUMBER)
                pbox.AddGrowableRow(rNum,1)
                self.inputs[key] = field
            elif key == 'service_reference' or \
                 key == 'message_reference':
                label = wx.StaticText(panel, label=key + ":")
                refNames = []
                for ref in self.references:
                    name = ""
                    if ref.parent != self.editObj.parent.parent:
                        name += ref.parent.properties['name'] + '/'
                    name += ref.properties['name']
                    refNames.append(name)
                field = wx.ComboBox(panel, choices = refNames, style=wx.CB_READONLY)
                if value != None:
                    setName = ""
                    if value.parent != self.editObj.parent.parent:
                        setName += value.parent.properties['name'] + '/'
                    setName += value.properties['name']
                    field.SetValue(setName)
                self.inputs[key] = field
            elif key == 'component_reference' or \
                 key == 'hardware_configuration_reference' or \
                 key == 'host_reference' or \
                 key == 'node_reference':
                label = wx.StaticText(panel, label=key + ":")
                refNames = [x.properties['name'] for x in self.references]
                field = wx.ComboBox(panel, choices = refNames, style=wx.CB_READONLY)
                if value != None:
                    field.SetValue(value.properties['name'])
                self.inputs[key] = field
            if label != None and field != None:
                pbox.AddMany([(label),(field,1,wx.EXPAND)])
            rNum += 1

        pbox.AddGrowableCol(1,1)

        panel.SetSizer(pbox)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, label='Ok')
        closeButton = wx.Button(self, label='Close')
        hbox.Add(okButton)
        hbox.Add(closeButton, flag=wx.LEFT, border=5)

        vbox.Add(panel, proportion=1, 
            flag=wx.ALL|wx.EXPAND, border=5)
        vbox.Add(hbox, 
            flag=wx.ALIGN_CENTER|wx.BOTTOM, border=10)

        self.SetSizer(vbox)
        
        okButton.Bind(wx.EVT_BUTTON, self.OnOk)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)

    def GenerateFieldString(self,fieldsList):
        retStr = ""
        for field in fieldsList:
            fStr = ""
            if len(field) == 2:
                fStr = ' '.join(field)
            elif len(field) == 3:
                fStr = '{} {} = {}'.format(field[0],field[1],field[2])
            if fStr != "":
                retStr += fStr + '\n'
        return retStr

    def ParseFieldLine(self,fieldLine):
        retField = []
        tmp = fieldLine.split(" ")
        if len(tmp) >= 2:
            retField = [x for x in tmp if x != "="]
        return retField

    def ParseFields(self,fieldStr):
        retFields = []
        fields = fieldStr.split('\n')
        for field in fields:
            fLst = self.ParseFieldLine(field)
            if fLst != []:
                retFields.append(fLst)
        return retFields

    def UpdateInputs(self):
        for key,field in self.inputs.iteritems():
            if key == 'name' or \
               key == 'period' or \
               key == 'unit' or \
               key == 'ip_address' or \
               key == 'architecture' or \
               key == 'username' or \
               key == 'sshkey' or \
               key == 'init' or \
               key == 'cmdline_arguments':
                self.returnDict[key] = field.GetValue()
            elif key == 'fields' or \
                 key == 'request' or \
                 key == 'response' or \
                 key == 'env_variables':
                fieldTxt = field.GetText()
                retFields = self.ParseFields(fieldTxt)
                self.returnDict[key] = retFields
            elif key == 'service_reference' or \
                 key == 'message_reference':
                objName = field.GetValue()
                refList = objName.split('/')
                for ref in self.references:
                    if ref.properties['name'] == refList[-1]:
                        if len(refList) == 1 or \
                           (len(refList) > 1 and ref.parent.properties['name'] == refList[0]):
                            obj = [ref]
                            break
                self.returnDict[key] = obj[0]
            elif key == 'component_reference' or \
                 key == 'hardware_configuration_reference' or \
                 key == 'host_reference' or \
                 key == 'node_reference':
                objName = field.GetValue()
                obj = [x for x in self.references if x.properties['name'] == objName]
                self.returnDict[key] = obj[0]

    def GetInput(self):
        return self.returnDict

    def OnOk(self,e):
        self.UpdateInputs()
        self.Destroy()

    def OnClose(self, e):
        self.returnDict = OrderedDict()
        self.Destroy()
