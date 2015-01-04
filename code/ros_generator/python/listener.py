# Listener
# Accumulate workspace objects while 
# walking the parse tree
#
# Author: Pranav Srinivas Kumar
# Date: 2014.12.16

'''
* create dictionaries for each context menu?
'''


from ROSListener import ROSListener
from collections import OrderedDict

import sys,os
sys.path.append('../../python_gui/')
from CanvasOptions import *
from rosmod_dialogs import *

# ROS_Workspace class
class ROS_Workspace:

    def __init__(self):
        # Name of ROS workspace
        self.name = ""
        # List of ROS packages in workspace
        self.packages = []
        # Useful Dictionaries
        self.packages_dict = OrderedDict()

    def AddPackage(self,package):
        self.DeletePackage(package.name)
        self.packages.append(package)
        self.packages_dict[package.name] = package
    def DeletePackage(self,name):
        if name in self.packages_dict:
            del self.packages_dict[name]
        self.packages[:] = [pack for pack in self.packages if pack.name != name]

    def __str__(self):
        workspace = "workspace " + self.name + ";"
        if len(self.packages) > 0:
            workspace += ""
            for package in self.packages:
                workspace += "\npackage " + package.name
                workspace += "\n{"
                workspace += str(package)
                workspace += "\n}"
        return workspace

# ROS_Package class
class ROS_Package:

    def __init__(self):
        # Name of ROS package
        self.name = ""
        # List of messages in package
        self.messages = []
        # List of services in package
        self.services = []
        # List of components in package
        self.components = []
        # List of nodes in package
        self.nodes = []
        # Useful Dictionaries
        self.msg_dict = OrderedDict()
        self.srv_dict = OrderedDict()
        self.component_definition_dict = OrderedDict()
        self.nodes_dict = OrderedDict()

    def Edit(self):
        print "Popup window to input name"

    def AddMessage(self,message):
        self.DeleteMessage(message.name)
        self.messages.append(message)
        self.msg_dict[message.name] = message
    def DeleteMessage(self,name):
        if name in self.msg_dict:
            del self.msg_dict[name]
        self.messages[:] = [msg for msg in self.messages if msg.name != name]

    def AddService(self,service):
        self.DeleteService(service.name)
        self.services.append(service)
        self.srv_dict[service.name] = service
    def DeleteService(self,name):
        if name in self.srv_dict:
            del self.srv_dict[name]
        self.services[:] = [srv for srv in self.services if srv.name != name]

    def AddComponent(self,component):
        self.DeleteComponent(component.name)
        self.components.append(component)
        self.component_definition_dict[component.name] = component
    def DeleteComponent(self,name):
        if name in self.component_definition_dict:
            del self.component_definition_dict[name]
        self.components[:] = [comp for comp in self.components if comp.name != name]

    def AddNode(self,node):
        self.DeleteNode(node.name)
        self.nodes.append(node)
        self.nodes_dict[node.name] = node
    def DeleteNode(self,name):
        if name in self.nodes_dict:
            del self.nodes_dict[name]
        self.nodes[:] = [node for node in self.nodes if node.name != name]

    def __str__(self):
        package = ""
        if len(self.messages) > 0:
            package += "\n    messages"
            package += "\n    {"
            for msg in self.messages:
                package += str(msg)
            package += "\n    }"
        if len(self.services) > 0:
            package += "\n    services"
            package += "\n    {"
            for srv in self.services:
                package += str(srv)
            package += "\n    }"
        if len(self.components) > 0:
            package += "\n    components"
            package += "\n    {"
            for component in self.components:
                package += str(component)
            package += "\n    }"
        if len(self.nodes) > 0:
            package += "\n    nodes"
            package += "\n    {"
            for node in self.nodes:
                package += str(node)
            package += "\n    }"

        return package
        

# ROS Message class
class ROS_Message(CanvasObject):

    def __init__(self):
        CanvasObject.__init__(self)
        # Name of ROS Message
        self.name = ""
        # List of msg fields
        self.fields = []

    def Edit(self):
        print "Popup window to edit name and add fields"
        d = EditorDialogPopup(parent=self.canvas,title=self.name)
        if d.result != None:
            self.name = d.result[0]
            

    def __str__(self):
        msg = "\n        msg " + self.name
        msg += "\n        {"
        for field in self.fields:
            if len(field) > 2:
                msg += "\n            " + field[0] + " " + field[1] + "=" + field[2] + ";"
            else:
                msg += "\n            " + field[0] + " " + field[1] + ";"
        msg += "\n        }"
        return msg

