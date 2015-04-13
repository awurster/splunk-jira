
import splunk.admin as admin
import splunk.entity as entity
    

class ConfigApp(admin.MConfigHandler):
    '''
    Set up supported arguments
    '''
    
    def setup(self):
        if self.requestedAction == admin.ACTION_EDIT:
            s_args = ['debug', 'index',
                        'hostname', 'username', 'password', 'protocol', 'port',
                        'default_project', 'tempMax', 'keys', 'custom_keys' ]
            for arg in s_args:
                self.supportedArgs.addOptArg(arg)
        pass

    def handleList(self, confInfo):
        confDict = self.readConf('server')
        if None != confDict:
            for stanza, settings in confDict.items():
                for key, val in settings.items():
                    if key in ['hostname'] and val in [None, '']:
                        val = ''                            
                    if key in ['username'] and val in [None, '']:
                        val = ''
                    if key in ['password'] and val in [None, '']:
                        val = ''    
                    if key in ['protocol'] and val in [None, '']:
                        val = ''    
                    if key in ['port'] and val in [None, '']:
                        val = ''    
                    if key in ['path'] and val in [None, '']:   
                        val = ''    
                    confInfo[stanza].append(key, val)

    def handleEdit(self, confInfo):
        name = self.callerArgs.id
        args = self.callerArgs

        confDict = self.readConf('server')
        if None != confDict:
            for stanza, settings in confDict.items():
                for key, val in settings.items():
                    if key in ['hostname'] and val in [None, '']:
                        val = ''                            
                    if key in ['username'] and val in [None, '']:
                        val = ''
                    if key in ['password'] and val in [None, '']:
                        val = ''    
                    if key in ['protocol'] and val in [None, '']:
                        val = ''    
                    if key in ['port'] and val in [None, '']:
                        val = ''    
                    if key in ['path'] and val in [None, '']:   
                        val = ''    
                    confInfo[stanza].append(key, val)

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
                
        self.writeConf('jira', 'general', self.callerArgs.data)
        self.writeConf('jira', 'server', self.callerArgs.data)
        self.writeConf('jira', 'project', self.callerArgs.data)
                    
# initialize the handler
admin.init(ConfigApp, admin.CONTEXT_NONE)
