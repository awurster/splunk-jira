
import splunk.admin as admin
import splunk.entity as entity
    

class ConfigJiraApp(admin.MConfigHandler):
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
        # confDict = self.readConf('general')
        # if None != confDict:
        #     for stanza, settings in confDict.items():
        #         for key, val in settings.items():
        #             if key in ['debug'] and val in [None, '']:
        #                 val = ''                            
        #             if key in ['index'] and val in [None, '']:
        #                 val = ''
        #             confInfo[stanza].append(key, val)

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

        # confDict = self.readConf('project')
        # if None != confDict:
        #     for stanza, settings in confDict.items():
        #         for key, val in settings.items():
        #             if key in ['default_project'] and val in [None, '']:
        #                 val = ''                            
        #             if key in ['tempMax'] and val in [None, '']:
        #                 val = ''
        #             if key in ['custom_keys'] and val in [None, '']:
        #                 val = ''    
        #             confInfo[stanza].append(key, val)


    def handleEdit(self, confInfo):
        name = self.callerArgs.id
        args = self.callerArgs

        # if self.callerArgs.data['index'][0] in [None, '']:
        #     self.callerArgs.data['index'][0] = 'alerts'
        
        # if self.callerArgs.data['debug'][0] in [None, '']:
        #     self.callerArgs.data['debug'][0] = 'True'   

        if self.callerArgs.data['hostname'][0] in [None, '']:
            self.callerArgs.data['hostname'][0] = ''    

        if self.callerArgs.data['password'][0] in [None, '']:
            self.callerArgs.data['password'][0] = ''

        if self.callerArgs.data['protocol'][0] in [None, '']:
            self.callerArgs.data['protocol'][0] = 'https'

        if self.callerArgs.data['port'][0] in [None, '']:
            self.callerArgs.data['port'][0] = ''
        
        if self.callerArgs.data['path'][0] in [None, '']:
            self.callerArgs.data['path'][0] = ''
                
        # self.writeConf('jira', 'general', self.callerArgs.data)
        self.writeConf('jira', 'server', self.callerArgs.data)
        # self.writeConf('jira', 'project', self.callerArgs.data)
                    
# initialize the handler
admin.init(ConfigAJirapp, admin.CONTEXT_NONE)