class ROS_Server(CanvasObject):
    
    def __init__(self):
        CanvasObject.__init__(self)
        # Name change is not saved currently, not supported by grammar
        self.name = ""
        # reference to the actual service object
        self.service = None

class ROS_Client(CanvasObject):
    
    def __init__(self):
        CanvasObject.__init__(self)
        # Name change is not saved currently, not supported by grammar
        self.name = ""
        # reference to the actual service object
        self.service = None

# ROS Service class
class ROS_Service(CanvasObject):

    def __init__(self):
        CanvasObject.__init__(self)
        # Name of ROS Service
        self.name = ""
        # List of request fields
        self.request_fields = []
        # List of response fields
        self.response_fields = []

    def Edit(self):
        print "Popup window to edit name and add requests and responses"
        d = EditorDialogPopup(parent=self.canvas,title=self.name)
        if d.result != None:
            self.name = d.result[0]
        
    def __str__(self):
        srv_str = "\n        srv " + self.name
        srv_str += "\n        {"
        if len(self.request_fields) > 0:
            srv_str += "\n            request"
            srv_str += "\n            {"
            for field in self.request_fields:
                if len(field) > 2:
                    srv_str += "\n                " 
                    srv_str += field[0] + " " + field[1] + "=" + field[2] + ";"
                else:
                    srv_str += "\n                " 
                    srv_str += field[0] + " " + field[1] + ";"
            srv_str += "\n            }"
        if len(self.response_fields) > 0:
            srv_str += "\n            response"
            srv_str += "\n            {"
            for field in self.response_fields:
                if len(field) > 2:
                    srv_str += "\n                " 
                    srv_str += field[0] + " " + field[1] + "=" + field[2] + ";"
                else:
                    srv_str += "\n                " 
                    srv_str += field[0] + " " + field[1] + ";"
            srv_str += "\n             }"
        srv_str += "\n        }"
        return srv_str

