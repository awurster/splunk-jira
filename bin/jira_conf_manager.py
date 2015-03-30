
import splunk.admin as admin
import splunk.entity as entity
    

class JiraHandlerApp(admin.MConfigHandler):
    '''
    Set up supported arguments
    '''
    
    def setup(self):
        if self.requestedAction == admin.ACTION_EDIT:
            #for arg in ['index', 'default_owner', 'default_priority', 'save_results', 'user_directories']:
            for arg in ['index', 'default_owner', 'default_priority', 'user_directories', 'default_notify_user_template']:
                self.supportedArgs.addOptArg(arg)
        pass

    def handleList(self, confInfo):
        confDict = self.readConf("jira")
        if None != confDict:
            for stanza, jira in confDict.items():
                for key, val in settings.items():
                    #if key in ['save_results']:
                    #    if int(val) == 1:
                    #        val = '1'
                    #    else:
                    #        val = '0'
                    if key in ['hostname'] and val in [None, '']:
                        val = ''                            
                    if key in ['username'] and val in [None, '']:
                        val = ''
                    if key in ['password'] and val in [None, '']:
                        val = ''    
                    confInfo[stanza].append(key, val)

    def handleEdit(self, confInfo):
        name = self.callerArgs.id
        args = self.callerArgs
        
        if self.callerArgs.data['index'][0] in [None, '']:
            self.callerArgs.data['index'][0] = ''
        
        if self.callerArgs.data['default_owner'][0] in [None, '']:
            self.callerArgs.data['default_owner'][0] = ''   

        if self.callerArgs.data['default_priority'][0] in [None, '']:
            self.callerArgs.data['default_priority'][0] = ''    

        if self.callerArgs.data['user_directories'][0] in [None, '']:
            self.callerArgs.data['user_directories'][0] = ''

        if self.callerArgs.data['default_notify_user_template'][0] in [None, '']:
            self.callerArgs.data['default_notify_user_template'][0] = ''

        #if int(self.callerArgs.data['save_results'][0]) == 1:
        #    self.callerArgs.data['save_results'][0] = '1'
        #else:
        #    self.callerArgs.data['save_results'][0] = '0'             
                
        self.writeConf('alert_manager', 'settings', self.callerArgs.data)                        
                    
# initialize the handler
admin.init(AlertHandlerApp, admin.CONTEXT_APP_AND_USER)