# ROS Component class
class ROS_Component(CanvasObject):
    
    def __init__(self):
        CanvasObject.__init__(self)
        # Name of the ROS component
        self.name = ""
        # List of provided services
        self.provided_services = []
        # List of required services
        self.required_services = []
        # List of publisher ports
        self.publishers = []
        # List of subscriber ports
        self.subscribers = []
        # List of timers
        self.timers = []

    def Edit(self):
        print "popup window to edit name"
        d = EditorDialogPopup(parent=self.canvas,title=self.name)
        if d.result != None:
            self.name = d.result[0]

    def addTimer(self,timer):
        self.deleteTimer(timer.name)
        self.timers.append(timer)
    def deleteTimer(self,name):
        self.timers[:] = [tmr for tmr in self.timers if tmr.name != name]

    def addServer(self,server):
        self.deleteServer(server.name)
        self.provided_services.append(server)
    def deleteServer(self,name):
        self.provided_services[:] = [srv for srv in self.provided_services if srv.name != name]

    def addClient(self,client):
        self.deleteClient(client.name)
        self.required_services.append(client)
    def deleteClient(self,name):
        self.required_services[:] = [srv for srv in self.required_services if srv.name != name]

    def addPublisher(self,pub):
        self.deletePublisher(pub.name)
        self.publishers.append(pub)
    def deletePublisher(self,name):
        self.publishers[:] = [msg for msg in self.publishers if msg.name != name]

    def addSubscriber(self,sub):
        self.deleteSubscriber(sub.name)
        self.subscribers.append(sub)
    def deleteSubscriber(self,name):
        self.subscribers[:] = [msg for msg in self.subscribers if msg.name != name]

    def buildChildList(self):
        self.cleanChildren()
        for obj in self.subscribers:
            objType = 'subscriber'
            obj.setCanvasParams(
                canvas = self.canvas,
                position = self.position,
                canvasOptions = canvasOptionsDict[objType]
            )
            objDrawOptions = canvasOptionsDict[objType].drawOptions
            obj.drawOptions = DrawOptions(
                color = objDrawOptions.color,
                minSize = objDrawOptions.minSize,
                textPosition = "RIGHT", connectFrom = True
            )
            self.addChild(obj.name,obj)
        for obj in self.publishers:
            objType = 'publisher'
            obj.setCanvasParams(
                canvas = self.canvas,
                position = self.position,
                canvasOptions = canvasOptionsDict[objType]
            )
            objDrawOptions = canvasOptionsDict[objType].drawOptions
            obj.drawOptions = DrawOptions(
                color = objDrawOptions.color,
                minSize = objDrawOptions.minSize,
                textPosition = "RIGHT", connectFrom = True
            )
            self.addChild(obj.name,obj)
        for obj in self.timers:
            objType = 'timer'
            obj.setCanvasParams(
                canvas = self.canvas,
                position = self.position,
                canvasOptions = canvasOptionsDict[objType]
            )
            objDrawOptions = canvasOptionsDict[objType].drawOptions
            obj.drawOptions = DrawOptions(
                color = objDrawOptions.color,
                minSize = objDrawOptions.minSize,
                textPosition = "RIGHT", connectFrom = True
            )
            self.addChild(obj.name,obj)
        for obj in self.provided_services:
            objType = 'server'
            obj.setCanvasParams(
                canvas = self.canvas,
                position = self.position,
                canvasOptions = canvasOptionsDict[objType]
            )
            objDrawOptions = canvasOptionsDict[objType].drawOptions
            obj.drawOptions = DrawOptions(
                color = objDrawOptions.color,
                minSize = objDrawOptions.minSize,
                textPosition = "RIGHT", connectFrom = True
            )
            self.addChild(obj.name,obj)
        for obj in self.required_services:
            objType = 'client'
            obj.setCanvasParams(
                canvas = self.canvas,
                position = self.position,
                canvasOptions = canvasOptionsDict[objType]
            )
            objDrawOptions = canvasOptionsDict[objType].drawOptions
            obj.drawOptions = DrawOptions(
                color = objDrawOptions.color,
                minSize = objDrawOptions.minSize,
                textPosition = "RIGHT", connectFrom = True
            )
            self.addChild(obj.name,obj)

    def __str__(self):
        comp = "\n        component " + self.name
        comp += "\n        {"
        if len(self.provided_services) > 0:
            for provided in self.provided_services:
                comp += "\n            provides " + provided.service.name + ";"
        if len(self.required_services) > 0:
            for required in self.required_services:
                comp += "\n            requires " + required.service.name + ";"
        if len(self.publishers) > 0:
            for publisher in self.publishers:
                comp += "\n            publisher<" + publisher.topic + "> " + publisher.name + ";" 
        if len(self.subscribers) > 0:
            for subscriber in self.subscribers:
                comp += "\n            subscriber<" + subscriber.topic + "> " + subscriber.name + ";"
        if len(self.timers) > 0:
            for timer in self.timers:
                comp += "\n            timer " + timer.name
                comp += "\n            {"
                comp += "\n                period = " + timer.period + timer.period_unit + ";";
                comp += "\n            }"
        comp += "\n        }"
        return comp

# ROS Publisher
class ROS_Publisher(CanvasObject):
    
    def __init__(self):
        CanvasObject.__init__(self)
        # Name of publisher port
        self.name = ""
        # Name of msg topic
        self.topic = ""

    def Edit(self):
        print "Popup window to edit name and topic"
        d = EditorDialogPopup(parent=self.canvas,title=self.name)
        if d.result != None:
            self.name = d.result[0]

# ROS Subscriber
class ROS_Subscriber(CanvasObject):
    
    def __init__(self):
        CanvasObject.__init__(self)
        # Name of subscriber port
        self.name = ""
        # Name of msg topic
        self.topic = ""

    def Edit(self):
        print "Popup window to edit name and topic"
        d = EditorDialogPopup(parent=self.canvas,title=self.name)
        if d.result != None:
            self.name = d.result[0]

# ROS Timer
class ROS_Timer(CanvasObject):
    
    def __init__(self):
        CanvasObject.__init__(self)
        # Name of timer
        self.name = ""
        # Period of timer
        self.period = "0.0"
        # Unit of timer period
        self.period_unit = ""

    def Edit(self):
        print "Popup window to edit name, period, and units"
        d = EditorDialogPopup(parent=self.canvas,title=self.name)
        if d.result != None:
            self.name = d.result[0]

# ROS Node
class ROS_Node(CanvasObject):
    
    def __init__(self):
        CanvasObject.__init__(self)
        # Name of the ROS node
        self.name = ""
        # List of components
        self.components = []
        # List of component defs
        self.comp_defs = []
        # Useful Dictionary
        self.component_instance_dict = OrderedDict()

    def Edit(self):
        print "Popup window to edit name"
        d = EditorDialogPopup(parent=self.canvas,title=self.name)
        if d.result != None:
            self.name = d.result[0]

    def AddComponent(self,component):
        self.DeleteComponent(component.name)
        self.components.append(component)
        self.component_definition_dict[component.name] = component
    def DeleteComponent(self,name):
        if name in self.component_instance_dict:
            del self.component_instance_dict[name]
        self.components[:] = [comp for comp in self.components if comp.name != name]

    def __str__(self):
        node = "\n        node " + self.name
        node += "\n        {"
        for instance in self.components:
            node += "\n            component<" + instance[0] + "> " + instance[1] + ";"
        node += "\n        }"
        return node

    def buildChildList(self):
        self.cleanChildren()
        for name, compInst in self.component_instance_dict.iteritems():
            childObj = CanvasObject( name=name, isObjRef=True, objRef=compInst)
            childObj.setCanvasParams(
                canvas = self.canvas,
                position = self.position,
                canvasOptions = canvasOptionsDict['component']
            )
            objDrawOptions = canvasOptionsDict['component'].drawOptions
            childObj.drawOptions = DrawOptions(
                    color = objDrawOptions.color,
                    minSize = objDrawOptions.minSize,
                    textPosition = "RIGHT", connectFrom = True
                )
            self.addChild(name,childObj)

class Listener(ROSListener):
    def __init__(self):
        self.workspace = ROS_Workspace()

    # Create a new workspace object
    def enterDefine_workspace(self, ctx):
        self.workspace = ROS_Workspace()

    # Save the workspace name
    def enterWorkspace_name(self, ctx):
        self.workspace.name = ctx.getText()

    # Create a new ROS package object
    def enterRos_packages(self, ctx):
        self.package = ROS_Package()

    # On exit, add the new package to list of packages in workspace
    def exitRos_packages(self, ctx):
        self.workspace.packages.append(self.package)
        self.workspace.packages_dict[self.package.name] = self.package

    # Save the package name
    def enterPackage_name(self, ctx):
        self.package.name = ctx.getText()

    # Create a new ROS message object
    def enterRos_msg(self, ctx):
        self.message = ROS_Message()

    # Save the message name
    def enterMsg_name(self, ctx):
        self.message.name = ctx.getText()

    # Save the fields in the ROS msg
    def enterMsg_field(self,ctx):
        field_type = ""
        field_name = ""
        for child in ctx.getChildren():
            context = str(type(child))
            # Find the message field type
            if "Msg_field_typeContext" in context:
                field_type = child.getText()
            # Find the message field name
            if "Msg_field_nameContext" in context:
                field_name = child.getText()
        if field_type != "":
            if field_name != "":
                self.message.fields.append([field_type, field_name])

    # On exit, append message to list of messages in package
    def exitRos_msg(self, ctx):
        # Append new ros msg onto list of package messages
        self.package.messages.append(self.message)
        self.package.msg_dict[self.message.name] = self.message

    # Create a new ROS Service object
    def enterRos_srv(self, ctx):
        self.service = ROS_Service()

    # Save the name of the ROS Service
    def enterSrv_name(self, ctx):
        self.service.name = ctx.getText()

    # Save the request arguments of the service
    def enterReq_argument(self, ctx):
        field_type = ""
        field_name = ""
        field_value = ""
        for child in ctx.getChildren():
            context = str(type(child))
            # Find request field type
            if "Req_field_typeContext" in context:
                field_type = child.getText()
            # Find request field name
            if "Req_field_nameContext" in context:
                field_name = child.getText()
            # Find request field value
            if "Req_field_valueContext" in context:
                field_value = child.getText()
        if field_type != "":
            if field_name != "":
                if field_value != "":
                    self.service.request_fields.append([field_type, field_name, field_value])
                else:
                    self.service.request_fields.append([field_type, field_name])

                
    # Save the response arguments of the service
    def enterRes_argument(self, ctx):
        field_type = ""
        field_name = ""
        field_value = ""
        for child in ctx.getChildren():
            context = str(type(child))
            # Find request field type
            if "Res_field_typeContext" in context:
                field_type = child.getText()
            # Find request field name
            if "Res_field_nameContext" in context:
                field_name = child.getText()
            # Find request field value
            if "Res_field_valueContext" in context:
                field_value = child.getText()
        if field_type != "":
            if field_name != "":
                if field_value != "":
                    self.service.response_fields.append([field_type, field_name, field_value])
                else:
                    self.service.response_fields.append([field_type, field_name])

    # On exit, add the service to the list of services in the package
    def exitRos_srv(self, ctx):
        self.package.services.append(self.service)
        self.package.srv_dict[self.service.name] = self.service
        
    # Create a new component object
    def enterRos_component(self, ctx):
        self.component = ROS_Component()

    # Save the name of the component
    def enterComponent_name(self, ctx):
        self.component.name = ctx.getText()

    # Save all provided and required services
    def enterRos_service(self, ctx):
        if "provides" in ctx.getText():
            for child in ctx.getChildren():
                context = str(type(child))
                if "Service_nameContext" in context:
                    service_name = child.getText()
                    # CHECK: If this service has been defined 
                    self.server = ROS_Server()
                    self.server.name = service_name + "_server"
                    self.server.service = self.package.srv_dict[service_name]
                    self.component.addServer(self.server)
        elif "requires" in ctx.getText():
            for child in ctx.getChildren():
                context = str(type(child))
                if "Service_nameContext" in context:
                    service_name = child.getText()
                    # CHECK: If this service has been defined 
                    self.client = ROS_Client()
                    self.client.name = service_name + "_client"
                    self.client.service = self.package.srv_dict[service_name]
                    self.component.addClient(self.client)

    # Save all publishers and susbcribers
    def enterRos_pub_sub(self, ctx):
        if "publisher" in ctx.getText():
            self.publisher = ROS_Publisher()
            for child in ctx.getChildren():
                context = str(type(child))
                if "TopicContext" in context:
                    self.publisher.topic = child.getText()
                    # CHECK: If this toic has been defined
                if "PublisherContext" in context:
                    self.publisher.name = child.getText()
            if self.publisher.name != "":
                if self.publisher.topic != "":
                    self.component.addPublisher(self.publisher)

        elif "subscriber" in ctx.getText():
            self.subscriber = ROS_Subscriber()
            for child in ctx.getChildren():
                context = str(type(child))
                if "TopicContext" in context:
                    self.subscriber.topic =  child.getText()
                    # CHECK: If this topic has been defined
                if "SubscriberContext" in context:
                    self.subscriber.name = child.getText()
            if self.subscriber.name != "":
                if self.subscriber.topic != "":
                    self.component.addSubscriber(self.subscriber)

    # Save all component timers
    def enterRos_timer(self, ctx):
        self.timer = ROS_Timer()
        for child in ctx.getChildren():
            context = str(type(child))
            if "Timer_nameContext" in context:
                self.timer.name = child.getText()
            elif "Timer_periodContext" in context:
                self.timer.period = child.getText()
            elif "Period_unitContext" in context:
                self.timer.period_unit = child.getText()
        self.component.addTimer(self.timer)

    # On exit, add component to list of components in package
    def exitRos_component(self, ctx):
        self.package.components.append(self.component)
        self.package.component_definition_dict[self.component.name] = self.component

    # Create a new ROS node object
    def enterRos_node(self, ctx):
        self.node = ROS_Node()

    # Save ROS node name
    def enterNode_name(self, ctx):
        self.node.name = ctx.getText()

    # Save the component instances in each node
    def enterComponent_instances(self, ctx):
        comp_type = ""
        instance = ""
        for child in ctx.getChildren():
            context = str(type(child))
            if "Component_typeContext" in context:
                # CHECK: If this component has been defined
                comp_type = child.getText()

            elif "Component_instanceContext" in context:
                instance = child.getText()
        self.node.components.append([comp_type, instance])
        self.node.comp_defs.append(comp_type)
        self.node.component_instance_dict[instance] = self.package.component_definition_dict[comp_type]

    # On exit, add the node to the list of nodes in package
    def exitRos_node(self, ctx):
        self.package.nodes.append(self.node)
        self.package.nodes_dict[self.node.name] = self.node
